"""Modelos de entrada e saída da API.

Os nomes dos campos são mais amigáveis que os das colunas (ex.: `nome_animal`
em vez de `Nome_Ani`); a tradução é feita com aliases nas consultas SQL.
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field

CPF = Field(pattern=r"^\d{11}$", description="Somente os 11 dígitos", examples=["19032343550"])


# ---------- Cliente ----------
class ClienteIn(BaseModel):
    nome: str = Field(max_length=80, examples=["Mariana Alves"])
    email: str | None = Field(default=None, max_length=40, examples=["cliente01@example.com"])
    endereco: str | None = Field(default=None, max_length=255, examples=["Rua Flor 69"])
    cep: str | None = Field(default=None, max_length=40, examples=["21080345"])
    nome_animal: str | None = Field(default=None, max_length=40, examples=["Zoe Maria"])


class ClienteCriar(ClienteIn):
    cpf: str = CPF


class Cliente(ClienteIn):
    cpf: str


class AnimalResumo(BaseModel):
    id: int
    nome: str | None
    especie: str | None


class ClienteDetalhe(Cliente):
    telefones: list[str]
    animais: list[AnimalResumo]


# ---------- Animal ----------
class AnimalIn(BaseModel):
    nome: str = Field(max_length=70, examples=["Thor"])
    especie: str | None = Field(default=None, max_length=40, examples=["Cachorro"])
    raca: str | None = Field(default=None, max_length=40, examples=["Beagle"])
    microchip: Literal["Sim", "Nao"] | None = None
    sexo: Literal["F", "M"] | None = None
    dono_cpf: str = CPF


class Animal(AnimalIn):
    id: int


# ---------- Veterinário ----------
class Veterinario(BaseModel):
    cpf: str
    nome: str | None
    crmv: int | None
    especialidade: str | None
    filial: str


# ---------- Consulta ----------
class ConsultaIn(BaseModel):
    data_hora: datetime = Field(examples=["2026-06-11T09:30:00"])
    sintomas: str | None = Field(default=None, max_length=255, examples=["Vômito e apatia"])
    valor: Decimal = Field(ge=0, max_digits=10, decimal_places=2, examples=["150.00"])
    animal_id: int
    vet_cpf: str = CPF


class Consulta(BaseModel):
    id: int
    data_hora: datetime
    sintomas: str | None
    valor: Decimal
    animal_id: int
    animal: str | None
    tutor: str | None
    vet_cpf: str
    veterinario: str | None


class Exame(BaseModel):
    tipo: str | None
    resultado: str | None
    data: date | None


class Receita(BaseModel):
    medicamento: str | None
    dosagem: str | None
    frequencia: str | None


class Pagamento(BaseModel):
    forma: str | None
    valor: Decimal | None
    data: date | None


class ConsultaDetalhe(Consulta):
    exames: list[Exame]
    receitas: list[Receita]
    pagamento: Pagamento | None


# ---------- Relatórios ----------
class FaturamentoFilial(BaseModel):
    filial: str
    consultas: int
    faturamento: Decimal
