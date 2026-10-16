"""API REST do Zoolife.

Rodar (de dentro da pasta api/):  uvicorn app.main:app --reload
Documentação interativa:          http://127.0.0.1:8000/docs
"""

import pymysql
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app import auth
from app.routers import animais, clientes, consultas, relatorios, veterinarios

app = FastAPI(
    title="Zoolife API",
    description=(
        "API REST sobre o banco de dados da rede de clínicas veterinárias Zoolife (MariaDB).\n\n"
        "**Leitura (GET) é aberta. Cadastrar, alterar e remover exigem login:** "
        "use o botão **Authorize** com usuário e senha."
    ),
    version="1.1.0",
)

app.include_router(auth.router)
app.include_router(clientes.router)
app.include_router(animais.router)
app.include_router(veterinarios.router)
app.include_router(consultas.router)
app.include_router(relatorios.router)

# Códigos de erro do MariaDB traduzidos para mensagens da API.
MENSAGENS_INTEGRIDADE = {
    1062: "Registro duplicado: já existe um cadastro com esse identificador.",
    1451: "Não é possível remover: existem registros que dependem deste.",
    1452: "Referência inválida: o registro relacionado não existe.",
}


@app.exception_handler(pymysql.err.IntegrityError)
def erro_de_integridade(request: Request, exc: pymysql.err.IntegrityError):
    """Transforma violações de chave (PK, UNIQUE, FK) em 409 Conflict."""
    codigo = exc.args[0] if exc.args else None
    mensagem = MENSAGENS_INTEGRIDADE.get(codigo, "Violação de integridade no banco de dados.")
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": mensagem})


@app.get("/", tags=["Status"], summary="Status da API")
def raiz():
    return {"api": "Zoolife", "versao": app.version, "documentacao": "/docs"}
