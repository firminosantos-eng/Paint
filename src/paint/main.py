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

    view.atualizar(desenho)

    view.executar()


if __name__ == "__main__":
    main()
