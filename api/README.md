# Zoolife API

API REST em **Python + FastAPI** sobre o banco de dados [`clinica`](../README.md) do Zoolife (MariaDB). Ela expõe clientes, animais, veterinários, consultas e relatórios, traduz as regras do banco (chaves primárias e estrangeiras) em respostas HTTP claras e protege as operações de escrita com **login por token JWT**.

## Tecnologias

- **Python 3.13** e **FastAPI**: rotas, validação dos dados e documentação automática (Swagger)
- **PyMySQL**: conexão com o MariaDB, com SQL escrito à mão e sempre parametrizado (`%s`), o que impede SQL injection
- **Pydantic**: modelos de entrada e saída, com validação (ex.: CPF com 11 dígitos, sexo `F`/`M`)
- **JWT (PyJWT) + Argon2 (pwdlib)**: login com token e senhas guardadas só como hash
- **pytest**: 26 testes de integração contra o banco real

## Rotas

🔒 = exige login (cabeçalho `Authorization: Bearer <token>`). As leituras são abertas.

| Método | Rota | O que faz |
|---|---|---|
| POST | `/auth/token` | Login: troca usuário e senha por um token (válido por 60 min) |
| GET | `/auth/me` 🔒 | Mostra quem está logado |
| GET | `/clientes?nome=` | Lista clientes; `nome` filtra por parte do nome |
| GET | `/clientes/{cpf}` | Cliente com telefones e animais |
| POST | `/clientes` 🔒 | Cadastra cliente |
| PUT | `/clientes/{cpf}` 🔒 | Atualiza cliente |
| DELETE | `/clientes/{cpf}` 🔒 | Remove cliente (409 se ainda tiver animais) |
| GET | `/animais?especie=` | Lista animais; `especie` filtra (ex.: `Gato`) |
| GET | `/animais/{id}` | Detalha um animal |
| POST | `/animais` 🔒 | Cadastra animal (409 se o dono não existir) |
| GET | `/veterinarios?especialidade=` | Veterinários com a filial onde trabalham |
| GET | `/consultas?data=AAAA-MM-DD` | Agenda com animal, tutor e veterinário |
| GET | `/consultas/{id}` | Prontuário: exames, receitas e pagamento |
| POST | `/consultas` 🔒 | Agenda consulta |
| GET | `/relatorios/faturamento-por-filial` | Faturamento por filial |

### Como funciona o login

1. O cliente envia usuário e senha para `POST /auth/token`.
2. A API compara a senha com o **hash Argon2** guardado na tabela `usuario_api` (a senha em texto puro nunca é gravada) e devolve um **token JWT** assinado.
3. Nas rotas 🔒, o cliente manda `Authorization: Bearer <token>`. A API confere a assinatura e a validade; sem token, com token falsificado ou vencido, a resposta é `401`.

Senha errada e usuário inexistente recebem a mesma resposta, no mesmo tempo, para a API não revelar quais usuários existem.

### Como os erros viram respostas HTTP

| Situação | MariaDB | API |
|---|---|---|
| Sem login, token inválido ou vencido | — | `401 Unauthorized` |
| Registro não encontrado | — | `404 Not Found` |
| Dado inválido (ex.: CPF com 3 dígitos) | — | `422 Unprocessable Entity` |
| CPF ou CNPJ repetido | erro 1062 (chave duplicada) | `409 Conflict` |
| Animal com dono inexistente | erro 1452 (chave estrangeira) | `409 Conflict` |
| Remover cliente que tem animal | erro 1451 (chave estrangeira) | `409 Conflict` |

## Como rodar

Pré-requisitos: Python 3.11+ e o banco `clinica` carregado com `sql/01_schema.sql` e `sql/02_dados_exemplo.sql` (veja o [README principal](../README.md#como-rodar)).

**1. Prepare o banco**, como root no console do MariaDB. Crie a tabela de login e um usuário do banco só para a API, com permissão apenas para ler e gravar dados:

```sql
SOURCE sql/04_usuarios_api.sql;
CREATE USER 'zoolife_api'@'localhost' IDENTIFIED BY 'escolha-uma-senha';
GRANT SELECT, INSERT, UPDATE, DELETE ON clinica.* TO 'zoolife_api'@'localhost';
```

**2. Configure.** Dentro da pasta `api/`, copie `.env.example` para `.env`, coloque a senha do banco e gere uma chave para o `JWT_SECRET`:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

O `.env` fica fora do Git.

**3. Instale as dependências** (dentro da pasta `api/`).

No Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

No Linux/macOS:

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

**4. Crie o seu usuário de login.** A senha é pedida no terminal e não aparece enquanto você digita:

```powershell
.\.venv\Scripts\python.exe -m app.criar_usuario admin
```

**5. Suba a API:**

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

**6. Abra a documentação interativa** em http://127.0.0.1:8000/docs. Para usar as rotas 🔒, clique em **Authorize**, informe usuário e senha e confirme.

**Testes** (criam e apagam o próprio usuário de login):

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

## Exemplos

`GET /consultas/1`, o prontuário de uma consulta, junta 8 tabelas: consulta, animal, cliente, veterinário, exame, receita, medicamento e pagamento.

```json
{
  "id": 1,
  "data_hora": "2026-06-08T10:00:00",
  "sintomas": "Febre e vomito",
  "valor": "150.00",
  "animal_id": 1,
  "animal": "Zoe Maria",
  "tutor": "Mariana Alves",
  "vet_cpf": "45561230988",
  "veterinario": "Dr. Roberto",
  "exames": [
    { "tipo": "Hemograma", "resultado": "Alterado - Infeccao", "data": "2026-06-08" }
  ],
  "receitas": [
    { "medicamento": "Antibiotico Pet", "dosagem": "1 comprimido", "frequencia": "De 12 em 12 horas" }
  ],
  "pagamento": { "forma": "Pix", "valor": "150.00", "data": "2026-06-08" }
}
```

`POST /animais` com um dono que não existe:

```json
// 409 Conflict
{ "detail": "Referência inválida: o registro relacionado não existe." }
```

`POST /clientes` sem login:

```json
// 401 Unauthorized
{ "detail": "Not authenticated" }
```

## Estrutura

```
api/
├── app/
│   ├── main.py           # cria a aplicação e traduz erros do banco em 409
│   ├── auth.py           # login, geração e validação do token JWT
│   ├── criar_usuario.py  # comando para criar usuários de login
│   ├── db.py             # conexão com o MariaDB (lê o .env)
│   ├── schemas.py        # modelos Pydantic de entrada e saída
│   └── routers/          # uma rota por assunto
│       ├── clientes.py
│       ├── animais.py
│       ├── veterinarios.py
│       ├── consultas.py
│       └── relatorios.py
├── tests/test_api.py     # 26 testes de integração
├── requirements.txt
└── .env.example
```
