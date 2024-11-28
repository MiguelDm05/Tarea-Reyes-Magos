# schemas.py
from pydantic import BaseModel
from typing import List, Optional


class UsuarioBase(BaseModel):
    id: int
    nombre: str
    edad: int


class UsuarioCreate(BaseModel):
    nombre: str
    edad: int


class Usuario(UsuarioBase):

    class Config:
        orm_mode = True


class ReyMagoBase(BaseModel):
    id: int
    nombre: str


class ReyMagoCreate(BaseModel):
    nombre: str


class ReyMago(ReyMagoBase):
    
    class Config:
        orm_mode = True


class JugueteBase(BaseModel):
    id: int
    nombre: str
    imagen: str


class JugueteCreate(BaseModel):
    nombre: str
    imagen: str


class Juguete(JugueteBase):

    class Config:
        orm_mode = True


class CartaBase(BaseModel):
    id: int
    usuario_id: int
    rey_mago_id: int
    juguetes_ids: List[int]

    class Config:
        orm_mode = True


class CartaCreate(BaseModel):
    usuario_id: int
    rey_mago_id: int
    juguetes_ids: List[int]

    class Config:
        orm_mode = True


class Carta(CartaBase):
    id: int

    class Config:
        orm_mode = True
