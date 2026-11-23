# Preview PNG de um STL sem tela e sem Blender: rasterização simples com numpy, dentro do
# freecadcmd. Rodado pelo `p3d render arquivo.stl [saida.png] [cor] [iso|tras|topo]`.
# Fundo claro, peça em cor sólida com luz difusa, contorno de silhueta. ~5 a 20 s.
import struct
import sys
import zlib

import Mesh
import numpy as np

LARG, ALT = 1000, 750


def png(caminho, img):
    h, w, _ = img.shape
    cru = b"".join(b"\x00" + img[y].tobytes() for y in range(h))

    def bloco(tipo, dados):
        c = struct.pack(">I", len(dados)) + tipo + dados
        return c + struct.pack(">I", zlib.crc32(tipo + dados) & 0xFFFFFFFF)

    with open(caminho, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + bloco(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
                + bloco(b"IDAT", zlib.compress(cru, 6)) + bloco(b"IEND", b""))


def vista(nome):
    """Matriz de rotação mundo -> câmera (x direita, y cima, z para o observador)."""
    az, el = {"iso": (-45, 35), "tras": (135, 35), "topo": (0, 89.9)}.get(nome, (-45, 35))
    a, e = np.radians(az), np.radians(el)
    rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
    # olhando de cima com elevação e: Z do mundo sobe na tela e aponta um pouco para a câmera
    rx = np.array([[1, 0, 0], [0, np.sin(e), np.cos(e)], [0, -np.cos(e), np.sin(e)]])
    return rx @ rz


def main(stl, saida, cor, nome_vista):
    malha = Mesh.Mesh(stl)
    tri = np.array([[list(p) for p in f.Points] for f in malha.Facets], dtype=float)
    centro = (tri.reshape(-1, 3).max(0) + tri.reshape(-1, 3).min(0)) / 2
    r = vista(nome_vista)
    t = (tri - centro) @ r.T
    xy = t[:, :, :2]
    lo, hi = xy.reshape(-1, 2).min(0), xy.reshape(-1, 2).max(0)
    escala = 0.85 * min(LARG / (hi[0] - lo[0]), ALT / (hi[1] - lo[1]))
    px = (xy - (lo + hi) / 2) * escala
    sx = px[:, :, 0] + LARG / 2
    sy = ALT / 2 - px[:, :, 1]
    sz = t[:, :, 2]

    n = np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0])
    norma = np.linalg.norm(n, axis=1)
    n = n / np.where(norma == 0, 1, norma)[:, None]
    luz = np.array([-0.4, 0.6, 0.7]); luz /= np.linalg.norm(luz)
    brilho = 0.30 + 0.70 * np.abs(n @ luz)
    base = np.array([int(cor[i:i + 2], 16) for i in (0, 2, 4)], dtype=float)

    zbuf = np.full((ALT, LARG), -np.inf)
    img = np.empty((ALT, LARG, 3), dtype=np.uint8)
    yy, xx = np.mgrid[0:ALT, 0:LARG]
    fundo = (238 - 18 * yy / ALT).astype(np.uint8)
    img[:] = fundo[:, :, None]
    mascara = np.zeros((ALT, LARG), dtype=bool)

    for i in range(len(tri)):
        x0, x1, x2 = sx[i]; y0, y1, y2 = sy[i]
        area = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
        if abs(area) < 1e-9:
            continue
        xa, xb = int(max(0, np.floor(min(x0, x1, x2)))), int(min(LARG - 1, np.ceil(max(x0, x1, x2))))
        ya, yb = int(max(0, np.floor(min(y0, y1, y2)))), int(min(ALT - 1, np.ceil(max(y0, y1, y2))))
        if xa > xb or ya > yb:
            continue
        gx, gy = xx[ya:yb + 1, xa:xb + 1] + 0.5, yy[ya:yb + 1, xa:xb + 1] + 0.5
        w0 = ((x1 - gx) * (y2 - gy) - (x2 - gx) * (y1 - gy)) / area
        w1 = ((x2 - gx) * (y0 - gy) - (x0 - gx) * (y2 - gy)) / area
        w2 = 1 - w0 - w1
        dentro = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
        if not dentro.any():
            continue
        z = w0 * sz[i, 0] + w1 * sz[i, 1] + w2 * sz[i, 2]
        zb = zbuf[ya:yb + 1, xa:xb + 1]
        frente = dentro & (z > zb)
        zb[frente] = z[frente]
        img[ya:yb + 1, xa:xb + 1][frente] = np.clip(base * brilho[i], 0, 255).astype(np.uint8)
        mascara[ya:yb + 1, xa:xb + 1] |= dentro

    borda = mascara & ~(np.roll(mascara, 1, 0) & np.roll(mascara, -1, 0) & np.roll(mascara, 1, 1) & np.roll(mascara, -1, 1))
    img[borda] = (40, 40, 40)
    png(saida, img)
    print(f"PREVIEW_OK {saida} ({len(tri)} triângulos, vista {nome_vista})")


if len(sys.argv) < 3:
    raise SystemExit("uso: p3d render arquivo.stl saida.png [cor_hex] [iso|tras|topo]")
main(sys.argv[1], sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else "E07A2F").lstrip("#"),
     sys.argv[4] if len(sys.argv) > 4 else "iso")
