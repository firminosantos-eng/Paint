"""
Modelo (Model): hierarquia de classes `Figura`.

Entrega 3 (tag mvc.3): estas classes fazem parte do Model no padrão MVC.
Não dependem de Tkinter — cada figura só conhece a própria geometria e
oferece `descricao_desenho()`, que a View usa para saber o que desenhar,
sem que o Model precise conhecer a API do Canvas. Isso também deixa o
Model testável sem precisar de uma janela gráfica (ver Entrega 4).
"""

import math
from abc import ABC, abstractmethod


class Figura(ABC):
    """Classe-base abstrata para todas as figuras do Paint."""

    def __init__(self, cor_borda, cor_preenchimento):
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

    @abstractmethod
    def incompleta(self):
        """True se a figura ainda não pode ser incluída no Desenho
        (ex.: comprimento/área zero, poucos pontos)."""
        raise NotImplementedError

    @abstractmethod
    def descricao_desenho(self):
        """Retorna (primitivo, pontos):
          primitivo -> "linha" | "retangulo" | "oval" | "poligono"
          pontos    -> coordenadas necessárias para desenhar esse primitivo

        A View usa essa descrição para decidir qual comando do Canvas
        chamar, sem que o Model precise saber nada sobre Tkinter.
        """
        raise NotImplementedError


class FiguraDoisPontos(Figura):
    """Base para figuras definidas por dois cantos: linha, retângulo,
    oval e as formas prontas (que se ajustam à caixa delimitadora)."""

    def __init__(self, x, y, cor_borda, cor_preenchimento):
        super().__init__(cor_borda, cor_preenchimento)
        self.x0, self.y0 = x, y
        self.x1, self.y1 = x, y

    def atualizar(self, x, y):
        """Atualiza o segundo canto da figura (chamado durante o arraste)."""
        self.x1, self.y1 = x, y

    def incompleta(self):
        return (self.x0, self.y0) == (self.x1, self.y1)

    def _centro_e_raios(self):
        cx = (self.x0 + self.x1) / 2
        cy = (self.y0 + self.y1) / 2
        rx = abs(self.x1 - self.x0) / 2
        ry = abs(self.y1 - self.y0) / 2
        return cx, cy, rx, ry


class Linha(FiguraDoisPontos):
    def descricao_desenho(self):
        return "linha", [(self.x0, self.y0), (self.x1, self.y1)]


class Retangulo(FiguraDoisPontos):
    def descricao_desenho(self):
        return "retangulo", (self.x0, self.y0, self.x1, self.y1)


class Oval(FiguraDoisPontos):
    def descricao_desenho(self):
        return "oval", (self.x0, self.y0, self.x1, self.y1)


class FormaRegular(FiguraDoisPontos):
    """Base para formas prontas com N lados iguais, inscritas na caixa
    delimitadora — como no galeria de "Formas" do Word. Subclasses só
    precisam definir `N_LADOS`."""

    N_LADOS = None
    ANGULO_INICIAL = -90  # graus; -90 deixa o primeiro vértice apontando para cima

    def _vertices(self):
        cx, cy, rx, ry = self._centro_e_raios()
        return _vertices_regulares(cx, cy, rx, ry, self.N_LADOS, self.ANGULO_INICIAL)

    def descricao_desenho(self):
        return "poligono", self._vertices()


class Triangulo(FormaRegular):
    N_LADOS = 3


class Pentagono(FormaRegular):
    N_LADOS = 5


class Hexagono(FormaRegular):
    N_LADOS = 6


class Estrela(FiguraDoisPontos):
    """Estrela de 5 pontas, inscrita na caixa delimitadora."""

    PONTAS = 5
    PROPORCAO_INTERNA = 0.45  # raio dos vértices "internos" em relação ao externo

    def descricao_desenho(self):
        cx, cy, rx, ry = self._centro_e_raios()
        n = self.PONTAS * 2
        passo = 360 / n
        vertices = []
        for i in range(n):
            escala = 1.0 if i % 2 == 0 else self.PROPORCAO_INTERNA
            angulo = math.radians(-90 + i * passo)
            vertices.append((cx + math.cos(angulo) * rx * escala,
                              cy + math.sin(angulo) * ry * escala))
        return "poligono", vertices


class Rabisco(Figura):
    """Traço à mão livre: sequência de pontos conectados por segmentos."""

    def __init__(self, x, y, cor_borda, cor_preenchimento):
        super().__init__(cor_borda, cor_preenchimento)
        self.pontos = [(x, y)]

    def atualizar(self, x, y):
        self.pontos.append((x, y))

    def incompleta(self):
        return len(self.pontos) <= 1

    def descricao_desenho(self):
        return "linha", list(self.pontos)


def _vertices_regulares(cx, cy, rx, ry, n_lados, angulo_inicial_graus):
    """Calcula os vértices de um polígono regular de `n_lados`, inscrito
    numa elipse de centro (cx, cy) e raios (rx, ry)."""
    passo = 360 / n_lados
    vertices = []
    for i in range(n_lados):
        angulo = math.radians(angulo_inicial_graus + i * passo)
        vertices.append((cx + math.cos(angulo) * rx, cy + math.sin(angulo) * ry))
    return vertices


# Mapeia o nome da ferramenta (usado pela View) à classe correspondente.
CLASSES_FIGURA = {
    "Linha": Linha,
    "Rabisco": Rabisco,
    "Retangulo": Retangulo,
    "Oval": Oval,
    "Triangulo": Triangulo,
    "Pentagono": Pentagono,
    "Hexagono": Hexagono,
    "Estrela": Estrela,
}

# Formas que aparecem agrupadas no submenu "Formas" da View.
FORMAS_PRONTAS = ["Triangulo", "Pentagono", "Hexagono", "Estrela"]
