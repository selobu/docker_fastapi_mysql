from datetime import date
from typing import Optional
from xmlrpc.client import boolean
from tools import map_name_to_table
from sqlmodel import Field, SQLModel, Relationship, Column, String, Field
from pydantic import EmailStr


@map_name_to_table
class TipoSolicitud(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tipo: str = Field(unique=True, sa_column=Column(String(100)))


@map_name_to_table
class AtencionUsuario_register(SQLModel):
    nombrecompleto: str = Field(sa_column=Column(String(2000)))
    identificacion: str = Field(sa_column=Column(String(2000)))
    correocontacto: EmailStr = Field(sa_column=Column(String(100)))
    telefonocontacto: str = Field(sa_column=Column(String(2000)))
    tipoSolicitud: int = Field(foreign_key='tiposolicitud.id')
    solicitud: str = Field(sa_column=Column(String(2000)))


@map_name_to_table
class AtencionUsuario_cierre(SQLModel):
    resuelta: Optional[bool] = False
    fechasolucion: Optional[date] = Field(default=None)
    comentarioCierre: Optional[str] = Field(sa_column=Column(String(100)))


@map_name_to_table
class AtencionUsuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: date = Field(default=date.today())
    usuarioencargado: Optional[int] = Field(
        default=None, foreign_key='user.id')
    nombrecompleto: str = Field(sa_column=Column(String(2000)))
    identificacion: str = Field(sa_column=Column(String(2000)))
    correocontacto: EmailStr = Field( sa_column=Column(String(100)))
    telefonocontacto: str = Field(sa_column=Column(String(2000)))
    tipoSolicitud: int = Field(foreign_key='tiposolicitud.id')
    solicitud: str = Field(sa_column=Column(String(2000)))
    resuelta: Optional[bool] = False
    fechasolucion: Optional[date] = Field(default=None)
    comentarioCierre: Optional[str] = Field(sa_column=Column(String(100)))
