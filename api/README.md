# Zoolife API

API REST em **Python + FastAPI** sobre o banco de dados [`clinica`](../README.md) do Zoolife (MariaDB). Ela expõe clientes, animais, veterinários, consultas e relatórios, e traduz as regras do banco (chaves primárias e estrangeiras) em respostas HTTP claras.

## Tecnologias

- **Python 3.13** e **FastAPI**: rotas, validação dos dados e documentação automática (Swagger)
- **PyMySQL**: conexão com o MariaDB, com SQL escrito à mão e sempre parametrizado (`%s`), o que impede SQL injection
- **Pydantic**: modelos de entrada e saída, com validação (ex.: CPF com 11 dígitos, sexo `F`/`M`)
- **pytest**: 16 testes de integração contra o banco real

## Rotas

| Método | Rota | O que faz |
|---|---|---|
| GET | `/clientes?nome=` | Lista clientes; `nome` filtra por parte do nome |
| GET | `/clientes/{cpf}` | Cliente com telefones e animais |
| POST | `/clientes` | Cadastra cliente |
| PUT | `/clientes/{cpf}` | Atualiza cliente |
| DELETE | `/clientes/{cpf}` | Remove cliente (409 se ainda tiver animais) |
| GET | `/animais?especie=` | Lista animais; `especie` filtra (ex.: `Gato`) |
| GET | `/animais/{id}` | Detalha um animal |
| POST | `/animais` | Cadastra animal (409 se o dono não existir) |
| GET | `/veterinarios?especialidade=` | Veterinários com a filial onde trabalham |
| GET | `/consultas?data=AAAA-MM-DD` | Agenda com animal, tutor e veterinário |
| GET | `/consultas/{id}` | Prontuário: exames, receitas e pagamento |
| POST | `/consultas` | Agenda consulta |
| GET | `/relatorios/faturamento-por-filial` | Faturamento por filial |

### Como os erros do banco viram respostas HTTP

| Situação | MariaDB | API |
|---|---|---|
| Registro não encontrado | — | `404 Not Found` |
| Dado inválido (ex.: CPF com 3 dígitos) | — | `422 Unprocessable Entity` |
| CPF ou CNPJ repetido | erro 1062 (chave duplicada) | `409 Conflict` |
| Animal com dono inexistente | erro 1452 (chave estrangeira) | `409 Conflict` |
| Remover cliente que tem animal | erro 1451 (chave estrangeira) | `409 Conflict` |

## Como rodar

Pré-requisitos: Python 3.11+ e o banco `clinica` carregado com `sql/01_schema.sql` e `sql/02_dados_exemplo.sql` (veja o [README principal](../README.md#como-rodar)).

**1. Crie um usuário do banco só para a API**, com permissão apenas para ler e gravar dados. No console do MariaDB, como root:

```sql
CREATE USER 'zoolife_api'@'localhost' IDENTIFIED BY 'escolha-uma-senha';
GRANT SELECT, INSERT, UPDATE, DELETE ON clinica.* TO 'zoolife_api'@'localhost';
```

**2. Configure a conexão.** Dentro da pasta `api/`, copie `.env.example` para `.env` e coloque a senha escolhida. O `.env` fica fora do Git.

**3. Instale as dependências e suba a API** (dentro da pasta `api/`).

No Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

No Linux/macOS:

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/uvicorn app.main:app --reload
```

**4. Abra a documentação interativa** em http://127.0.0.1:8000/docs. Ali dá para testar todas as rotas pelo navegador.

**Testes:**

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

## Exemplo

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

## Estrutura

```
api/
├── app/
│   ├── main.py          # cria a aplicação e traduz erros do banco em 409
│   ├── db.py            # conexão com o MariaDB (lê o .env)
│   ├── schemas.py       # modelos Pydantic de entrada e saída
│   └── routers/         # uma rota por assunto
│       ├── clientes.py
│       ├── animais.py
│       ├── veterinarios.py
│       ├── consultas.py
│       └── relatorios.py
├── tests/test_api.py    # 16 testes de integração
├── requirements.txt
└── .env.example
```
