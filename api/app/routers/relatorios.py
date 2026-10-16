from fastapi import APIRouter, Depends

from app.db import get_db
from app.schemas import FaturamentoFilial

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])


@router.get("/faturamento-por-filial", response_model=list[FaturamentoFilial], summary="Faturamento por filial")
def faturamento_por_filial(db=Depends(get_db)):
    """Soma os pagamentos de cada filial (JOIN de 4 tabelas + GROUP BY)."""
    with db.cursor() as cur:
        cur.execute("""
            SELECT e.Nome AS filial,
                   COUNT(p.Pagamento_ID) AS consultas,
                   SUM(p.Valor) AS faturamento
            FROM pagamento p
            JOIN consulta c    ON c.ConsultaID = p.ConsultaID
            JOIN veterinario v ON v.CPF        = c.Vet_CPF
            JOIN empresa e     ON e.Empresa_ID = v.Empresa_ID
            GROUP BY e.Empresa_ID, e.Nome
            ORDER BY faturamento DESC, filial
        """)
        return cur.fetchall()
