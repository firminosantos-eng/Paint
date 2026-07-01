import tkinter as tk

# ---------------------------------------------------------------------------
# 01-linha.py — referência imperativa
#
# Desenha uma única linha por vez: a cada novo clique + arraste, a linha
# anterior é apagada e uma nova é traçada. Não há acumulação de figuras.
# ---------------------------------------------------------------------------

ponto_inicial = None  # (x, y) de onde o traço começou


def iniciar_linha(event):
    global ponto_inicial
    ponto_inicial = (event.x, event.y)
    canvas.delete("all")  # apaga a linha anterior


def atualizar_linha(event):
    canvas.delete("all")
    x0, y0 = ponto_inicial
    canvas.create_line(x0, y0, event.x, event.y, fill="black")


def main():
    global canvas

    root = tk.Tk()
    root.title("Paint — uma linha por vez")

    canvas = tk.Canvas(root, bg="white", width=700, height=600)
    canvas.pack(padx=5, pady=5)

    canvas.bind("<ButtonPress-1>", iniciar_linha)
    canvas.bind("<B1-Motion>", atualizar_linha)

    root.mainloop()


if __name__ == "__main__":
    main()
