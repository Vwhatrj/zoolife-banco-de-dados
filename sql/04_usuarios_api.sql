-- =============================================================
-- Zoolife — 04_usuarios_api.sql
-- Tabela de usuários da API REST (login). Fica separada das 12
-- tabelas do modelo da clínica, porque não faz parte do negócio:
-- serve só para controlar quem pode alterar dados pela API.
-- Rode depois de 01_schema.sql.
-- =============================================================

USE clinica;

CREATE TABLE IF NOT EXISTS usuario_api (
    Usuario_ID INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
    usuario    VARCHAR(50)  NOT NULL UNIQUE,
    -- Hash Argon2 da senha. A senha em texto puro nunca é gravada.
    senha_hash VARCHAR(255) NOT NULL,
    criado_em  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
);
