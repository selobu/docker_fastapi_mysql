# coding: utf-8
from os import environ
from sys import path
from os.path import abspath
if abspath('.') not in path:
    path.append(abspath('.'))
from fake import createusers, setpqroptions
from main import Tb, settings
from sqlmodel import create_engine, SQLModel

engine = create_engine(settings.database_maria_uri)
# creating database structure
SQLModel.metadata.create_all(engine)

# populating structure
createusers()
setpqroptions()
print("//----db updated----//")
