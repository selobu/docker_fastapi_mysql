from typing import Optional
from tools import map_name_to_table
from config import settings
from sqlmodel import Field, SQLModel, Relationship,  Column, String, Field
from pydantic import EmailStr

Tb = settings.app.Tb


@map_name_to_table
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombres: str = Field(sa_column=Column(String(2000)))
    apellidos: str = Field(sa_column=Column(String(2000)))
    correo: EmailStr = Field(unique=True, sa_column=Column(String(100)))
    cedula: str = Field(sa_column=Column(String(2000)))
    departamento: str = Field(sa_column=Column(String(2000)))
    municipio: str = Field(sa_column=Column(String(2000)))
    direccion: str = Field(sa_column=Column(String(2000)))
    activo: bool = True
    pertenecealgrupo: bool = False
    password: str = Field(sa_column=Column(String(2000)))


@map_name_to_table
class UserOut(SQLModel):
    id: Optional[int]
    nombres: str = Field(sa_column=Column(String(2000)))
    apellidos: str = Field(sa_column=Column(String(2000)))
    correo: EmailStr = Field(sa_column=Column(String(100)))
    cedula: str = Field(sa_column=Column(String(2000)))
    departamento: str = Field(sa_column=Column(String(2000)))
    municipio: str = Field(sa_column=Column(String(2000)))
    direccion: str = Field(sa_column=Column(String(2000)))
    activo: bool = True
    pertenecealgrupo: bool = False
