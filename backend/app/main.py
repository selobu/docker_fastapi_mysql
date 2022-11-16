# coding: utf-8
from sys import path
from os.path import abspath

if abspath('.') not in path:
    path.append(abspath('.'))

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fake import createusers, setpqroptions
from tools import  Tb, digest
from fastapi.middleware.cors import CORSMiddleware
import modules
from config import settings
from sqlmodel import create_engine, SQLModel, Session, select
from os.path import isfile, exists
#import uvicorn

# print(help(FastAPI))
app = FastAPI(
    title= settings.api_name,
    version= settings.version,
    description= settings.api_description,
    contact= settings.api_contact,
    license_info={'name': 'GPL V3',
                  'url': 'https://www.gnu.org/licenses/gpl-3.0.en.html'})

# making app globally available by calling settings
settings.app = app
setattr(app,'Tb', Tb)

# create connection
engine = create_engine(settings.database_user_uri)  # database_uri)
settings.engine = engine
modules.init_app(app)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"api": "/docs","message":"please visit localhost/docs to interact with api"}

if False:
    @app.get("/creatreall")
    def create_all():
        SQLModel.metadata.create_all(engine)
        return {'message':'ok'}


    @app.get("/populatedatabase")
    def populate_database():
        createusers()
        setpqroptions()
        return {'message': 'ok'}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # getting the user
    with Session(engine) as session:
        res = select(Tb.User).filter(Tb.User.correo == form_data.username)
        user = session.exec(res).first()
        if user is None:
            HTTPException(status_code=404, detail='Usuario no encontrado')
    if digest(form_data.password) != user.password:
        raise HTTPException(
            status_code=400, detail="Usuario o contraseña equivocada")

    return {"access_token": user.correo, "token_type": "bearer"}

#if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=8000)
