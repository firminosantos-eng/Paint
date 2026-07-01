

import math
from abc import ABC, abstractmethod


class Figura(ABC):
    """Classe-base abstrata para todas as figuras do Paint."""

    def __init__(self, cor_borda, cor_preenchimento):
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

    @abstractmethod
    def desenhar(self, canvas, tracejado=False):
        raise NotImplementedError

    @abstractmethod
    def incompleta(self):
        raise NotImplementedError

    def _opcoes_traco(self, tracejado):
        return {"dash": (4, 2)} if tracejado else {}


class FiguraDoisPontos(Figura):
    def __init__(self, x, y, cor_borda, cor_preenchimento):
        super().__init__(cor_borda, cor_preenchimento)
        self.x0, self.y0 = x, y
        self.x1, self.y1 = x, y

    def atualizar(self, x, y):
        self.x1, self.y1 = x, y

    def incompleta(self):
        return (self.x0, self.y0) == (self.x1, self.y1)


class Linha(FiguraDoisPontos):
    def desenhar(self, canvas, tracejado=False):
        canvas.create_line(self.x0, self.y0, self.x1, self.y1,
                            fill=self.cor_borda, **self._opcoes_traco(tracejado))


class Retangulo(FiguraDoisPontos):
    def desenhar(self, canvas, tracejado=False):
        canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1,
                                 outline=self.cor_borda, fill=self.cor_preenchimento,
                                 **self._opcoes_traco(tracejado))


class Oval(FiguraDoisPontos):
    def desenhar(self, canvas, tracejado=False):
        canvas.create_oval(self.x0, self.y0, self.x1, self.y1,
                            outline=self.cor_borda, fill=self.cor_preenchimento,
                            **self._opcoes_traco(tracejado))


class Rabisco(Figura):

    def __init__(self, x, y, cor_borda, cor_preenchimento):
        super().__init__(cor_borda, cor_preenchimento)
        self.pontos = [(x, y)]

    def atualizar(self, x, y):
        self.pontos.append((x, y))

    def incompleta(self):
        return len(self.pontos) <= 1

    def desenhar(self, canvas, tracejado=False):
        if len(self.pontos) >= 2:
            canvas.create_line(self.pontos, fill=self.cor_borda,
                                **self._opcoes_traco(tracejado))


class FormaRegular(FiguraDoisPontos):

    N_LADOS = None          # definido pelas subclasses
    ANGULO_INICIAL = -90    # graus; -90 deixa o primeiro vértice apontando para cima

    def _centro_e_raios(self):
        cx = (self.x0 + self.x1) / 2
        cy = (self.y0 + self.y1) / 2
        rx = abs(self.x1 - self.x0) / 2
        ry = abs(self.y1 - self.y0) / 2
        return cx, cy, rx, ry

    def _vertices(self):
        cx, cy, rx, ry = self._centro_e_raios()
        return _vertices_regulares(cx, cy, rx, ry, self.N_LADOS, self.ANGULO_INICIAL)

    def desenhar(self, canvas, tracejado=False):
        canvas.create_polygon(self._vertices(), outline=self.cor_borda,
                               fill=self.cor_preenchimento,
                               **self._opcoes_traco(tracejado))


class Triangulo(FormaRegular):
    N_LADOS = 3


class Pentagono(FormaRegular):
    N_LADOS = 5


class Hexagono(FormaRegular):
    N_LADOS = 6


class Estrela(FiguraDoisPontos):

    PONTAS = 5
    PROPORCAO_INTERNA = 0.45  # raio dos vértices "internos" em relação ao externo

    def desenhar(self, canvas, tracejado=False):
        cx = (self.x0 + self.x1) / 2
        cy = (self.y0 + self.y1) / 2
        rx = abs(self.x1 - self.x0) / 2
        ry = abs(self.y1 - self.y0) / 2

        n = self.PONTAS * 2
        passo = 360 / n
        vertices = []
        for i in range(n):
            escala = 1.0 if i % 2 == 0 else self.PROPORCAO_INTERNA
            angulo = math.radians(-90 + i * passo)
            vertices.append((cx + math.cos(angulo) * rx * escala,
                              cy + math.sin(angulo) * ry * escala))

        canvas.create_polygon(vertices, outline=self.cor_borda,
                               fill=self.cor_preenchimento,
                               **self._opcoes_traco(tracejado))


def _vertices_regulares(cx, cy, rx, ry, n_lados, angulo_inicial_graus):
    passo = 360 / n_lados
    vertices = []
    for i in range(n_lados):
        angulo = math.radians(angulo_inicial_graus + i * passo)
        vertices.append((cx + math.cos(angulo) * rx, cy + math.sin(angulo) * ry))
    return vertices


# Mapeia o texto exibido no menu de ferramentas para a classe correspondente.
# Usado pelo arquivo principal como "fábrica" de figuras.
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

# Formas do submenu "Formas" (todas ajustadas por arraste, como no Word).
FORMAS_PRONTAS = ["Triangulo", "Pentagono", "Hexagono", "Estrela"]
