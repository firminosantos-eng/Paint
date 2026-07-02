
from paint.controlador.estado_ferramenta import ESTADOS_FERRAMENTA
from paint.modelo.repositorio_desenho import RepositorioDesenho

FERRAMENTA_INICIAL = "Linha"


class ControladorDesenho:
    def __init__(self, desenho, view):
        self.desenho = desenho
        self.view = view
        self._repositorio = RepositorioDesenho()

        self.figura_nova = None
        self.cor_borda_atual = "black"
        self.cor_preenchimento_atual = ""
        self.estado_atual = ESTADOS_FERRAMENTA[FERRAMENTA_INICIAL]


    def selecionar_ferramenta(self, nome_ferramenta):
        self.estado_atual = ESTADOS_FERRAMENTA[nome_ferramenta]

    def definir_cor_borda(self, cor):
        self.cor_borda_atual = cor

    def definir_cor_preenchimento(self, cor):
        self.cor_preenchimento_atual = cor


    def ao_pressionar_botao(self, x, y):
        self.estado_atual.ao_pressionar(self, x, y)

    def ao_arrastar(self, x, y):
        self.estado_atual.ao_arrastar(self, x, y)

    def ao_soltar_botao(self, x, y):
        self.estado_atual.ao_soltar(self, x, y)


    def desfazer(self):
        self.desenho.desfazer()
        self.atualizar_view()

    def salvar(self, caminho):
        self._repositorio.salvar(self.desenho, caminho)

    def abrir(self, caminho):
        self._repositorio.carregar(self.desenho, caminho)
        self.figura_nova = None
        self.atualizar_view()


    def atualizar_view(self):
        self.view.atualizar(self.desenho, self.figura_nova)
