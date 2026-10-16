"""Autenticação com JWT.

Fluxo:
1. O cliente envia usuário e senha para POST /auth/token.
2. A API confere a senha com o hash Argon2 guardado em `usuario_api` e
   devolve um token JWT assinado, válido por JWT_EXPIRA_MINUTOS.
3. Nas rotas protegidas, o cliente manda o cabeçalho
   `Authorization: Bearer <token>`; a API valida a assinatura e a validade.
"""

import os
from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from pydantic import BaseModel

from app.db import get_db

JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGORITMO = "HS256"
JWT_EXPIRA_MINUTOS = int(os.getenv("JWT_EXPIRA_MINUTOS", "60"))

hasher = PasswordHash.recommended()  # Argon2
# Hash de uma senha qualquer, usado quando o usuário não existe: assim a
# resposta leva o mesmo tempo e não revela quais usuários estão cadastrados.
HASH_FALSO = hasher.hash("senha-que-nao-existe")

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter(prefix="/auth", tags=["Autenticação"])


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expira_em_minutos: int


class Usuario(BaseModel):
    usuario: str


def hash_senha(senha: str) -> str:
    return hasher.hash(senha)


def criar_token(usuario: str) -> str:
    expira = datetime.now(UTC) + timedelta(minutes=JWT_EXPIRA_MINUTOS)
    return jwt.encode({"sub": usuario, "exp": expira}, JWT_SECRET, algorithm=JWT_ALGORITMO)


def usuario_atual(token: Annotated[str, Depends(oauth2)]) -> Usuario:
    """Dependência das rotas protegidas: só deixa passar com token válido."""
    nao_autorizado = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "Token ausente, inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        dados = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITMO])
    except jwt.InvalidTokenError:
        raise nao_autorizado
    usuario = dados.get("sub")
    if not usuario:
        raise nao_autorizado
    return Usuario(usuario=usuario)


@router.post("/token", response_model=Token, summary="Login: troca usuário e senha por um token")
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("SELECT senha_hash FROM usuario_api WHERE usuario = %s", (form.username,))
        linha = cur.fetchone()
    senha_ok = hasher.verify(form.password, linha["senha_hash"] if linha else HASH_FALSO)
    if not linha or not senha_ok:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=criar_token(form.username), expira_em_minutos=JWT_EXPIRA_MINUTOS)


@router.get("/me", response_model=Usuario, summary="Mostra quem está logado")
def eu(usuario: Annotated[Usuario, Depends(usuario_atual)]):
    return usuario
