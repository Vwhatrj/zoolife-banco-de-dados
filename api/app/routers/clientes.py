from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.auth import usuario_atual
from app.db import get_db
from app.schemas import Cliente, ClienteCriar, ClienteDetalhe, ClienteIn

router = APIRouter(prefix="/clientes", tags=["Clientes"])
LOGIN = [Depends(usuario_atual)]  # rotas de escrita exigem token

COLUNAS = """CPF AS cpf, Nome_Cli AS nome, email, End_DESC AS endereco,
             End_CEP AS cep, Nome_Ani AS nome_animal"""


@router.get("", response_model=list[Cliente], summary="Lista clientes")
def listar(nome: str | None = None, db=Depends(get_db)):
    """Lista os clientes em ordem alfabética. `nome` filtra por parte do nome (LIKE)."""
    sql = f"SELECT {COLUNAS} FROM cliente"
    params = []
    if nome:
        sql += " WHERE Nome_Cli LIKE %s"
        params.append(f"%{nome}%")
    sql += " ORDER BY Nome_Cli"
    with db.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


@router.get("/{cpf}", response_model=ClienteDetalhe, summary="Detalha um cliente")
def obter(cpf: str, db=Depends(get_db)):
    """Retorna o cliente com seus telefones e animais."""
    with db.cursor() as cur:
        cur.execute(f"SELECT {COLUNAS} FROM cliente WHERE CPF = %s", (cpf,))
        cliente = cur.fetchone()
        if cliente is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Cliente não encontrado")
        cur.execute("SELECT NumeroCEL FROM telefone WHERE Cli_CPF = %s ORDER BY Tel_ID", (cpf,))
        cliente["telefones"] = [linha["NumeroCEL"] for linha in cur.fetchall()]
        cur.execute(
            "SELECT Animal_ID AS id, Nome AS nome, Especie AS especie "
            "FROM animal WHERE Dono_CPF = %s ORDER BY Nome",
            (cpf,),
        )
        cliente["animais"] = cur.fetchall()
    return cliente


@router.post("", response_model=Cliente, status_code=status.HTTP_201_CREATED, summary="Cadastra um cliente",
             dependencies=LOGIN)
def criar(dados: ClienteCriar, db=Depends(get_db)):
    """Cadastra um cliente. CPF repetido retorna 409."""
    with db.cursor() as cur:
        cur.execute(
            "INSERT INTO cliente (CPF, Nome_Cli, email, End_DESC, End_CEP, Nome_Ani) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (dados.cpf, dados.nome, dados.email, dados.endereco, dados.cep, dados.nome_animal),
        )
    db.commit()
    return dados


@router.put("/{cpf}", response_model=Cliente, summary="Atualiza um cliente", dependencies=LOGIN)
def atualizar(cpf: str, dados: ClienteIn, db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("SELECT 1 FROM cliente WHERE CPF = %s", (cpf,))
        if cur.fetchone() is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Cliente não encontrado")
        cur.execute(
            "UPDATE cliente SET Nome_Cli = %s, email = %s, End_DESC = %s, End_CEP = %s, Nome_Ani = %s "
            "WHERE CPF = %s",
            (dados.nome, dados.email, dados.endereco, dados.cep, dados.nome_animal, cpf),
        )
    db.commit()
    return {"cpf": cpf, **dados.model_dump()}


@router.delete("/{cpf}", status_code=status.HTTP_204_NO_CONTENT, summary="Remove um cliente",
               dependencies=LOGIN)
def remover(cpf: str, db=Depends(get_db)):
    """Remove um cliente. Se ele ainda tiver animais ou telefones, retorna 409:
    a chave estrangeira do banco impede deixar registros órfãos."""
    with db.cursor() as cur:
        apagados = cur.execute("DELETE FROM cliente WHERE CPF = %s", (cpf,))
    db.commit()
    if apagados == 0:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Cliente não encontrado")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
