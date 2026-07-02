from paint.modelo.figura import figura_de_dict


class Desenho:
    def __init__(self):
        self._figuras = []

    def incluir(self, figura):
        if figura is not None and not figura.incompleta():
            self._figuras.append(figura)

    def remover(self, figura):
        if figura in self._figuras:
            self._figuras.remove(figura)

    def desfazer(self):
        if self._figuras:
            self._figuras.pop()

    def limpar(self):
        self._figuras.clear()

    def mover_para_frente(self, figura):
        if figura in self._figuras:
            self._figuras.remove(figura)
            self._figuras.append(figura)

    def mover_para_tras(self, figura):
        if figura in self._figuras:
            self._figuras.remove(figura)
            self._figuras.insert(0, figura)

    def figura_no_ponto(self, x, y):
        for figura in reversed(self._figuras):
            if figura.contem_ponto(x, y):
                return figura
        return None

    def figuras_na_area(self, retangulo):
        x0, y0, x1, y1 = retangulo
        return [figura for figura in self._figuras if figura.esta_dentro_da_area(x0, y0, x1, y1)]

    def para_lista_dict(self):
        return [figura.para_dict() for figura in self._figuras]

    def carregar_de_lista_dict(self, lista_dict):
        self._figuras = [figura_de_dict(dados) for dados in lista_dict]

    def __iter__(self):
        return iter(self._figuras)

    def __len__(self):
        return len(self._figuras)
