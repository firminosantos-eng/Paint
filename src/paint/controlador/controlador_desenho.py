"""
Controlador (Controller): `ControladorDesenho`.

Recebe os eventos encaminhados pela View (clique, arraste, soltar,
desfazer, troca de cor), decide o que fazer com o Model (`Desenho`) e
pede para a View se redesenhar. A View e o Model não conversam
diretamente entre si — toda a orquestração passa por aqui.

Nesta entrega há um único Controller, com um método por evento. Um
Controller por ferramenta (mais próximo de Strategy/State) é o próximo
passo natural, adiado para a Entrega 4.
"""

from paint.modelo.figura import CLASSES_FIGURA


class ControladorDesenho:
    def __init__(self, desenho, view):
        self.desenho = desenho
        self.view = view

        self.figura_nova = None
        self.cor_borda_atual = "black"
        self.cor_preenchimento_atual = ""

    # -----------------------------------------------------------------
    # Cores
    # -----------------------------------------------------------------

    def definir_cor_borda(self, cor):
        self.cor_borda_atual = cor

    def definir_cor_preenchimento(self, cor):
        self.cor_preenchimento_atual = cor

    # -----------------------------------------------------------------
    # Eventos de mouse
    # -----------------------------------------------------------------

    def ao_pressionar_botao(self, tipo_ferramenta, x, y):
        classe = CLASSES_FIGURA[tipo_ferramenta]
        self.figura_nova = classe(x, y, self.cor_borda_atual, self.cor_preenchimento_atual)
        self._atualizar_view()

    def ao_arrastar(self, x, y):
        if self.figura_nova is not None:
            self.figura_nova.atualizar(x, y)
            self._atualizar_view()

    def ao_soltar_botao(self, x, y):
        if self.figura_nova is not None:
            self.desenho.incluir(self.figura_nova)
            self.figura_nova = None
        self._atualizar_view()

    # -----------------------------------------------------------------
    # Outras ações
    # -----------------------------------------------------------------

    def desfazer(self):
        self.desenho.desfazer()
        self._atualizar_view()

    # -----------------------------------------------------------------

    def _atualizar_view(self):
        self.view.atualizar(self.desenho, self.figura_nova)
