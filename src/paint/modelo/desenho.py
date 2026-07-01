"""
Modelo (Model): classe `Desenho`.

Representa a coleção de figuras já concluídas — o "documento" que está
sendo editado. Concentra as regras sobre a coleção (o que pode ser
incluído, como desfazer) para que View e Controller não precisem mexer
direto numa lista.
"""


class Desenho:
    """Guarda a lista de figuras concluídas e oferece as operações de
    alto nível sobre essa coleção."""

    def __init__(self):
        self._figuras = []

    def incluir(self, figura):
        """Inclui a figura na coleção, desde que ela não esteja
        incompleta (ex.: comprimento/área zero, poucos pontos)."""
        if figura is not None and not figura.incompleta():
            self._figuras.append(figura)

    def desfazer(self):
        """Remove a última figura incluída, se houver alguma."""
        if self._figuras:
            self._figuras.pop()

    def limpar(self):
        """Remove todas as figuras do desenho."""
        self._figuras.clear()

    def __iter__(self):
        return iter(self._figuras)

    def __len__(self):
        return len(self._figuras)
