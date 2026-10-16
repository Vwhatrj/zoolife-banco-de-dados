"""Respostas de erro documentadas no /docs.

O FastAPI documenta sozinho só o sucesso e o 422 (validação). Os erros
abaixo também acontecem, então cada rota declara os que se aplicam a ela.
"""

from pydantic import BaseModel


class Erro(BaseModel):
    detail: str


def _erro(descricao: str, exemplo: str) -> dict:
    return {
        "model": Erro,
        "description": descricao,
        "content": {"application/json": {"example": {"detail": exemplo}}},
    }


SEM_LOGIN = {401: _erro("Sem login, ou token inválido ou expirado", "Not authenticated")}
LOGIN_INVALIDO = {401: _erro("Usuário ou senha incorretos", "Usuário ou senha incorretos")}

CLIENTE_NAO_ENCONTRADO = {404: _erro("Cliente não encontrado", "Cliente não encontrado")}
ANIMAL_NAO_ENCONTRADO = {404: _erro("Animal não encontrado", "Animal não encontrado")}
CONSULTA_NAO_ENCONTRADA = {404: _erro("Consulta não encontrada", "Consulta não encontrada")}

CPF_DUPLICADO = {409: _erro(
    "Já existe um cliente com esse CPF",
    "Registro duplicado: já existe um cadastro com esse identificador.",
)}
REFERENCIA_INVALIDA = {409: _erro(
    "O registro relacionado (dono, animal ou veterinário) não existe",
    "Referência inválida: o registro relacionado não existe.",
)}
TEM_DEPENDENTES = {409: _erro(
    "O cliente ainda tem animais ou telefones cadastrados",
    "Não é possível remover: existem registros que dependem deste.",
)}
