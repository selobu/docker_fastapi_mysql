# coding:utf-8
__all__ = ['createusers']
from config import settings
from sqlmodel import Session, select
from tools import digest
from json import dumps

def setpqroptions():
    Tb = settings.app.Tb
    pqrs = [{'tipo': 'Peticion'},
            {'tipo': 'Queja'},
            {'tipo': 'Reclamo'},
            {'tipo': 'Cotización'},
            {'tipo': 'Asesoría'},
            {'tipo': 'Agradecimientos'}]
    tipos = [t['tipo'] for t in pqrs]
    with Session(settings.engine) as session:
        not2add = select(Tb.TipoSolicitud.tipo).filter(
            Tb.TipoSolicitud.tipo.in_(tipos))
        not2add = session.exec(not2add).all()
        # testing under heroku server
        # raise Exception(dumps(session.exec(select(Tb.User.correo)).all()))
        toadd = [pqr for pqr in pqrs if pqr['tipo'] not in not2add]
        for pqr in toadd:
            session.add(Tb.TipoSolicitud(**pqr))
        session.commit()
        
def createusers():
    Tb = settings.app.Tb
    default_users = [{
        "nombres": "selobu",
        "apellidos": "John Doe",
        "correo": "selobu@gmail.com",
        "cedula": "123213",
        "departamento": "Cundinamarca",
        "municipio": "cota",
        "direccion": "calle",
        "activo": True,
        "pertenecealgrupo": True,
        "password": "secret"
    },
        {
        "nombres": "johndoe",
        "apellidos": "John Doe",
        "correo": "johndoe@example.com",
        "cedula": "123214",
        "departamento": "Cundinamarca",
        "municipio": "cota",
        "direccion": "calle",
        "activo": False,
        "password": "secret"
    },
    ]
    correos= [u['correo'] for u in default_users]
    with Session(settings.engine) as session:
        not2add = select(Tb.User.correo).filter(Tb.User.correo.in_(correos))
        not2add = session.exec(not2add).all()
        # testing under heroku server
        # raise Exception(dumps(session.exec(select(Tb.User.correo)).all()))
        toadd = [usr for usr in default_users if usr['correo'] not in not2add]
        for user in toadd:
            user['password'] = digest(user['password'])
            session.add(Tb.User(**user))
        session.commit()

def fake_hash_password(password: str):
    return "fakehashed" + password