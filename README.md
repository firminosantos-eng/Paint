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
- `pytest` (opcional, só para rodar os testes automatizados — veja
  "Como rodar os testes" abaixo).

Para conferir se o Tkinter está disponível:

```bash
python -m tkinter
```

## Como executar

A partir da Entrega 3, o programa principal segue a arquitetura MVC e mora
em `src/paint/`. Duas formas de rodar, a partir da raiz do projeto:

```bash
# Opção 1: atalho pronto (não precisa mexer no PYTHONPATH)
python executar.py

# Opção 2: rodando o pacote diretamente
cd src
python -m paint.main
```

Os scripts de referência das entregas anteriores continuam na raiz, cada
um abrindo sua própria janela:

```bash
python 01-linha.py   # desenha uma única linha (apaga a anterior)
python 02-linhas.py  # acumula várias linhas
```

**Ferramentas disponíveis:** Linha, Rabisco, Retângulo, Oval, e um submenu
**Formas** com figuras prontas (Triângulo, Pentágono, Hexágono, Estrela).
Todas funcionam por clique e arraste: você desenha uma caixa delimitadora e
a figura se ajusta a ela.

**Outras ações:** `Ctrl+Z` (ou o botão "Desfazer") remove a última figura
incluída. **Salvar** (`Ctrl+S`) grava o desenho atual num arquivo `.json`;
**Abrir** (`Ctrl+O`) carrega um desenho salvo anteriormente.

## Como rodar os testes

Os testes cobrem só o Model (`Figura` e `Desenho`) — não precisam de
display gráfico, então rodam em qualquer ambiente, inclusive CI.

```bash
pip install -r requirements-dev.txt
pytest
```

## Estrutura de pastas

```
projeto-paint/
├── .gitignore
├── README.md
├── requirements-dev.txt   # dependências só para rodar os testes (pytest)
├── executar.py            # atalho para rodar sem mexer no PYTHONPATH
├── 01-linha.py             # referência: uma única linha por vez
├── 02-linhas.py            # referência: várias linhas acumuladas
├── tests/                  # testes automatizados do Model
│   ├── conftest.py
│   ├── test_figura_geometria.py
│   └── test_serializacao.py
└── src/
    └── paint/              # pacote Python do projeto
        ├── main.py         # monta Model + View + Controller e inicia o app
        ├── modelo/
        │   ├── figura.py               # hierarquia de classes Figura
        │   ├── desenho.py              # classe Desenho (coleção de figuras)
        │   └── repositorio_desenho.py  # leitura/escrita em disco (JSON)
        ├── visao/
        │   └── janela.py   # classe Janela — interface Tkinter
        └── controlador/
            ├── controlador_desenho.py  # classe ControladorDesenho
            └── estado_ferramenta.py    # padrão State (uma classe por ferramenta)
```

## Arquitetura MVC

| Camada     | Classe(s)                          | Responsabilidade                                                                 |
|------------|-------------------------------------|-----------------------------------------------------------------------------------|
| **Model**      | `Figura` e subclasses (`figura.py`) | Geometria e regras de cada tipo de figura, clique/seleção e serialização. **Não depende de Tkinter.** |
| **Model**      | `Desenho` (`desenho.py`)            | Coleção de figuras concluídas: incluir, desfazer, limpar, serializar a coleção.   |
| **Model**      | `RepositorioDesenho` (`repositorio_desenho.py`) | Lê/escreve o `Desenho` em disco (JSON) — só o "envelope" do arquivo, não o formato de cada figura. |
| **View**       | `Janela` (`janela.py`)              | Monta a interface Tkinter, desenha o estado do Model no Canvas, encaminha eventos ao Controller. |
| **Controller** | `ControladorDesenho` (`controlador_desenho.py`) | Recebe os eventos da View, delega ao Estado (ferramenta) atual, aciona o `RepositorioDesenho`, manda a View se redesenhar. |
| **Controller** | `EstadoFerramenta` e subclasses (`estado_ferramenta.py`) | Padrão *State*: cada ferramenta (Linha, Retângulo, ...) é um estado que sabe reagir aos eventos de mouse. |

O fluxo de uma interação é sempre o mesmo:

```
usuário → View (evento de mouse/menu) → Controller → Model (Desenho/Figura)
                                              ↓
                                        View.atualizar(...)
```

View e Model nunca conversam diretamente entre si — toda comunicação passa
pelo Controller. Isso é o que torna o Model testável sem precisar de uma
janela gráfica: cada `Figura` não desenha em um Canvas diretamente, ela só
descreve a si mesma (`descricao_desenho()`), e é a `Janela` quem traduz essa
descrição para comandos do Tkinter.

## Padrão State (Entrega 4)

Antes, o Controller decidia qual classe de `Figura` instanciar com um
`if tipo == "Linha": ... elif tipo == "Retangulo": ...`. Agora essa decisão
virou um objeto: a ferramenta selecionada é um `EstadoFerramenta`, guardado
em `ControladorDesenho.estado_atual`. O Controller não pergunta mais "qual
ferramenta é essa?" — ele só repassa os três eventos de mouse para o estado:

```python
def ao_pressionar_botao(self, x, y):
    self.estado_atual.ao_pressionar(self, x, y)
```

Como as oito ferramentas atuais (Linha, Rabisco, Retângulo, Oval, Triângulo,
Pentágono, Hexágono, Estrela) têm o mesmo comportamento — criar uma figura
no clique, atualizá-la no arraste, incluí-la no Model ao soltar —, essa
lógica mora uma única vez em `EstadoDesenharFigura`; cada estado nomeado
(`EstadoLinha`, `EstadoOval`, ...) só indica qual classe de `Figura`
instanciar. Trocar de ferramenta no menu chama
`controlador.selecionar_ferramenta(nome)`, que troca `estado_atual` — sem
nenhum condicional por tipo.

## Progresso das entregas

- [x] **Entrega 1** (tag `imperativa.1`) — Familiarização com Tkinter e com o
  fluxo Git/GitHub da equipe. Partindo do esqueleto de linhas e rabiscos,
  foram adicionadas:
  - Desenho de **retângulos**.
  - Desenho de **ovais**.
  - **Cor de borda** configurável por figura.
  - **Cor de preenchimento** configurável por figura.

  Implementação em estilo imperativo (`if tipo == "..."`), como esperado
  nesta etapa.

- [x] **Entrega 2** (tag `orientadoaobjetos.2`) — Substituição do código
  imperativo por modelagem Orientada a Objetos:
  - Hierarquia de classes `Figura`: `Figura` (abstrata) → `FiguraDoisPontos`
    (linha, retângulo, oval, formas prontas) e, direto de `Figura`, `Rabisco`.
  - Programa adequado para usar a hierarquia via polimorfismo, sem mais
    nenhum `if tipo == "..."` para decidir como desenhar.
  - Código separado em módulos (classes de figura x interface).

- [x] **Melhoria adicional (fora do enunciado formal)** — a ferramenta de
  polígono por clique-em-cada-vértice foi substituída por um submenu
  **Formas**, com Triângulo, Pentágono, Hexágono e Estrela prontos, que se
  ajustam à caixa delimitadora arrastada — igual ao galeria de "Formas" do
  Word.

- [x] **Entrega 3** (tag `mvc.3`) — Separação de responsabilidades com MVC:
  - Projeto reorganizado na estrutura de pastas recomendada
    (`src/paint/{modelo,visao,controlador}`, `tests/`).
  - **Model**: `Figura`/subclasses (geometria pura, sem Tkinter) e `Desenho`
    (coleção de figuras, com `incluir`/`desfazer`/`limpar`).
  - **View**: classe `Janela`, única responsável por widgets Tkinter e por
    traduzir `descricao_desenho()` em comandos do Canvas.
  - **Controller**: classe única `ControladorDesenho`, com um método por
    evento (`ao_pressionar_botao`, `ao_arrastar`, `ao_soltar_botao`,
    `desfazer`, `definir_cor_borda`, `definir_cor_preenchimento`).
  - Como consequência da separação, o Model passou a ser testável sem
    depender de uma janela gráfica — a base para a Entrega 4.

- [x] **Entrega 4** (tag `state-testes.4`) — Padrão State, persistência e testes:
  - **State**: `EstadoFerramenta` (`estado_ferramenta.py`) elimina os
    últimos condicionais por tipo de figura/ferramenta no Controller — a
    ferramenta selecionada agora é um objeto, não uma string comparada em
    cadeia de `if`.
  - **Salvar/Abrir**: formato JSON. Cada `Figura` sabe se converter para
    dicionário (`para_dict()`) e reconstruir a si mesma
    (`ClasseFigura.de_dict(...)`, despachado por `figura_de_dict()`); o
    `RepositorioDesenho` só lê/escreve o arquivo.
  - **`contem_ponto(x, y)`** adicionado à `Figura` — detecção de
    clique/seleção, implementada de forma genérica em cima de
    `descricao_desenho()` (usado só pelos testes por enquanto).
  - **Testes automatizados** em `tests/`, cobrindo geometria (criação,
    mover, clique/seleção) e serialização (round-trip e ciclo Salvar/Abrir)
    — 18 testes, todos passando.

- [ ] **Entrega 5** — a definir conforme o enunciado.
- [ ] **Entrega 6** (padrão *Composite*) — a definir conforme o enunciado; testes de `tests/` devem crescer junto.
- [ ] **Entrega 7** (padrão *Command*) — a definir conforme o enunciado; testes de `tests/` devem crescer junto.

## Como as figuras são representadas

Cada figura é uma instância de uma subclasse de `Figura`
(`src/paint/modelo/figura.py`):

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

Toda figura sabe se está incompleta (`incompleta()`), sabe descrever a
própria geometria (`descricao_desenho()`), sabe responder se um ponto está
sobre ela (`contem_ponto(x, y)`) e sabe se converter para/de dicionário
(`para_dict()` / `ClasseFigura.de_dict(...)`) — nada disso depende de
Tkinter. A `Janela` (View) só traduz `descricao_desenho()` para comandos do
Canvas; o `RepositorioDesenho` só grava/lê o JSON resultante de
`para_dict()`. As cores de borda e preenchimento são fixadas no momento em
que a figura é criada, então trocar a cor selecionada na interface não
altera figuras já desenhadas.

## Créditos

- Exercício original: Dr. Giovanny Fernando Lucero Palma.
- Adaptação para a turma T05 (2026/1): Prof. Dr. André Yoshiaki Kashiwabara — DCOMP/UFS.
