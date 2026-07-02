from abc import ABC, abstractmethod

from paint.modelo.figura import (
    Linha, Rabisco, Retangulo, Oval, Triangulo, Pentagono, Hexagono, Estrela,
)


class EstadoFerramenta(ABC):
    @abstractmethod
    def ao_pressionar(self, controlador, x, y, ctrl=False):
        raise NotImplementedError

    @abstractmethod
    def ao_arrastar(self, controlador, x, y, ctrl=False):
        raise NotImplementedError

    @abstractmethod
    def ao_soltar(self, controlador, x, y, ctrl=False):
        raise NotImplementedError


class EstadoDesenharFigura(EstadoFerramenta):
    CLASSE_FIGURA = None

    def ao_pressionar(self, controlador, x, y, ctrl=False):
        controlador.figura_nova = self.CLASSE_FIGURA(
            x, y, controlador.cor_borda_atual, controlador.cor_preenchimento_atual
        )
        controlador.atualizar_view()

    def ao_arrastar(self, controlador, x, y, ctrl=False):
        if controlador.figura_nova is not None:
            controlador.figura_nova.atualizar(x, y)
            controlador.atualizar_view()

    def ao_soltar(self, controlador, x, y, ctrl=False):
        if controlador.figura_nova is not None:
            controlador.desenho.incluir(controlador.figura_nova)
            controlador.figura_nova = None
        controlador.atualizar_view()


class EstadoLinha(EstadoDesenharFigura):
    CLASSE_FIGURA = Linha


class EstadoRabisco(EstadoDesenharFigura):
    CLASSE_FIGURA = Rabisco


class EstadoRetangulo(EstadoDesenharFigura):
    CLASSE_FIGURA = Retangulo


class EstadoOval(EstadoDesenharFigura):
    CLASSE_FIGURA = Oval


class EstadoTriangulo(EstadoDesenharFigura):
    CLASSE_FIGURA = Triangulo


class EstadoPentagono(EstadoDesenharFigura):
    CLASSE_FIGURA = Pentagono


class EstadoHexagono(EstadoDesenharFigura):
    CLASSE_FIGURA = Hexagono


class EstadoEstrela(EstadoDesenharFigura):
    CLASSE_FIGURA = Estrela
