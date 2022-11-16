from pydantic import BaseSettings
from os import environ
adminpassword = environ['MYSQL_ROOT_PASSWORD']
adminuser = environ['MYSQL_ROOT_USER']
port = environ['MYSQL_PORT']
database = environ['MYSQL_DATABASE']
host = environ['MYSQL_HOST']
user = environ['MYSQL_USER']
userpassword = environ['MYSQL_PASSWORD']

class Settings(BaseSettings):
    api_name: str = "Backend api"
    version: str = "0.0.1"
    api_description: str = "[source code](https://github.com/selobu/backend_sena_docker)"
    admin_email: str = ""
    items_per_user: int = 50
    database_uri: str = "sqlite:///database.db"
    api_contact: object = {'name': 'Sebastian López Buriticá', 'email': 'sebastian.lopez@gestionhseq.com',
                        'url': 'https://gestionhseq.com'}
    database_user_uri: str = f"mariadb+pymysql://{user}:{userpassword}@{host}:{port}/{database}"
    database_maria_uri: str = f"mariadb+pymysql://{adminuser}:{adminpassword}@{host}:{port}/{database}"
    app: object={}
    engine: object={}

settings = Settings()