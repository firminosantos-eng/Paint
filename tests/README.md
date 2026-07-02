# Testes automatizados

Testes do Model (`Figura` e `Desenho`), adicionados na **Entrega 4**.
Como o Model não depende de Tkinter, os testes rodam sem precisar de
display gráfico.

- `test_figura_geometria.py` — criação, mover (`atualizar`) e
  clique/seleção (`contem_ponto`) de cada tipo de figura.
- `test_serializacao.py` — round-trip figura → dicionário → figura, e o
  ciclo Salvar/Abrir via `RepositorioDesenho`.

## Como rodar

A partir da raiz do projeto:

```bash
pip install pytest
pytest
```

Essa pasta deve continuar crescendo nas próximas entregas (Composite na
Entrega 6, comandos na Entrega 7).

