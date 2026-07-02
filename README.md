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
python 01-linha.py
python 02-linhas.py
```

**Ferramentas disponíveis:** Linha, Rabisco, Retângulo, Oval, e um submenu
**Formas** com figuras prontas (Triângulo, Pentágono, Hexágono, Estrela).
Todas funcionam por clique e arraste: você desenha uma caixa delimitadora e
a figura se ajusta a ela.

**Outras ações:** `Ctrl+Z` (ou o botão "Desfazer") remove a última figura
incluída. **Salvar** (`Ctrl+S`) grava o desenho atual num arquivo `.json`;
**Abrir** (`Ctrl+O`) carrega um desenho salvo anteriormente.

**Selecionar e editar (Entrega 5):** com a ferramenta **Selecionar**, clique
numa figura para selecioná-la, `Ctrl+clique` para adicionar/remover da
seleção, ou clique e arraste numa área vazia para selecionar por retângulo
(seleciona as figuras totalmente dentro da área). Com algo selecionado:

- **Mover**: clique numa figura selecionada e arraste.
- **Apagar**: `Delete`/`Backspace` ou o botão "Apagar".
- **Copiar/Colar**: `Ctrl+C` / `Ctrl+V` — cola uma cópia deslocada, já selecionada.
- **Mover para frente/trás**: botões "Trazer para frente" / "Enviar para trás".
- **Mudar cores**: os botões "Cor da borda" / "Cor de preenchimento" aplicam
  a nova cor diretamente às figuras selecionadas (em vez de só definir a cor
  da próxima figura a ser desenhada).
- Tudo isso funciona com **seleção múltipla**.

## Como rodar os testes

Os testes cobrem só o Modelo (`Figura` e `Desenho`) — não precisam de
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
├── requirements-dev.txt
├── executar.py
├── 01-linha.py
├── 02-linhas.py
├── tests/
│   ├── conftest.py
│   ├── test_figura_geometria.py
│   ├── test_serializacao.py
│   └── test_desenho.py
└── src/
    └── paint/
        ├── main.py
        ├── modelo/
        │   ├── figura.py
        │   ├── desenho.py
        │   └── repositorio_desenho.py
        ├── visao/
        │   └── janela.py
        └── controlador/
            ├── controlador_desenho.py
            ├── estado_ferramenta.py
            └── estado_selecao.py
```

## Arquitetura MVC

| Camada     | Classe(s)                          | Responsabilidade                                                                 |
|------------|-------------------------------------|-----------------------------------------------------------------------------------|
| **Modelo**      | `Figura` e subclasses (`figura.py`) | Geometria e regras de cada tipo de figura, mover, clique/seleção e serialização. **Não depende de Tkinter.** |
| **Modelo**      | `Desenho` (`desenho.py`)            | Coleção de figuras: incluir, remover, desfazer, limpar, reordenar (z-order), buscar por ponto/área, serializar. |
| **Modelo**      | `RepositorioDesenho` (`repositorio_desenho.py`) | Lê/escreve o `Desenho` em disco (JSON) — só o "envelope" do arquivo, não o formato de cada figura. |
| **Visão**       | `Janela` (`janela.py`)              | Monta a interface Tkinter, desenha o estado do Modelo no Canvas (inclusive seleção), encaminha eventos ao controlador. |
| **Controlador** | `ControladorDesenho` (`controlador_desenho.py`) | Recebe os eventos da visão, delega ao Estado (ferramenta) atual, mantém a seleção e a área de transferência, aciona o `RepositorioDesenho`, manda a visão se redesenhar. |
| **Controlador** | `EstadoFerramenta` e subclasses (`estado_ferramenta.py`, `estado_selecao.py`) | Padrão *State*: cada ferramenta (Linha, Retângulo, Selecionar, ...) é um estado que sabe reagir aos eventos de mouse. |

O fluxo de uma interação é sempre o mesmo:

```
usuário → visão (evento de mouse/menu) → controlador → Modelo (Desenho/Figura)
                                              ↓
                                        visão.atualizar(...)
```

visão e Modelo nunca conversam diretamente entre si — toda comunicação passa
pelo controlador. Isso é o que torna o Modelo testável sem precisar de uma
janela gráfica: cada `Figura` não desenha em um Canvas diretamente, ela só
descreve a si mesma (`descricao_desenho()`), e é a `Janela` quem traduz essa
descrição para comandos do Tkinter.

## Padrão State

Antes, o controlador decidia qual classe de `Figura` instanciar com um
`if tipo == "Linha": ... elif tipo == "Retangulo": ...`. Agora essa decisão
virou um objeto: a ferramenta selecionada é um `EstadoFerramenta`, guardado
em `ControladorDesenho.estado_atual`. O controlador não pergunta mais "qual
ferramenta é essa?" — ele só repassa os três eventos de mouse para o estado:

```python
def ao_pressionar_botao(self, x, y, ctrl=False):
    self.estado_atual.ao_pressionar(self, x, y, ctrl)
```

As oito ferramentas de desenho (Linha, Rabisco, Retângulo, Oval, Triângulo,
Pentágono, Hexágono, Estrela) têm o mesmo comportamento — criar uma figura
no clique, atualizá-la no arraste, incluí-la no Modelo ao soltar —, então
essa lógica mora uma única vez em `EstadoDesenharFigura`; cada estado
nomeado (`EstadoLinha`, `EstadoOval`, ...) só indica qual classe de `Figura`
instanciar. A ferramenta **Selecionar** (`EstadoSelecao`, Entrega 5) é um
estado à parte, com sua própria lógica de clique/seleção/arraste. Trocar de
ferramenta no menu chama `controlador.selecionar_ferramenta(nome)`, que
troca `estado_atual` — sem nenhum condicional por tipo.

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
  - **Modelo**: `Figura`/subclasses (geometria pura, sem Tkinter) e `Desenho`
    (coleção de figuras, com `incluir`/`desfazer`/`limpar`).
  - **visão**: classe `Janela`, única responsável por widgets Tkinter e por
    traduzir `descricao_desenho()` em comandos do Canvas.
  - **controlador**: classe única `ControladorDesenho`, com um método por
    evento (`ao_pressionar_botao`, `ao_arrastar`, `ao_soltar_botao`,
    `desfazer`, `definir_cor_borda`, `definir_cor_preenchimento`).
  - Como consequência da separação, o Modelo passou a ser testável sem
    depender de uma janela gráfica — a base para a Entrega 4.

- [x] **Entrega 4** (tag `state-testes.4`) — Padrão State, persistência e testes:
  - **State**: `EstadoFerramenta` (`estado_ferramenta.py`) elimina os
    últimos condicionais por tipo de figura/ferramenta no controlador — a
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

- [x] **Entrega 5** (tag `selecao.5`) — Manipulação de figuras já desenhadas:
  - Nova ferramenta **Selecionar** (`EstadoSelecao`): clique seleciona uma
    figura, `Ctrl+clique` alterna a seleção (multi-seleção), clique e
    arraste numa área vazia faz seleção por retângulo elástico.
  - **Mover** figura(s) selecionada(s) por arraste (`Figura.mover(dx, dy)`,
    implementado em todas as subclasses).
  - **Apagar** (`Delete`/`Backspace`), **Copiar/Colar** (`Ctrl+C`/`Ctrl+V`,
    reaproveitando `para_dict()`/`figura_de_dict()` da Entrega 4 para
    clonar), **mover para frente/trás** (`Desenho.mover_para_frente` /
    `mover_para_tras`, reordenando a lista interna) e **mudar cores** das
    figuras selecionadas (os botões de cor passam a agir sobre a seleção
    quando ela não está vazia).
  - Tudo funciona com **seleção múltipla** (lista `selecionadas` no
    controlador), incluindo mover, apagar, copiar/colar e mudar cores de
    várias figuras de uma vez.
  - Novos métodos do Modelo, usados pela seleção: `Desenho.remover`,
    `figura_no_ponto`, `figuras_na_area`, e `Figura.esta_dentro_da_area`
    (reaproveita `descricao_desenho()`, no mesmo espírito de
    `contem_ponto`).
  - Testes novos em `tests/test_desenho.py`, cobrindo remoção, z-order e
    busca por ponto/área.
  - **Nota de processo**: o enunciado pede que as tarefas desta entrega
    sejam divididas entre os integrantes do grupo, com commits individuais
    de cada aluno no GitHub — isso é organização de equipe, não algo que
    o código em si expresse; fica registrado aqui como lembrete pra quando
    vocês forem dividir o trabalho e abrir os PRs/commits.

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
própria geometria (`descricao_desenho()`), sabe se mover (`mover(dx, dy)`),
sabe responder se um ponto está sobre ela (`contem_ponto(x, y)`) ou se está
totalmente dentro de uma área (`esta_dentro_da_area(...)`, usada na seleção
por retângulo) e sabe se converter para/de dicionário (`para_dict()` /
`ClasseFigura.de_dict(...)`) — nada disso depende de Tkinter. A `Janela`
(visão) só traduz `descricao_desenho()` para comandos do Canvas; o
`RepositorioDesenho` só grava/lê o JSON resultante de `para_dict()`. As
cores de borda e preenchimento ficam guardadas na própria figura, então o
controlador pode alterá-las diretamente quando a figura está selecionada.



## Créditos

- Exercício original: Dr. Giovanny Fernando Lucero Palma.
- Adaptação para a turma T05 (2026/1): Prof. Dr. André Yoshiaki Kashiwabara — DCOMP/UFS.
