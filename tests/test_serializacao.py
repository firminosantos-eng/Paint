import json

from paint.modelo.desenho import Desenho
from paint.modelo.figura import (
    CLASSES_FIGURA, Linha, Retangulo, Oval, Rabisco, Triangulo, Estrela,
    figura_de_dict,
)
from paint.modelo.repositorio_desenho import RepositorioDesenho


def _figura(classe, x0, y0, x1, y1, cor_borda="black", cor_preenchimento="red"):
    figura = classe(x0, y0, cor_borda, cor_preenchimento)
    figura.atualizar(x1, y1)
    return figura


def test_todas_as_classes_de_figura_fazem_round_trip_completo():
    for nome, classe in CLASSES_FIGURA.items():
        original = _figura(classe, 5, 5, 45, 65)

        dados = original.para_dict()
        assert dados["tipo"] == nome

        reconstruida = figura_de_dict(dados)

        assert type(reconstruida) is classe
        assert reconstruida.cor_borda == original.cor_borda
        assert reconstruida.cor_preenchimento == original.cor_preenchimento
        assert reconstruida.descricao_desenho() == original.descricao_desenho()


def test_rabisco_preserva_todos_os_pontos_no_round_trip():
    rabisco = Rabisco(0, 0, "black", "")
    for x, y in [(1, 1), (2, 4), (3, 9)]:
        rabisco.atualizar(x, y)

    reconstruido = figura_de_dict(rabisco.para_dict())

    assert reconstruido.pontos == rabisco.pontos


def test_para_dict_so_usa_tipos_nativos_serializaveis_em_json():
    figura = _figura(Retangulo, 0, 0, 10, 10)
    json.dumps(figura.para_dict())


def test_desenho_faz_round_trip_da_colecao_inteira():
    desenho = Desenho()
    desenho.incluir(_figura(Linha, 0, 0, 10, 10))
    desenho.incluir(_figura(Oval, 5, 5, 25, 15))

    lista = desenho.para_lista_dict()

    novo_desenho = Desenho()
    novo_desenho.carregar_de_lista_dict(lista)

    assert len(novo_desenho) == len(desenho)


def test_repositorio_salva_e_carrega_um_desenho_do_disco(tmp_path):
    desenho = Desenho()
    desenho.incluir(_figura(Triangulo, 0, 0, 80, 60))
    desenho.incluir(_figura(Estrela, 10, 10, 90, 90))

    caminho = tmp_path / "meu_desenho.json"
    repositorio = RepositorioDesenho()
    repositorio.salvar(desenho, caminho)

    assert caminho.exists()

    desenho_carregado = Desenho()
    repositorio.carregar(desenho_carregado, caminho)

    assert len(desenho_carregado) == len(desenho)


def test_arquivo_salvo_e_json_valido_com_a_estrutura_esperada(tmp_path):
    desenho = Desenho()
    desenho.incluir(_figura(Linha, 0, 0, 10, 10))

    caminho = tmp_path / "desenho.json"
    RepositorioDesenho().salvar(desenho, caminho)

    with open(caminho, encoding="utf-8") as arquivo:
        conteudo = json.load(arquivo)

    assert "figuras" in conteudo
    assert len(conteudo["figuras"]) == 1
    assert conteudo["figuras"][0]["tipo"] == "Linha"
