from typing import Optional
from xmlrpc.client import boolean
from tools import map_name_to_table
from config import settings
from sqlmodel import Field, SQLModel, Relationship, Column, String, Field
from pydantic import EmailStr

Tb = settings.app.Tb


@map_name_to_table
class Ubicaciones(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    departamento: str = Field(sa_column=Column(String(2000)))
    centro_trabajo: str = Field(sa_column=Column(String(2000)))
    sitio: str = Field(sa_column=Column(String(2000)))
    activa: bool = True


@map_name_to_table
class Ubicaciones_register(SQLModel):
    departamento: str = Field(sa_column=Column(String(2000)))
    centro_trabajo: str = Field(sa_column=Column(String(2000)))
    sitio: str = Field(sa_column=Column(String(2000)))


@map_name_to_table
class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tipo: str = Field(sa_column=Column(String(2000)))
    responsable: Optional[int] = Field(default=None, foreign_key='user.id')
    nombre: str = Field(sa_column=Column(String(2000)))
    serial: str = Field(sa_column=Column(String(2000)))
    foto1: Optional[bytes]
    foto2: Optional[bytes]
    descripcion: str = Field(sa_column=Column(String(2000)))
    ubicacion: Optional[int] = Field(
        default=None, foreign_key='ubicaciones.id')
    activa: bool = True
    ventaid: Optional[int] = Field(default=None, foreign_key='venta.id')


@map_name_to_table
class Product_register(SQLModel):
    tipo: str = Field(sa_column=Column(String(2000)))
    responsable: Optional[int] = Field(default=None, foreign_key='user.id')
    nombre: str = Field(sa_column=Column(String(2000)))
    serial: str = Field(sa_column=Column(String(2000)))
    foto1: Optional[bytes]
    foto2: Optional[bytes]
    descripcion: str = Field(sa_column=Column(String(2000)))
    ubicacion: Optional[int] = Field(
        default=None, foreign_key='ubicaciones.id')
    activa: bool = True
