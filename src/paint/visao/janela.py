

import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import messagebox

from paint.modelo.figura import CLASSES_FIGURA, FORMAS_PRONTAS


class Janela:
    def __init__(self, root):
        self.root = root
        self.controlador = None  

        self.cor_borda_atual = "black"
        self.cor_preenchimento_atual = ""

        self._montar_interface()

    def definir_controlador(self, controlador):
        self.controlador = controlador

    def _montar_interface(self):
        self.root.title("Projeto Paint — Entrega 4 (State + Salvar/Abrir)")
        frame = tk.Frame(self.root)
        paddings = {"padx": 5, "pady": 5}

        label = ttk.Label(frame, text="Ferramenta:")
        label.grid(column=0, row=0, sticky=tk.W, **paddings)

        self.tipo_ferramenta_var = tk.StringVar(self.root, value="Linha")
        self.tipo_ferramenta_var.trace_add("write", self._ferramenta_alterada)

        menu_ferramenta = self._montar_menu_ferramenta()
        botao_ferramenta = ttk.Menubutton(frame, textvariable=self.tipo_ferramenta_var,
                                           menu=menu_ferramenta, direction="below")
        botao_ferramenta.grid(column=1, row=0, sticky=tk.W, **paddings)

        botao_cor_borda = ttk.Button(frame, text="Cor da borda", command=self._escolher_cor_borda)
        botao_cor_borda.grid(column=2, row=0, sticky=tk.W, **paddings)

        self.amostra_borda = tk.Label(frame, text="  ", bg=self.cor_borda_atual,
                                       relief=tk.SUNKEN, width=3)
        self.amostra_borda.grid(column=3, row=0, sticky=tk.W, **paddings)

        botao_cor_preenchimento = ttk.Button(frame, text="Cor de preenchimento",
                                              command=self._escolher_cor_preenchimento)
        botao_cor_preenchimento.grid(column=4, row=0, sticky=tk.W, **paddings)

        self._cor_fundo_padrao = frame.cget("bg")
        self.amostra_preenchimento = tk.Label(frame, text="  ", bg=self._cor_fundo_padrao,
                                               relief=tk.SUNKEN, width=3)
        self.amostra_preenchimento.grid(column=5, row=0, sticky=tk.W, **paddings)

        botao_sem_preenchimento = ttk.Button(frame, text="Sem preenchimento",
                                              command=self._remover_preenchimento)
        botao_sem_preenchimento.grid(column=6, row=0, sticky=tk.W, **paddings)

        botao_desfazer = ttk.Button(frame, text="Desfazer (Ctrl+Z)",
                                     command=self._pedir_desfazer)
        botao_desfazer.grid(column=7, row=0, sticky=tk.W, **paddings)

        botao_salvar = ttk.Button(frame, text="Salvar", command=self._salvar)
        botao_salvar.grid(column=8, row=0, sticky=tk.W, **paddings)

        botao_abrir = ttk.Button(frame, text="Abrir", command=self._abrir)
        botao_abrir.grid(column=9, row=0, sticky=tk.W, **paddings)

        self.canvas = tk.Canvas(frame, bg="white", width=700, height=600)
        self.canvas.grid(column=0, row=1, columnspan=10, sticky=tk.W, **paddings)

        frame.pack()

        self.canvas.bind("<ButtonPress-1>", self._evento_pressionar)
        self.canvas.bind("<B1-Motion>", self._evento_arrastar)
        self.canvas.bind("<ButtonRelease-1>", self._evento_soltar)
        self.root.bind("<Control-z>", lambda event: self._pedir_desfazer())
        self.root.bind("<Control-s>", lambda event: self._salvar())
        self.root.bind("<Control-o>", lambda event: self._abrir())

    def _montar_menu_ferramenta(self):
        menu = tk.Menu(self.root, tearoff=False)

        for nome in CLASSES_FIGURA:
            if nome in FORMAS_PRONTAS:
                continue
            menu.add_radiobutton(label=nome, variable=self.tipo_ferramenta_var, value=nome)

        submenu_formas = tk.Menu(menu, tearoff=False)
        for nome in FORMAS_PRONTAS:
            submenu_formas.add_radiobutton(label=nome, variable=self.tipo_ferramenta_var, value=nome)
        menu.add_cascade(label="Formas", menu=submenu_formas)

        return menu


    def _ferramenta_alterada(self, *_args):
        if self.controlador is not None:
            self.controlador.selecionar_ferramenta(self.tipo_ferramenta_var.get())

    def _evento_pressionar(self, event):
        if self.controlador is not None:
            self.controlador.ao_pressionar_botao(event.x, event.y)

    def _evento_arrastar(self, event):
        if self.controlador is not None:
            self.controlador.ao_arrastar(event.x, event.y)

    def _evento_soltar(self, event):
        if self.controlador is not None:
            self.controlador.ao_soltar_botao(event.x, event.y)

    def _pedir_desfazer(self):
        if self.controlador is not None:
            self.controlador.desfazer()

    def _escolher_cor_borda(self):
        cor = colorchooser.askcolor(title="Cor da borda", initialcolor=self.cor_borda_atual)[1]
        if cor is not None:
            self.cor_borda_atual = cor
            self.amostra_borda.config(bg=cor)
            if self.controlador is not None:
                self.controlador.definir_cor_borda(cor)

    def _escolher_cor_preenchimento(self):
        cor_inicial = self.cor_preenchimento_atual if self.cor_preenchimento_atual else "white"
        cor = colorchooser.askcolor(title="Cor de preenchimento", initialcolor=cor_inicial)[1]
        if cor is not None:
            self.cor_preenchimento_atual = cor
            self.amostra_preenchimento.config(bg=cor)
            if self.controlador is not None:
                self.controlador.definir_cor_preenchimento(cor)

    def _remover_preenchimento(self):
        self.cor_preenchimento_atual = ""
        self.amostra_preenchimento.config(bg=self._cor_fundo_padrao)
        if self.controlador is not None:
            self.controlador.definir_cor_preenchimento("")

    def _salvar(self):
        if self.controlador is None:
            return
        caminho = filedialog.asksaveasfilename(
            title="Salvar desenho",
            defaultextension=".json",
            filetypes=[("Desenho (JSON)", "*.json")],
        )
        if not caminho:
            return
        try:
            self.controlador.salvar(caminho)
        except OSError as erro:
            messagebox.showerror("Erro ao salvar", str(erro))

    def _abrir(self):
        if self.controlador is None:
            return
        caminho = filedialog.askopenfilename(
            title="Abrir desenho",
            defaultextension=".json",
            filetypes=[("Desenho (JSON)", "*.json")],
        )
        if not caminho:
            return
        try:
            self.controlador.abrir(caminho)
        except (OSError, ValueError, KeyError) as erro:
            messagebox.showerror("Erro ao abrir", str(erro))

    def atualizar(self, desenho, figura_em_construcao=None):
        self.canvas.delete("all")
        for figura in desenho:
            self._desenhar_figura(figura)
        if figura_em_construcao is not None:
            self._desenhar_figura(figura_em_construcao, tracejado=True)

    def _desenhar_figura(self, figura, tracejado=False):
        primitivo, pontos = figura.descricao_desenho()
        opcoes = {"dash": (4, 2)} if tracejado else {}

        if primitivo == "linha":
            if len(pontos) >= 2:
                self.canvas.create_line(pontos, fill=figura.cor_borda, **opcoes)
        elif primitivo == "retangulo":
            self.canvas.create_rectangle(*pontos, outline=figura.cor_borda,
                                          fill=figura.cor_preenchimento, **opcoes)
        elif primitivo == "oval":
            self.canvas.create_oval(*pontos, outline=figura.cor_borda,
                                     fill=figura.cor_preenchimento, **opcoes)
        elif primitivo == "poligono":
            if len(pontos) >= 3:
                self.canvas.create_polygon(pontos, outline=figura.cor_borda,
                                            fill=figura.cor_preenchimento, **opcoes)

    def executar(self):
        self.root.mainloop()
