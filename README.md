# Projeto Paint — Programação A 2026-1

Projeto da disciplina **Programação A (2026-1)** — DCOMP/UFS, Turma T05.

Um programa do tipo *paint* em Python com Tkinter, no estilo das aplicações
Google Drawings e LibreOffice Draw. O projeto parte de uma implementação
imperativa simples e evolui, ao longo de 7 entregas, para uma arquitetura
Orientada a Objetos com MVC e padrões de projeto.


## Requisitos

- Python 3.10 ou superior.
- Tkinter (incluído na maioria das instalações de Python; no Linux pode
  exigir o pacote `python3-tk`).

Para conferir se o Tkinter está disponível:

```bash
python -m tkinter
```

## Como executar

Cada script de referência abre uma janela própria. A partir da raiz do projeto:

```bash
python 01-linha.py         # desenha uma única linha (apaga a anterior)
python 02-linhas.py        # acumula várias linhas
python linhasERabiscos.py  # base atual dos alunos — versão Orientada a Objetos (Entrega 2)
```

O `linhasERabiscos.py` importa a hierarquia de classes de `figuras.py`, então
os dois arquivos precisam estar na mesma pasta.

**Ferramentas disponíveis:** Linha, Rabisco, Retângulo, Oval, e um submenu
**Formas** com figuras prontas (Triângulo, Pentágono, Hexágono, Estrela).
Todas funcionam por clique e arraste: você desenha uma caixa delimitadora e
a figura se ajusta a ela — inclusive as formas do submenu, que se esticam
proporcionalmente à caixa, como no galeria de "Formas" do Word.

## Mapa dos arquivos

| Arquivo                | Descrição                                                                 |
|--------------------------|----------------------------------------------------------------------------|
| `descricao.ipynb`        | Enunciado completo do projeto (entregas, datas, tags Git).                |
| `01-linha.py`             | Referência imperativa: uma única linha por vez.                          |
| `02-linhas.py`            | Referência imperativa: várias linhas acumuladas.                         |
| `linhasERabiscos.py`      | **Base dos alunos / entrega atual** — interface Tkinter e eventos de mouse, usando a hierarquia de `figuras.py`. |
| `figuras.py`              | **Módulo de classes (Entrega 2)** — hierarquia `Figura` (Linha, Rabisco, Retangulo, Oval, Triangulo, Pentagono, Hexagono, Estrela). |

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

- [x] **Entrega 2** (tag `orientadoaobjetos.2`) — Substituição do código
  imperativo por modelagem Orientada a Objetos:
  - Hierarquia de classes `Figura` (`figuras.py`): `Figura` (abstrata) →
    `FiguraDoisPontos` (linha, retângulo, oval, formas prontas) e, direto
    de `Figura`, `Rabisco`.
  - `linhasERabiscos.py` adequado para usar a hierarquia via polimorfismo
    (`figura.desenhar(...)`, `figura.incompleta()`), sem mais nenhum
    `if tipo == "..."` para decidir como desenhar.
  - Desenho de **polígonos** adicionado e, em seguida, evoluído para
    **formas prontas** por arraste (ver "Melhoria adicional" abaixo).
  - Código separado em módulos: classes de figura em `figuras.py`,
    interface e eventos em `linhasERabiscos.py`.

- [x] **Melhoria adicional (fora do enunciado formal)** — a ferramenta de
  polígono por clique-em-cada-vértice foi substituída por um submenu
  **Formas**, com Triângulo, Pentágono, Hexágono e Estrela prontos, que se
  ajustam à caixa delimitadora arrastada — igual ao galeria de "Formas" do
  Word. Adicionadas as classes `FormaRegular` (base para polígonos
  regulares de N lados) e `Estrela` em `figuras.py`.

- [ ] **Entrega 3** — a definir conforme o enunciado.
- [ ] **Entrega 4** (padrão *State*) — eliminação das condicionais por tipo de figura.
- [ ] **Entrega 5** — a definir conforme o enunciado.
- [ ] **Entrega 6** — a definir conforme o enunciado.
- [ ] **Entrega 7** — a definir conforme o enunciado.

## Como as figuras são representadas

Cada figura desenhada é uma instância de uma subclasse de `Figura`
(definidas em `figuras.py`):

```
Figura (abstrata)
├── FiguraDoisPontos (abstrata) — dois cantos: (x0, y0) e (x1, y1)
│   ├── Linha
│   ├── Retangulo
│   ├── Oval
│   ├── FormaRegular (abstrata) — polígono regular de N_LADOS, inscrito na caixa
│   │   ├── Triangulo   (N_LADOS = 3)
│   │   ├── Pentagono   (N_LADOS = 5)
│   │   └── Hexagono    (N_LADOS = 6)
│   └── Estrela          — 5 pontas, raio interno/externo alternado
└── Rabisco               — lista de pontos (traço à mão livre)
```

Toda figura sabe se desenhar (`desenhar(canvas, tracejado)`) e se ainda está
incompleta (`incompleta()`); o arquivo principal não precisa mais saber os
detalhes de cada tipo. As formas prontas (`FormaRegular` e `Estrela`) usam a
mesma lógica de "dois cantos" de `Retangulo`/`Oval`: os vértices são
recalculados a partir da caixa delimitadora sempre que a figura é desenhada.
As cores de borda e preenchimento são fixadas no momento em que a figura é
criada, então trocar a cor selecionada na interface não altera figuras já
desenhadas.

## Créditos

- Exercício original: Dr. Giovanny Fernando Lucero Palma.
- Adaptação para a turma T05 (2026/1): Prof. Dr. André Yoshiaki Kashiwabara — DCOMP/UFS.
