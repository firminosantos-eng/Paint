import tkinter as tk

# ---------------------------------------------------------------------------
# 02-linhas.py — referência imperativa
#
# Evolução do 01-linha.py: agora as linhas se acumulam numa lista, então
# cada nova linha desenhada não apaga as anteriores.
# ---------------------------------------------------------------------------

linhas = []       # lista de linhas já concluídas: cada item é (x0, y0, x1, y1)
linha_nova = None  # linha em construção (ainda não incluída em "linhas")


def iniciar_linha_nova(event):
    global linha_nova
    linha_nova = (event.x, event.y, event.x, event.y)


def atualizar_linha_nova(event):
    global linha_nova
    x0, y0, _, _ = linha_nova
    linha_nova = (x0, y0, event.x, event.y)
    desenhar()
    desenhar_linha_nova()


def incluir_linha_nova(event):
    if not incompleta(linha_nova):
        linhas.append(linha_nova)
    desenhar()


def desenhar():
    canvas.delete("all")
    for x0, y0, x1, y1 in linhas:
        canvas.create_line(x0, y0, x1, y1, fill="black")


def desenhar_linha_nova():
    x0, y0, x1, y1 = linha_nova
    canvas.create_line(x0, y0, x1, y1, fill="black", dash=(4, 2))


def incompleta(linha):
    x0, y0, x1, y1 = linha
    return (x0, y0) == (x1, y1)  # comprimento zero: clique sem arrastar


def main():
    global canvas

    root = tk.Tk()
    root.title("Paint — várias linhas")

    canvas = tk.Canvas(root, bg="white", width=700, height=600)
    canvas.pack(padx=5, pady=5)

    canvas.bind("<ButtonPress-1>", iniciar_linha_nova)
    canvas.bind("<B1-Motion>", atualizar_linha_nova)
    canvas.bind("<ButtonRelease-1>", incluir_linha_nova)

    root.mainloop()


if __name__ == "__main__":
    main()
