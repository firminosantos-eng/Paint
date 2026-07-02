
from paint.modelo.figura import figura_de_dict


class Desenho:

    def __init__(self):
        self._figuras = []

    def incluir(self, figura):
        if figura is not None and not figura.incompleta():
            self._figuras.append(figura)

    def desfazer(self):
        if self._figuras:
            self._figuras.pop()

    def limpar(self):
        self._figuras.clear()

    def para_lista_dict(self):
        return [figura.para_dict() for figura in self._figuras]

    def carregar_de_lista_dict(self, lista_dict):
        self._figuras = [figura_de_dict(dados) for dados in lista_dict]

    def __iter__(self):
        return iter(self._figuras)

    def __len__(self):
        return len(self._figuras)
