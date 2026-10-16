"""Conexão com o MariaDB.

Cada requisição recebe a sua própria conexão (via dependência do FastAPI),
que é fechada ao final. As consultas usam parâmetros (%s), nunca texto
concatenado, para evitar SQL injection.
"""

import os
from collections.abc import Iterator
from pathlib import Path

import pymysql
from dotenv import load_dotenv
from pymysql.cursors import DictCursor

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def conectar() -> pymysql.connections.Connection:
    return pymysql.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.getenv("DB_NAME", "clinica"),
        charset="utf8mb4",
        cursorclass=DictCursor,
        autocommit=False,
    )


def get_db() -> Iterator[pymysql.connections.Connection]:
    conn = conectar()
    try:
        yield conn
    finally:
        conn.close()
