# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from db import Base


class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    edad = Column(Integer)


class ReyMago(Base):
    __tablename__ = "reyes_magos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)


class Juguete(Base):
    __tablename__ = "juguetes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    imagen = Column(String)


class Carta(Base):
    __tablename__ = "cartas"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    rey_mago_id = Column(Integer, ForeignKey("reyes_magos.id"))

    usuario = relationship("Usuario")
    rey_mago = relationship("ReyMago")
    juguetes = relationship("Juguete", secondary="carta_juguetes")


# Tabla asociativa entre Carta y Juguete
carta_juguetes = Table(
    "carta_juguetes",
    Base.metadata,
    Column("carta_id", Integer, ForeignKey("cartas.id")),
    Column("juguete_id", Integer, ForeignKey("juguetes.id")),
)
