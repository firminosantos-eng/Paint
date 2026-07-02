from paint.controlador.estado_ferramenta import EstadoFerramenta


class EstadoSelecao(EstadoFerramenta):
    def __init__(self):
        self._arrastando_figuras = False
        self._selecionando_retangulo = False
        self._ultimo_x = None
        self._ultimo_y = None

    def ao_pressionar(self, controlador, x, y, ctrl=False):
        self._ultimo_x, self._ultimo_y = x, y
        figura = controlador.desenho.figura_no_ponto(x, y)

        if figura is not None:
            if ctrl:
                controlador.alternar_selecao(figura)
            elif figura not in controlador.selecionadas:
                controlador.definir_selecao([figura])
            self._arrastando_figuras = True
            self._selecionando_retangulo = False
        else:
            if not ctrl:
                controlador.definir_selecao([])
            self._selecionando_retangulo = True
            self._arrastando_figuras = False
            controlador.retangulo_selecao_atual = (x, y, x, y)

        controlador.atualizar_view()

    def ao_arrastar(self, controlador, x, y, ctrl=False):
        if self._arrastando_figuras:
            dx, dy = x - self._ultimo_x, y - self._ultimo_y
            for figura in controlador.selecionadas:
                figura.mover(dx, dy)
            self._ultimo_x, self._ultimo_y = x, y
            controlador.atualizar_view()
        elif self._selecionando_retangulo:
            x0, y0, _, _ = controlador.retangulo_selecao_atual
            controlador.retangulo_selecao_atual = (x0, y0, x, y)
            controlador.atualizar_view()

    def ao_soltar(self, controlador, x, y, ctrl=False):
        if self._selecionando_retangulo and controlador.retangulo_selecao_atual is not None:
            figuras = controlador.desenho.figuras_na_area(controlador.retangulo_selecao_atual)
            if ctrl:
                for figura in figuras:
                    controlador.alternar_selecao(figura)
            else:
                controlador.definir_selecao(figuras)

        self._arrastando_figuras = False
        self._selecionando_retangulo = False
        controlador.retangulo_selecao_atual = None
        controlador.atualizar_view()
