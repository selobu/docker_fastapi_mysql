from fastapi import status, Depends, HTTPException,\
    APIRouter
from fastapi.security import OAuth2PasswordBearer
# from fake import fake_users_db
from tools import paginate_parameters
from typing import Union, List
from config import settings
from main import app
from sqlmodel import Session, select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/Solicitud",
    tags=["Solicitud"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)


Tb = settings.app.Tb
engine = settings.engine


@router.get("/", response_model=List[Tb.AtencionUsuario])
async def read_all_requirements(token: str = Depends(oauth2_scheme),
                                commons: dict = Depends(paginate_parameters)):
    limit = commons['limit']
    with Session(engine) as session:
        res = select(Tb.AtencionUsuario).limit(limit)
        res = session.exec(res).all()
    return res


@router.get("/{requirement_id}", response_model=Tb.AtencionUsuario)
async def read_all_requirements(requirement_id: int, oken: str = Depends(oauth2_scheme)):
    with Session(engine) as session:
        res = select(Tb.AtencionUsuario).filter(
            Tb.AtencionUsuario.id == requirement_id)
        req = session.exec(res).one()
    return req


@router.post("/publicrequirement/", response_model=Tb.AtencionUsuario)
async def public_register_requirement(requirement: Tb.AtencionUsuario_register):
    keys2update = list(requirement.__fields__.keys())
    keys2update = [k for k in keys2update if k !=
                   'id' and hasattr(Tb.AtencionUsuario, k)]
    with Session(engine) as session:
        req = Tb.AtencionUsuario(**dict((k, getattr(requirement, k))
                                        for k in keys2update))
        session.add(req)
        session.commit()
        session.refresh(req)
    return req


@router.post("/asignarresponsable/{requirement_id}/{user_id}", response_model=Tb.AtencionUsuario)
async def requirement_set_responsible(requirement_id: int, user_id: int, token: str = Depends(oauth2_scheme)):
    with Session(engine) as session:
        res = select(Tb.AtencionUsuario).filter(
            Tb.AtencionUsuario.id == requirement_id)
        req = session.exec(res).one()
        res = select(Tb.User.id).filter(
            Tb.User.id == user_id)
        session.exec(res).one()  # check if the user id exists
        req.usuarioencargado = user_id
        session.add(req)
        session.commit()
        session.refresh(req)
    return req


@router.post("/tramitar/{requirement_id}", response_model=Tb.AtencionUsuario)
async def requirement_tramit(requirement_id: int, respuesta: Tb.AtencionUsuario_cierre, token: str = Depends(oauth2_scheme)):
    email = token
    keys2update = list(respuesta.__fields__.keys())
    keys2update = [k for k in keys2update if k !=
                   'id' and hasattr(Tb.AtencionUsuario, k)]

    with Session(engine) as session:
        res = select(Tb.AtencionUsuario).filter(
            Tb.AtencionUsuario.id == requirement_id)
        req = session.exec(res).one()

        res = select(Tb.User.id).filter(
            Tb.User.correo == email)
        usrid = session.exec(res).one()
        if usrid != req.usuarioencargado:
            HTTPException(
                401, 'Solo el usuario encargado puede tramitar el requerimiento')

        for k in keys2update:
            setattr(req, k, getattr(respuesta, k))

        session.add(req)
        session.commit()
        session.refresh(req)
    return req
