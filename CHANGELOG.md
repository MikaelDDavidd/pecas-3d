# Changelog

## 0.1.1 - 2026-11-23

- `p3d validar --exportar` reexporta com a mesma malha usada na geração (fica gravada no .FCStd).
- STL com defeito de malha (comum em texto gravado) é refeito com malha mais fina antes de dar falha.

## 0.1.0 - 2026-11-23

Primeira versão.

- `p3d setup` acha o FreeCAD no macOS e instala o 1.1.4 no Linux (AppImage com SHA256 fixo, sem sudo).
- `p3d gerar`, `validar`, `render`, `abrir`, `testar` e `nova`.
- Validação de esboços, sólidos, planilha e STL em `lib/validacao.py`.
- Exemplos: régua de folgas print-in-place e engrenagem para registro de PVC.
