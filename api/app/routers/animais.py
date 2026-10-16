from fastapi import APIRouter, Depends, HTTPException, status

from app.db import get_db
from app.schemas import Animal, AnimalIn

router = APIRouter(prefix="/animais", tags=["Animais"])

COLUNAS = """Animal_ID AS id, Nome AS nome, Especie AS especie, Raca AS raca,
             MicroChip AS microchip, Sexo AS sexo, Dono_CPF AS dono_cpf"""


@router.get("", response_model=list[Animal], summary="Lista animais")
def listar(especie: str | None = None, db=Depends(get_db)):
    """Lista os animais. `especie` filtra por espécie exata (ex.: Gato)."""
    sql = f"SELECT {COLUNAS} FROM animal"
    params = []
    if especie:
        sql += " WHERE Especie = %s"
        params.append(especie)
    sql += " ORDER BY Nome"
    with db.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


@router.get("/{animal_id}", response_model=Animal, summary="Detalha um animal")
def obter(animal_id: int, db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute(f"SELECT {COLUNAS} FROM animal WHERE Animal_ID = %s", (animal_id,))
        animal = cur.fetchone()
    if animal is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Animal não encontrado")
    return animal


@router.post("", response_model=Animal, status_code=status.HTTP_201_CREATED, summary="Cadastra um animal")
def criar(dados: AnimalIn, db=Depends(get_db)):
    """Cadastra um animal. Se o `dono_cpf` não existir, retorna 409 (chave estrangeira)."""
    with db.cursor() as cur:
        cur.execute(
            "INSERT INTO animal (Nome, Especie, Raca, MicroChip, Sexo, Dono_CPF) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (dados.nome, dados.especie, dados.raca, dados.microchip, dados.sexo, dados.dono_cpf),
        )
        novo_id = cur.lastrowid
    db.commit()
    return {"id": novo_id, **dados.model_dump()}
