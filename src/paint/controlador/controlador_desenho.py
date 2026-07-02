from paint.controlador.estado_ferramenta import (
    EstadoLinha, EstadoRabisco, EstadoRetangulo, EstadoOval,
    EstadoTriangulo, EstadoPentagono, EstadoHexagono, EstadoEstrela,
)
from paint.controlador.estado_selecao import EstadoSelecao
from paint.modelo.figura import figura_de_dict
from paint.modelo.repositorio_desenho import RepositorioDesenho

ESTADOS_FERRAMENTA = {
    "Selecionar": EstadoSelecao(),
    "Linha": EstadoLinha(),
    "Rabisco": EstadoRabisco(),
    "Retangulo": EstadoRetangulo(),
    "Oval": EstadoOval(),
    "Triangulo": EstadoTriangulo(),
    "Pentagono": EstadoPentagono(),
    "Hexagono": EstadoHexagono(),
    "Estrela": EstadoEstrela(),
}

FERRAMENTA_INICIAL = "Linha"

DESLOCAMENTO_COLAR = 20


class ControladorDesenho:
    def __init__(self, desenho, view):
        self.desenho = desenho
        self.view = view
        self._repositorio = RepositorioDesenho()

        self.figura_nova = None
        self.cor_borda_atual = "black"
        self.cor_preenchimento_atual = ""
        self.estado_atual = ESTADOS_FERRAMENTA[FERRAMENTA_INICIAL]

        self.selecionadas = []
        self.retangulo_selecao_atual = None
        self._area_transferencia = []

    def selecionar_ferramenta(self, nome_ferramenta):
        self.estado_atual = ESTADOS_FERRAMENTA[nome_ferramenta]

    def definir_cor_borda(self, cor):
        self.cor_borda_atual = cor
        if self.selecionadas:
            for figura in self.selecionadas:
                figura.cor_borda = cor
            self.atualizar_view()

    def definir_cor_preenchimento(self, cor):
        self.cor_preenchimento_atual = cor
        if self.selecionadas:
            for figura in self.selecionadas:
                figura.cor_preenchimento = cor
            self.atualizar_view()

    def ao_pressionar_botao(self, x, y, ctrl=False):
        self.estado_atual.ao_pressionar(self, x, y, ctrl)

    def ao_arrastar(self, x, y, ctrl=False):
        self.estado_atual.ao_arrastar(self, x, y, ctrl)

    def ao_soltar_botao(self, x, y, ctrl=False):
        self.estado_atual.ao_soltar(self, x, y, ctrl)

    def definir_selecao(self, figuras):
        self.selecionadas = list(figuras)
        self.atualizar_view()

    def alternar_selecao(self, figura):
        if figura in self.selecionadas:
            self.selecionadas.remove(figura)
        else:
            self.selecionadas.append(figura)
        self.atualizar_view()

    def deletar_selecionadas(self):
        for figura in self.selecionadas:
            self.desenho.remover(figura)
        self.selecionadas = []
        self.atualizar_view()

    def copiar_selecionadas(self):
        self._area_transferencia = [figura.para_dict() for figura in self.selecionadas]

    def colar(self):
        novas = []
        for dados in self._area_transferencia:
            nova = figura_de_dict(dados)
            nova.mover(DESLOCAMENTO_COLAR, DESLOCAMENTO_COLAR)
            self.desenho.incluir(nova)
            novas.append(nova)
        if novas:
            self.selecionadas = novas
            self.atualizar_view()

    def trazer_para_frente(self):
        for figura in self.selecionadas:
            self.desenho.mover_para_frente(figura)
        self.atualizar_view()

    def enviar_para_tras(self):
        for figura in reversed(self.selecionadas):
            self.desenho.mover_para_tras(figura)
        self.atualizar_view()

    def desfazer(self):
        self.desenho.desfazer()
        self.atualizar_view()

    def salvar(self, caminho):
        self._repositorio.salvar(self.desenho, caminho)

    def abrir(self, caminho):
        self._repositorio.carregar(self.desenho, caminho)
        self.figura_nova = None
        self.selecionadas = []
        self.atualizar_view()

    def atualizar_view(self):
        self.view.atualizar(self.desenho, self.figura_nova, self.selecionadas, self.retangulo_selecao_atual)
