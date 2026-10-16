from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import usuario_atual
from app.db import get_db
from app.respostas import CONSULTA_NAO_ENCONTRADA, REFERENCIA_INVALIDA, SEM_LOGIN
from app.schemas import Consulta, ConsultaDetalhe, ConsultaIn

router = APIRouter(prefix="/consultas", tags=["Consultas"])
LOGIN = [Depends(usuario_atual)]  # rotas de escrita exigem token

# A consulta guarda só os IDs/CPFs; os JOINs trazem os nomes do animal,
# do tutor e do veterinário.
SELECT_CONSULTA = """
    SELECT c.ConsultaID AS id, c.data_hora, c.sintomas, c.valor,
           c.Animal_ID AS animal_id, a.Nome AS animal, cl.Nome_Cli AS tutor,
           c.Vet_CPF AS vet_cpf, v.Nome AS veterinario
    FROM consulta c
    JOIN animal a      ON a.Animal_ID = c.Animal_ID
    JOIN cliente cl    ON cl.CPF      = a.Dono_CPF
    JOIN veterinario v ON v.CPF       = c.Vet_CPF
"""


@router.get("", response_model=list[Consulta], summary="Agenda de consultas")
def listar(data: date | None = None, db=Depends(get_db)):
    """Lista as consultas em ordem cronológica. `data` (AAAA-MM-DD) filtra por dia."""
    sql = SELECT_CONSULTA
    params = []
    if data:
        sql += " WHERE DATE(c.data_hora) = %s"
        params.append(data)
    sql += " ORDER BY c.data_hora"
    with db.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


@router.get("/{consulta_id}", response_model=ConsultaDetalhe, summary="Prontuário de uma consulta",
            responses=CONSULTA_NAO_ENCONTRADA)
def obter(consulta_id: int, db=Depends(get_db)):
    """Retorna a consulta com os exames, as receitas e o pagamento."""
    with db.cursor() as cur:
        cur.execute(SELECT_CONSULTA + " WHERE c.ConsultaID = %s", (consulta_id,))
        consulta = cur.fetchone()
        if consulta is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Consulta não encontrada")

        cur.execute(
            "SELECT tipo_exame AS tipo, Resultado AS resultado, data_Exame AS data "
            "FROM exame WHERE ConsultaID = %s ORDER BY Exame_ID",
            (consulta_id,),
        )
        consulta["exames"] = cur.fetchall()

        cur.execute(
            "SELECT m.Nome AS medicamento, r.Dosagem AS dosagem, r.Frequencia AS frequencia "
            "FROM receita r JOIN medicamento m ON m.MedicamentoID = r.Medicamento_ID "
            "WHERE r.ConsultaID = %s ORDER BY r.Receita_ID",
            (consulta_id,),
        )
        consulta["receitas"] = cur.fetchall()

        cur.execute(
            "SELECT Forma_Pagamento AS forma, Valor AS valor, Data_Pagamento AS data "
            "FROM pagamento WHERE ConsultaID = %s",
            (consulta_id,),
        )
        consulta["pagamento"] = cur.fetchone()
    return consulta


@router.post("", response_model=Consulta, status_code=status.HTTP_201_CREATED, summary="Agenda uma consulta",
             dependencies=LOGIN, responses={**SEM_LOGIN, **REFERENCIA_INVALIDA})
def criar(dados: ConsultaIn, db=Depends(get_db)):
    """Agenda uma consulta. Animal ou veterinário inexistente retorna 409."""
    with db.cursor() as cur:
        cur.execute(
            "INSERT INTO consulta (data_hora, sintomas, valor, Animal_ID, Vet_CPF) "
            "VALUES (%s, %s, %s, %s, %s)",
            (dados.data_hora, dados.sintomas, dados.valor, dados.animal_id, dados.vet_cpf),
        )
        novo_id = cur.lastrowid
        db.commit()
        cur.execute(SELECT_CONSULTA + " WHERE c.ConsultaID = %s", (novo_id,))
        return cur.fetchone()
