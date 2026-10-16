"""Testes de integração: rodam contra o banco `clinica` carregado com
sql/01_schema.sql, sql/02_dados_exemplo.sql e sql/04_usuarios_api.sql.
Tudo o que um teste cria (inclusive o usuário de login) é apagado no
final, então os dados de exemplo ficam intactos.

Rodar (de dentro da pasta api/):  python -m pytest -v
"""

import pytest
from fastapi.testclient import TestClient

from app.auth import hash_senha
from app.db import conectar
from app.main import app

client = TestClient(app)    # recebe o token de login (ver fixture abaixo)
anonimo = TestClient(app)   # nunca faz login

CPF_TESTE = "99999999901"
CPF_MARIANA = "19032343550"  # cliente dos dados de exemplo, dona da Zoe Maria
USUARIO_TESTE = "teste_automatizado"
SENHA_TESTE = "senha-de-teste-123"


def _executar(*comandos):
    conn = conectar()
    try:
        with conn.cursor() as cur:
            for sql, params in comandos:
                cur.execute(sql, params)
        conn.commit()
    finally:
        conn.close()


def _limpar_dados_de_teste():
    _executar(
        ("DELETE FROM consulta WHERE Animal_ID IN (SELECT Animal_ID FROM animal WHERE Dono_CPF = %s)", (CPF_TESTE,)),
        ("DELETE FROM animal WHERE Dono_CPF = %s", (CPF_TESTE,)),
        ("DELETE FROM cliente WHERE CPF = %s", (CPF_TESTE,)),
    )


@pytest.fixture(scope="module", autouse=True)
def usuario_logado():
    """Cria um usuário de login só para os testes e coloca o token no `client`."""
    _executar(
        ("DELETE FROM usuario_api WHERE usuario = %s", (USUARIO_TESTE,)),
        ("INSERT INTO usuario_api (usuario, senha_hash) VALUES (%s, %s)", (USUARIO_TESTE, hash_senha(SENHA_TESTE))),
    )
    resposta = client.post("/auth/token", data={"username": USUARIO_TESTE, "password": SENHA_TESTE})
    client.headers["Authorization"] = f"Bearer {resposta.json()['access_token']}"
    yield
    _executar(("DELETE FROM usuario_api WHERE usuario = %s", (USUARIO_TESTE,)))


@pytest.fixture(autouse=True)
def banco_limpo():
    _limpar_dados_de_teste()
    yield
    _limpar_dados_de_teste()


def novo_cliente():
    return {"cpf": CPF_TESTE, "nome": "Cliente de Teste", "email": "teste@example.com"}


# ---------- leitura ----------
def test_raiz():
    assert client.get("/").json()["api"] == "Zoolife"


def test_lista_clientes_em_ordem_alfabetica():
    clientes = client.get("/clientes").json()
    assert len(clientes) == 10
    assert clientes[0]["nome"] == "Eduardo Lopes"


def test_filtra_clientes_por_nome():
    clientes = client.get("/clientes", params={"nome": "alves"}).json()
    assert [c["nome"] for c in clientes] == ["Mariana Alves"]


def test_detalha_cliente_com_telefones_e_animais():
    cliente = client.get(f"/clientes/{CPF_MARIANA}").json()
    assert cliente["telefones"] == ["21998345671"]
    assert cliente["animais"][0]["nome"] == "Zoe Maria"


def test_cliente_inexistente_retorna_404():
    assert client.get("/clientes/00000000000").status_code == 404


def test_filtra_animais_por_especie():
    gatos = client.get("/animais", params={"especie": "Gato"}).json()
    assert [g["nome"] for g in gatos] == ["Felix", "Katy", "Marrocos", "Musa"]


def test_veterinarios_trazem_a_filial():
    vets = client.get("/veterinarios", params={"especialidade": "Cirurgia"}).json()
    assert vets == [{
        "cpf": "45561230988", "nome": "Dr. Roberto", "crmv": 1001,
        "especialidade": "Cirurgia", "filial": "Clinica Matriz Centro",
    }]


def test_agenda_filtrada_por_dia():
    consultas = client.get("/consultas", params={"data": "2026-06-08"}).json()
    assert len(consultas) == 4
    assert consultas[0]["animal"] == "Zoe Maria"
    assert consultas[0]["tutor"] == "Mariana Alves"


def test_prontuario_da_consulta():
    consulta = client.get("/consultas/1").json()
    assert consulta["veterinario"] == "Dr. Roberto"
    assert consulta["exames"][0]["tipo"] == "Hemograma"
    assert consulta["receitas"][0]["medicamento"] == "Antibiotico Pet"
    assert consulta["pagamento"]["forma"] == "Pix"


def test_faturamento_por_filial():
    relatorio = client.get("/relatorios/faturamento-por-filial").json()
    assert relatorio[0] == {"filial": "Clinica Matriz Centro", "consultas": 3, "faturamento": "420.00"}
    assert len(relatorio) == 7


# ---------- escrita e regras do banco ----------
def test_ciclo_completo_de_cliente():
    assert client.post("/clientes", json=novo_cliente()).status_code == 201

    resposta = client.put(f"/clientes/{CPF_TESTE}", json={"nome": "Nome Alterado"})
    assert resposta.status_code == 200
    assert client.get(f"/clientes/{CPF_TESTE}").json()["nome"] == "Nome Alterado"

    assert client.delete(f"/clientes/{CPF_TESTE}").status_code == 204
    assert client.get(f"/clientes/{CPF_TESTE}").status_code == 404


def test_cpf_repetido_retorna_409():
    client.post("/clientes", json=novo_cliente())
    resposta = client.post("/clientes", json=novo_cliente())
    assert resposta.status_code == 409
    assert "duplicado" in resposta.json()["detail"]


def test_cpf_invalido_retorna_422():
    resposta = client.post("/clientes", json={**novo_cliente(), "cpf": "123"})
    assert resposta.status_code == 422


def test_animal_sem_dono_valido_retorna_409():
    resposta = client.post("/animais", json={"nome": "Fantasma", "dono_cpf": "00000000000"})
    assert resposta.status_code == 409


def test_nao_remove_cliente_que_tem_animal():
    resposta = client.delete(f"/clientes/{CPF_MARIANA}")
    assert resposta.status_code == 409
    assert client.get(f"/clientes/{CPF_MARIANA}").status_code == 200


def test_agenda_consulta_para_animal_novo():
    client.post("/clientes", json=novo_cliente())
    animal = client.post("/animais", json={"nome": "Thor", "especie": "Cachorro", "dono_cpf": CPF_TESTE}).json()

    resposta = client.post("/consultas", json={
        "data_hora": "2026-06-11T09:30:00", "sintomas": "Check-up", "valor": "130.00",
        "animal_id": animal["id"], "vet_cpf": "89912345600",
    })
    assert resposta.status_code == 201
    consulta = resposta.json()
    assert consulta["animal"] == "Thor"
    assert consulta["tutor"] == "Cliente de Teste"
    assert consulta["veterinario"] == "Dr. Lucas"


# ---------- login ----------
def test_leitura_nao_exige_login():
    assert anonimo.get("/clientes").status_code == 200


@pytest.mark.parametrize("metodo, rota, corpo", [
    ("post", "/clientes", {"cpf": CPF_TESTE, "nome": "Sem Login"}),
    ("put", f"/clientes/{CPF_MARIANA}", {"nome": "Invasor"}),
    ("delete", f"/clientes/{CPF_MARIANA}", None),
    ("post", "/animais", {"nome": "Rex", "dono_cpf": CPF_MARIANA}),
    ("post", "/consultas", {"data_hora": "2026-06-11T09:30:00", "valor": "1.00",
                            "animal_id": 1, "vet_cpf": "89912345600"}),
])
def test_escrita_sem_login_retorna_401(metodo, rota, corpo):
    resposta = anonimo.request(metodo, rota, json=corpo)
    assert resposta.status_code == 401
    # nada foi alterado
    assert anonimo.get(f"/clientes/{CPF_MARIANA}").json()["nome"] == "Mariana Alves"
    assert anonimo.get(f"/clientes/{CPF_TESTE}").status_code == 404


def test_login_com_senha_errada_retorna_401():
    resposta = anonimo.post("/auth/token", data={"username": USUARIO_TESTE, "password": "senha-errada"})
    assert resposta.status_code == 401


def test_login_com_usuario_inexistente_retorna_401():
    resposta = anonimo.post("/auth/token", data={"username": "ninguem", "password": "qualquer-coisa"})
    assert resposta.status_code == 401


def test_token_falsificado_retorna_401():
    resposta = anonimo.get("/auth/me", headers={"Authorization": "Bearer token.inventado.aqui"})
    assert resposta.status_code == 401


def test_me_mostra_usuario_logado():
    assert client.get("/auth/me").json() == {"usuario": USUARIO_TESTE}
