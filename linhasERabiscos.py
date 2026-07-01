import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser

# ---------------------------------------------------------------------------
# 03-linhasERabiscos.py
#
# Esqueleto base (linhas + rabiscos, com OptionMenu) evoluído para a
# Entrega 1 (tag imperativa.1), com:
#   * Desenho de retângulos
#   * Desenho de ovais
#   * Cor de borda por figura
#   * Cor de preenchimento por figura
#
# Cada figura é representada como uma tupla:
#   (tipo, valores, cor_borda, cor_preenchimento)
# onde tipo pertence a {"linha", "rabisco", "retangulo", "oval"}.
#
# Ainda em estilo imperativo (if tipo == "..."), como pedido nesta entrega.
# O padrão State que elimina essa condicional só entra na Entrega 4.
# ---------------------------------------------------------------------------

figuras = []        # todas as figuras já concluídas
figura_nova = None  # figura sendo desenhada no momento

cor_borda_atual = "black"      # cor de borda usada na próxima figura
cor_preenchimento_atual = ""   # cor de preenchimento ("" = sem preenchimento)


# ---------------------------------------------------------------------------
# Callbacks de mouse
# ---------------------------------------------------------------------------

def iniciar_figura_nova(event):
    """Chamado quando o botão do mouse é pressionado sobre o canvas."""
    global figura_nova
    tipo = tipo_figura_var.get()

    if tipo == "Linha":
        figura_nova = ("linha", (event.x, event.y, event.x, event.y),
                       cor_borda_atual, cor_preenchimento_atual)
    elif tipo == "Rabisco":
        figura_nova = ("rabisco", [(event.x, event.y)],
                       cor_borda_atual, cor_preenchimento_atual)
    elif tipo == "Retangulo":
        figura_nova = ("retangulo", (event.x, event.y, event.x, event.y),
                       cor_borda_atual, cor_preenchimento_atual)
    else:  # tipo == "Oval"
        figura_nova = ("oval", (event.x, event.y, event.x, event.y),
                       cor_borda_atual, cor_preenchimento_atual)


def atualizar_figura_nova(event):
    """Chamado a cada movimento do mouse com o botão pressionado."""
    global figura_nova
    tipo, valores, cor_borda, cor_preenchimento = figura_nova

    if tipo == "rabisco":
        valores.append((event.x, event.y))
    else:  # "linha", "retangulo" e "oval" são definidos por dois cantos
        valores = (valores[0], valores[1], event.x, event.y)

    figura_nova = (tipo, valores, cor_borda, cor_preenchimento)
    desenhar()
    desenhar_figura_nova()


def incluir_figura_nova(event):
    """Chamado quando o botão do mouse é solto."""
    if not incompleta(figura_nova):
        figuras.append(figura_nova)
    desenhar()


# ---------------------------------------------------------------------------
# Desenho
# ---------------------------------------------------------------------------

def desenhar_uma_figura(figura, tracejado=False):
    tipo, valores, cor_borda, cor_preenchimento = figura
    opcoes = {"dash": (4, 2)} if tracejado else {}

    if tipo == "linha":
        canvas.create_line(valores[0], valores[1], valores[2], valores[3],
                            fill=cor_borda, **opcoes)
    elif tipo == "rabisco":
        canvas.create_line(valores, fill=cor_borda, **opcoes)
    elif tipo == "retangulo":
        canvas.create_rectangle(valores[0], valores[1], valores[2], valores[3],
                                 outline=cor_borda, fill=cor_preenchimento, **opcoes)
    else:  # tipo == "oval"
        canvas.create_oval(valores[0], valores[1], valores[2], valores[3],
                            outline=cor_borda, fill=cor_preenchimento, **opcoes)


def desenhar():
    canvas.delete("all")
    for figura in figuras:
        desenhar_uma_figura(figura)


def desenhar_figura_nova():
    desenhar_uma_figura(figura_nova, tracejado=True)


def incompleta(figura):
    """Evita incluir figuras degeneradas: uma linha sem comprimento, um
    rabisco com um único ponto, ou um retângulo/oval sem área."""
    tipo, valores, _, _ = figura
    if tipo == "rabisco":
        return len(valores) <= 1
    else:  # "linha", "retangulo" ou "oval"
        return (valores[0], valores[1]) == (valores[2], valores[3])


# ---------------------------------------------------------------------------
# Seleção de cores
# ---------------------------------------------------------------------------

def escolher_cor_borda():
    global cor_borda_atual
    cor = colorchooser.askcolor(title="Cor da borda", initialcolor=cor_borda_atual)[1]
    if cor is not None:
        cor_borda_atual = cor
        amostra_borda.config(bg=cor_borda_atual)


def escolher_cor_preenchimento():
    global cor_preenchimento_atual
    cor_inicial = cor_preenchimento_atual if cor_preenchimento_atual else "white"
    cor = colorchooser.askcolor(title="Cor de preenchimento", initialcolor=cor_inicial)[1]
    if cor is not None:
        cor_preenchimento_atual = cor
        amostra_preenchimento.config(bg=cor_preenchimento_atual)


def remover_preenchimento():
    global cor_preenchimento_atual
    cor_preenchimento_atual = ""
    amostra_preenchimento.config(bg=cor_fundo_padrao)


# ---------------------------------------------------------------------------
# Interface (main)
# ---------------------------------------------------------------------------

def main():
    global canvas, tipo_figura_var, amostra_borda, amostra_preenchimento, cor_fundo_padrao

    root = tk.Tk()
    root.title("Projeto Paint — Entrega 1")
    frame = tk.Frame(root)

    paddings = {"padx": 5, "pady": 5}

    # Ferramenta (tipo de figura)
    label = ttk.Label(frame, text="Ferramenta:")
    label.grid(column=0, row=0, sticky=tk.W, **paddings)

    tipo_figura_var = tk.StringVar(root)
    option_menu = ttk.OptionMenu(frame, tipo_figura_var,
                                  "Linha", "Linha", "Rabisco", "Retangulo", "Oval")
    option_menu.grid(column=1, row=0, sticky=tk.W, **paddings)

    # Cor de borda
    botao_cor_borda = ttk.Button(frame, text="Cor da borda", command=escolher_cor_borda)
    botao_cor_borda.grid(column=2, row=0, sticky=tk.W, **paddings)

    amostra_borda = tk.Label(frame, text="  ", bg=cor_borda_atual, relief=tk.SUNKEN, width=3)
    amostra_borda.grid(column=3, row=0, sticky=tk.W, **paddings)

    # Cor de preenchimento
    botao_cor_preenchimento = ttk.Button(frame, text="Cor de preenchimento",
                                          command=escolher_cor_preenchimento)
    botao_cor_preenchimento.grid(column=4, row=0, sticky=tk.W, **paddings)

    cor_fundo_padrao = frame.cget("bg")
    amostra_preenchimento = tk.Label(frame, text="  ", bg=cor_fundo_padrao, relief=tk.SUNKEN, width=3)
    amostra_preenchimento.grid(column=5, row=0, sticky=tk.W, **paddings)

    botao_sem_preenchimento = ttk.Button(frame, text="Sem preenchimento",
                                          command=remover_preenchimento)
    botao_sem_preenchimento.grid(column=6, row=0, sticky=tk.W, **paddings)

    # Área de desenho
    canvas = tk.Canvas(frame, bg="white", width=700, height=600)
    canvas.grid(column=0, row=1, columnspan=7, sticky=tk.W, **paddings)

    frame.pack()

    # Eventos de mouse associados ao canvas
    canvas.bind("<ButtonPress-1>", iniciar_figura_nova)
    canvas.bind("<B1-Motion>", atualizar_figura_nova)
    canvas.bind("<ButtonRelease-1>", incluir_figura_nova)

    root.mainloop()


if __name__ == "__main__":
    main()
