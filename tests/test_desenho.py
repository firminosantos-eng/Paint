from paint.modelo.desenho import Desenho
from paint.modelo.figura import Linha, Retangulo


def _figura(classe, x0, y0, x1, y1, cor_borda="black", cor_preenchimento=""):
    figura = classe(x0, y0, cor_borda, cor_preenchimento)
    figura.atualizar(x1, y1)
    return figura


def test_remover_tira_a_figura_da_colecao():
    desenho = Desenho()
    figura = _figura(Linha, 0, 0, 10, 10)
    desenho.incluir(figura)
    desenho.remover(figura)
    assert len(desenho) == 0


def test_mover_para_frente_coloca_a_figura_no_final_da_lista():
    desenho = Desenho()
    a = _figura(Linha, 0, 0, 10, 10)
    b = _figura(Linha, 1, 1, 11, 11)
    desenho.incluir(a)
    desenho.incluir(b)

    desenho.mover_para_frente(a)

    assert list(desenho) == [b, a]


def test_mover_para_tras_coloca_a_figura_no_inicio_da_lista():
    desenho = Desenho()
    a = _figura(Linha, 0, 0, 10, 10)
    b = _figura(Linha, 1, 1, 11, 11)
    desenho.incluir(a)
    desenho.incluir(b)

    desenho.mover_para_tras(b)

    assert list(desenho) == [b, a]


def test_figura_no_ponto_retorna_a_figura_mais_ao_topo_entre_sobrepostas():
    desenho = Desenho()
    de_baixo = _figura(Retangulo, 0, 0, 50, 50)
    de_cima = _figura(Retangulo, 0, 0, 50, 50)
    desenho.incluir(de_baixo)
    desenho.incluir(de_cima)

    assert desenho.figura_no_ponto(25, 25) is de_cima


def test_figura_no_ponto_retorna_none_quando_nada_e_atingido():
    desenho = Desenho()
    desenho.incluir(_figura(Retangulo, 0, 0, 10, 10))
    assert desenho.figura_no_ponto(500, 500) is None


def test_figuras_na_area_retorna_so_as_totalmente_contidas():
    desenho = Desenho()
    dentro = _figura(Retangulo, 10, 10, 20, 20)
    fora = _figura(Retangulo, 10, 10, 500, 500)
    desenho.incluir(dentro)
    desenho.incluir(fora)

    selecionadas = desenho.figuras_na_area((0, 0, 100, 100))

    assert selecionadas == [dentro]
