from paint.modelo.figura import (
    Linha, Retangulo, Oval, Rabisco, Triangulo, Estrela,
)


def _figura(classe, x0, y0, x1, y1, cor_borda="black", cor_preenchimento=""):
    figura = classe(x0, y0, cor_borda, cor_preenchimento)
    figura.atualizar(x1, y1)
    return figura


def test_figura_recem_criada_com_clique_unico_esta_incompleta():
    linha = Linha(10, 10, "black", "")
    assert linha.incompleta()


def test_figura_fica_completa_apos_arrastar():
    linha = _figura(Linha, 0, 0, 50, 50)
    assert not linha.incompleta()


def test_rabisco_com_um_unico_ponto_esta_incompleto():
    rabisco = Rabisco(5, 5, "black", "")
    assert rabisco.incompleta()


def test_rabisco_com_dois_pontos_nao_esta_incompleto():
    rabisco = Rabisco(5, 5, "black", "")
    rabisco.atualizar(10, 10)
    assert not rabisco.incompleta()


def test_atualizar_move_o_segundo_canto_sem_alterar_o_primeiro():
    retangulo = Retangulo(0, 0, "black", "")
    retangulo.atualizar(30, 40)
    assert (retangulo.x0, retangulo.y0) == (0, 0)
    assert (retangulo.x1, retangulo.y1) == (30, 40)


def test_rabisco_atualizar_acumula_pontos_em_ordem():
    rabisco = Rabisco(0, 0, "black", "")
    rabisco.atualizar(1, 1)
    rabisco.atualizar(2, 2)
    assert rabisco.pontos == [(0, 0), (1, 1), (2, 2)]


def test_linha_contem_ponto_sobre_o_traco_mas_nao_fora_dele():
    linha = _figura(Linha, 0, 0, 100, 0)
    assert linha.contem_ponto(50, 0)
    assert not linha.contem_ponto(50, 20)


def test_retangulo_contem_ponto_dentro_da_caixa():
    retangulo = _figura(Retangulo, 10, 10, 60, 60)
    assert retangulo.contem_ponto(30, 30)
    assert not retangulo.contem_ponto(5, 5)


def test_retangulo_contem_ponto_mesmo_com_arraste_invertido():
    retangulo = _figura(Retangulo, 60, 60, 10, 10)
    assert retangulo.contem_ponto(30, 30)


def test_oval_contem_ponto_dentro_da_elipse_mas_nao_no_canto_da_caixa():
    oval = _figura(Oval, 0, 0, 100, 50)
    assert oval.contem_ponto(50, 25)
    assert not oval.contem_ponto(0, 0)


def test_forma_poligonal_contem_ponto_no_centro_mas_nao_no_canto_da_caixa():
    triangulo = _figura(Triangulo, 0, 0, 100, 100)
    cx, cy, _, _ = triangulo._centro_e_raios()
    assert triangulo.contem_ponto(cx, cy)
    assert not triangulo.contem_ponto(0, 0)


def test_estrela_contem_ponto_no_centro():
    estrela = _figura(Estrela, 0, 0, 100, 100)
    cx, cy, _, _ = estrela._centro_e_raios()
    assert estrela.contem_ponto(cx, cy)


def test_mover_desloca_figura_dois_pontos():
    retangulo = _figura(Retangulo, 10, 10, 30, 30)
    retangulo.mover(5, -5)
    assert (retangulo.x0, retangulo.y0, retangulo.x1, retangulo.y1) == (15, 5, 35, 25)


def test_mover_desloca_todos_os_pontos_do_rabisco():
    rabisco = Rabisco(0, 0, "black", "")
    rabisco.atualizar(10, 10)
    rabisco.mover(2, 3)
    assert rabisco.pontos == [(2, 3), (12, 13)]


def test_esta_dentro_da_area_quando_totalmente_contida():
    retangulo = _figura(Retangulo, 10, 10, 20, 20)
    assert retangulo.esta_dentro_da_area(0, 0, 100, 100)


def test_esta_dentro_da_area_falso_quando_parcialmente_fora():
    retangulo = _figura(Retangulo, 10, 10, 200, 200)
    assert not retangulo.esta_dentro_da_area(0, 0, 100, 100)
