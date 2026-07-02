import math
from abc import ABC, abstractmethod

TOLERANCIA_CLIQUE_LINHA = 4


class Figura(ABC):
    def __init__(self, cor_borda, cor_preenchimento):
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

    @abstractmethod
    def incompleta(self):
        raise NotImplementedError

    @abstractmethod
    def descricao_desenho(self):
        raise NotImplementedError

    @abstractmethod
    def para_dict(self):
        raise NotImplementedError

    @abstractmethod
    def mover(self, dx, dy):
        raise NotImplementedError

    def contem_ponto(self, x, y):
        primitivo, pontos = self.descricao_desenho()
        if primitivo == "linha":
            return _perto_de_alguma_aresta(x, y, pontos, TOLERANCIA_CLIQUE_LINHA)
        if primitivo == "retangulo":
            return _dentro_do_retangulo(x, y, pontos)
        if primitivo == "oval":
            return _dentro_da_elipse(x, y, pontos)
        if primitivo == "poligono":
            return _dentro_do_poligono(x, y, pontos)
        return False

    def esta_dentro_da_area(self, ax0, ay0, ax1, ay1):
        x_min, x_max = sorted((ax0, ax1))
        y_min, y_max = sorted((ay0, ay1))
        primitivo, pontos = self.descricao_desenho()
        if primitivo in ("retangulo", "oval"):
            coordenadas = [(pontos[0], pontos[1]), (pontos[2], pontos[3])]
        else:
            coordenadas = pontos
        return all(x_min <= px <= x_max and y_min <= py <= y_max for px, py in coordenadas)


class FiguraDoisPontos(Figura):
    def __init__(self, x, y, cor_borda, cor_preenchimento):
        super().__init__(cor_borda, cor_preenchimento)
        self.x0, self.y0 = x, y
        self.x1, self.y1 = x, y

    def atualizar(self, x, y):
        self.x1, self.y1 = x, y

    def mover(self, dx, dy):
        self.x0 += dx
        self.y0 += dy
        self.x1 += dx
        self.y1 += dy

    def incompleta(self):
        return (self.x0, self.y0) == (self.x1, self.y1)

    def _centro_e_raios(self):
        cx = (self.x0 + self.x1) / 2
        cy = (self.y0 + self.y1) / 2
        rx = abs(self.x1 - self.x0) / 2
        ry = abs(self.y1 - self.y0) / 2
        return cx, cy, rx, ry

    def para_dict(self):
        return {
            "tipo": type(self).__name__,
            "x0": self.x0, "y0": self.y0,
            "x1": self.x1, "y1": self.y1,
            "cor_borda": self.cor_borda,
            "cor_preenchimento": self.cor_preenchimento,
        }

    @classmethod
    def de_dict(cls, dados):
        figura = cls(dados["x0"], dados["y0"], dados["cor_borda"], dados["cor_preenchimento"])
        figura.atualizar(dados["x1"], dados["y1"])
        return figura


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
    N_LADOS = None
    ANGULO_INICIAL = -90

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
    PONTAS = 5
    PROPORCAO_INTERNA = 0.45

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
    def __init__(self, x, y, cor_borda, cor_preenchimento):
        super().__init__(cor_borda, cor_preenchimento)
        self.pontos = [(x, y)]

    def atualizar(self, x, y):
        self.pontos.append((x, y))

    def mover(self, dx, dy):
        self.pontos = [(x + dx, y + dy) for x, y in self.pontos]

    def incompleta(self):
        return len(self.pontos) <= 1

    def descricao_desenho(self):
        return "linha", list(self.pontos)

    def para_dict(self):
        return {
            "tipo": "Rabisco",
            "pontos": [list(ponto) for ponto in self.pontos],
            "cor_borda": self.cor_borda,
            "cor_preenchimento": self.cor_preenchimento,
        }

    @classmethod
    def de_dict(cls, dados):
        pontos = dados["pontos"]
        x0, y0 = pontos[0]
        figura = cls(x0, y0, dados["cor_borda"], dados["cor_preenchimento"])
        for x, y in pontos[1:]:
            figura.atualizar(x, y)
        return figura


def _vertices_regulares(cx, cy, rx, ry, n_lados, angulo_inicial_graus):
    passo = 360 / n_lados
    vertices = []
    for i in range(n_lados):
        angulo = math.radians(angulo_inicial_graus + i * passo)
        vertices.append((cx + math.cos(angulo) * rx, cy + math.sin(angulo) * ry))
    return vertices


def _distancia_ponto_segmento(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(px - x1, py - y1)
    t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    proj_x, proj_y = x1 + t * dx, y1 + t * dy
    return math.hypot(px - proj_x, py - proj_y)


def _perto_de_alguma_aresta(x, y, pontos, tolerancia):
    for (x1, y1), (x2, y2) in zip(pontos, pontos[1:]):
        if _distancia_ponto_segmento(x, y, x1, y1, x2, y2) <= tolerancia:
            return True
    return False


def _dentro_do_retangulo(x, y, pontos):
    x0, y0, x1, y1 = pontos
    x_min, x_max = sorted((x0, x1))
    y_min, y_max = sorted((y0, y1))
    return x_min <= x <= x_max and y_min <= y <= y_max


def _dentro_da_elipse(x, y, pontos):
    x0, y0, x1, y1 = pontos
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rx, ry = abs(x1 - x0) / 2, abs(y1 - y0) / 2
    if rx == 0 or ry == 0:
        return False
    return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1


def _dentro_do_poligono(x, y, vertices):
    dentro = False
    n = len(vertices)
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        cruza = ((y1 > y) != (y2 > y)) and \
            (x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1)
        if cruza:
            dentro = not dentro
    return dentro


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

FORMAS_PRONTAS = ["Triangulo", "Pentagono", "Hexagono", "Estrela"]


def figura_de_dict(dados):
    classe = CLASSES_FIGURA[dados["tipo"]]
    return classe.de_dict(dados)
