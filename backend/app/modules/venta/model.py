from datetime import date
from typing import Optional
from xmlrpc.client import boolean
from tools import map_name_to_table
from sqlmodel import Field, SQLModel, Relationship, Column, String, Field
from pydantic import EmailStr


@map_name_to_table
class Comprador_register(SQLModel):
    nombrecompleto: str = Field(sa_column=Column(String(2000)))
    cedula: str = Field(sa_column=Column(String(2000)))
    direccionResidencia: str = Field(sa_column=Column(String(2000)))
    departamento: str = Field(sa_column=Column(String(2000)))
    municipio: str = Field(sa_column=Column(String(2000)))
    direccionEnvio: str = Field(sa_column=Column(String(2000)))
    correo: EmailStr= Field(sa_column=Column(String(100)))
    telefono: str = Field(sa_column=Column(String(2000)))


@map_name_to_table
class Comprador(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombrecompleto: str = Field(sa_column=Column(String(2000)))
    cedula: str = Field(sa_column=Column(String(2000)))
    direccionResidencia: str = Field(sa_column=Column(String(2000)))
    departamento: str = Field(sa_column=Column(String(2000)))
    municipio: str = Field(sa_column=Column(String(2000)))
    direccionEnvio: str = Field(sa_column=Column(String(2000)))
    correo: EmailStr = Field(unique=True, sa_column=Column(String(100)))
    telefono: str = Field(sa_column=Column(String(2000)))
    correovalidado: Optional[bool] = False


@map_name_to_table
class VentaTramit(SQLModel):
    enviado: Optional[bool] = False
    fechaEnvio: Optional[date] = Field(default=None)
    recibido: Optional[bool] = False
    facturar: Optional[bool] = False
    cancelada: Optional[bool] = False


@map_name_to_table
class Venta(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    comprador: int = Field(foreign_key='comprador.id')
    fechacompra: Optional[date] = Field(default=date.today())
    responsableEnviar: Optional[int] = Field(
        default=None, foreign_key='user.id')
    enviado: Optional[bool] = False
    fechaEnvio: Optional[date] = Field(default=None)
    recibido: Optional[bool] = False
    # la facuración se envía al correo electrónico descrito
    facturar: Optional[bool] = False
    cancelada: Optional[bool] = False


@map_name_to_table
class ValidateMail(SQLModel, table=True):
    id: int = Field(primary_key=True)
    correo: EmailStr = Field(foreign_key='comprador.id', sa_column=Column(String(100)))
    key: str = Field(sa_column=Column(String(2000)))
