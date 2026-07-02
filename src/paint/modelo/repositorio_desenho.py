import json


class RepositorioDesenho:
    def salvar(self, desenho, caminho):
        dados = {"figuras": desenho.para_lista_dict()}
        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=2)

    def carregar(self, desenho, caminho):
        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        desenho.carregar_de_lista_dict(dados["figuras"])
