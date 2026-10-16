from fastapi import APIRouter, Depends

from app.db import get_db
from app.schemas import Veterinario

router = APIRouter(prefix="/veterinarios", tags=["Veterinários"])


@router.get("", response_model=list[Veterinario], summary="Lista veterinários")
def listar(especialidade: str | None = None, db=Depends(get_db)):
    """Lista os veterinários com a filial onde trabalham (JOIN com empresa)."""
    sql = """
        SELECT v.CPF AS cpf, v.Nome AS nome, v.CRMV AS crmv,
               v.Especialidade AS especialidade, e.Nome AS filial
        FROM veterinario v
        JOIN empresa e ON e.Empresa_ID = v.Empresa_ID
    """
    params = []
    if especialidade:
        sql += " WHERE v.Especialidade = %s"
        params.append(especialidade)
    sql += " ORDER BY v.Nome"
    with db.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()
