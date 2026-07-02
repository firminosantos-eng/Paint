import tkinter as tk

ponto_inicial = None


def iniciar_linha(event):
    global ponto_inicial
    ponto_inicial = (event.x, event.y)
    canvas.delete("all")


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
