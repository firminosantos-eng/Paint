# Projeto Paint — Programação A 2026-1

Projeto da disciplina **Programação A (2026-1)** — DCOMP/UFS.

Um programa do tipo *paint* em Python com Tkinter, no estilo das aplicações
Google Drawings e LibreOffice Draw. O projeto parte de uma implementação
imperativa simples e evolui, ao longo de 7 entregas, para uma arquitetura
Orientada a Objetos com MVC e padrões de projeto.

Este exercício foi desenvolvido por Dr. Giovanny Fernando Lucero Palma e
utilizado por docentes desta disciplina. Dr. André Yoshiaki Kashiwabara
adaptou o exercício para a turma T05 de 2026/1.

## Requisitos

- Python 3.10 ou superior.
- Tkinter (incluído na maioria das instalações de Python; no Linux pode
  exigir o pacote `python3-tk`).

Para conferir se o Tkinter está disponível:

```bash
python -m tkinter
```

## Como executar

Cada script abre uma janela própria. A partir da raiz do projeto:

```bash
python 01-linha.py            # desenha uma única linha (apaga a anterior)
python 02-linhas.py           # acumula várias linhas
python 03-linhasERabiscos.py  # linhas, rabiscos, retângulos e ovais, com cores (Entrega 1)
```

## Mapa dos arquivos

| Arquivo                    | Descrição                                                                 |
|-----------------------------|----------------------------------------------------------------------------|
| `descricao.ipynb`           | Enunciado completo do projeto (entregas, datas, tags Git).                |
| `01-linha.py`                | Referência imperativa: uma única linha por vez.                          |
| `02-linhas.py`               | Referência imperativa: várias linhas acumuladas.                         |
| `03-linhasERabiscos.py`      | **Entrega atual** — linhas, rabiscos, retângulos e ovais, com cor de borda e de preenchimento por figura. |

## Progresso das entregas

- [x] **Entrega 1** (tag `imperativa.1`) — Familiarização com Tkinter e com o
  fluxo Git/GitHub da equipe. Partindo do esqueleto de linhas e rabiscos,
  foram adicionadas:
  - Desenho de **retângulos**.
  - Desenho de **ovais**.
  - **Cor de borda** configurável por figura.
  - **Cor de preenchimento** configurável por figura.

  Implementação ainda em estilo imperativo (`if tipo == "..."`), como
  esperado nesta etapa. A condicional por tipo será eliminada na Entrega 4,
  com o padrão *State*.

- [ ] **Entrega 2** — a definir conforme o enunciado.
- [ ] **Entrega 3** — a definir conforme o enunciado.
- [ ] **Entrega 4** (padrão *State*) — eliminação das condicionais por tipo de figura.
- [ ] **Entrega 5** — a definir conforme o enunciado.
- [ ] **Entrega 6** — a definir conforme o enunciado.
- [ ] **Entrega 7** — a definir conforme o enunciado.

## Como as figuras são representadas (Entrega 1)

Cada figura desenhada é guardada como uma tupla:

```python
(tipo, valores, cor_borda, cor_preenchimento)
```

onde `tipo` pertence a `{"linha", "rabisco", "retangulo", "oval"}`. As cores
são fixadas no momento em que a figura é criada, então trocar a cor
selecionada na interface não altera figuras já desenhadas.

## Créditos

- Exercício original: Dr. Giovanny Fernando Lucero Palma.
- Adaptação para a turma T05 (2026/1): Prof. Dr. André Yoshiaki Kashiwabara — DCOMP/UFS.
