"""Cria (ou troca a senha de) um usuário da API.

Uso, de dentro da pasta api/:
    python -m app.criar_usuario admin

A senha é pedida no terminal (não aparece enquanto você digita) e
gravada apenas como hash Argon2.
"""

import getpass
import sys

from app.auth import hash_senha
from app.db import conectar


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Uso: python -m app.criar_usuario <nome-do-usuario>")
    usuario = sys.argv[1]

    senha = getpass.getpass(f"Senha para '{usuario}': ")
    if len(senha) < 8:
        sys.exit("A senha precisa ter pelo menos 8 caracteres.")
    if getpass.getpass("Repita a senha: ") != senha:
        sys.exit("As senhas não conferem.")

    conn = conectar()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO usuario_api (usuario, senha_hash) VALUES (%s, %s) "
                "ON DUPLICATE KEY UPDATE senha_hash = VALUES(senha_hash)",
                (usuario, hash_senha(senha)),
            )
        conn.commit()
    finally:
        conn.close()
    print(f"Usuário '{usuario}' pronto para fazer login em POST /auth/token.")


if __name__ == "__main__":
    main()
