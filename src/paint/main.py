"""
Ponto de entrada do Projeto Paint (Entrega 3 — arquitetura MVC).

Monta o Model (`Desenho`), a View (`Janela`) e o Controller
(`ControladorDesenho`), liga os três e inicia o loop de eventos do
Tkinter. Esta é a única peça do programa que conhece as três camadas ao
mesmo tempo — é aqui que a "fiação" do MVC acontece.
"""

import tkinter as tk

from paint.modelo.desenho import Desenho
from paint.visao.janela import Janela
from paint.controlador.controlador_desenho import ControladorDesenho


def main():
    root = tk.Tk()

    desenho = Desenho()
    view = Janela(root)
    controlador = ControladorDesenho(desenho, view)
    view.definir_controlador(controlador)

    view.atualizar(desenho)  # estado inicial: canvas vazio

    view.executar()


if __name__ == "__main__":
    main()
