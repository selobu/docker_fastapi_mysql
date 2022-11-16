from fastapi import status, Depends, HTTPException,\
    APIRouter
from fastapi.security import OAuth2PasswordBearer
# from fake import fake_users_db
from tools import paginate_parameters, generate_random, sendmail
from typing import Union, List
from config import settings
from main import app
from sqlmodel import Session, select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/ventas",
    tags=["Ventas"],
    responses={404: {"description": "Not found"}},
)


Tb = settings.app.Tb
engine = settings.engine


@router.get("/", response_model=List[Tb.Venta])
async def read_ventas(commons: dict = Depends(paginate_parameters),
                      token: str = Depends(oauth2_scheme)):
    email = token
    limit = commons['limit']
    with Session(engine) as session:
        res = select(Tb.Venta).limit(limit)
        ventas = session.exec(res).all()
        # se relacionan los productos a la venta
    return ventas


@router.post("/comprador", response_model=Tb.Comprador)
async def registrar_comprador(comprador: Tb.Comprador_register):
    keys2update = list(comprador.__fields__.keys())
    keys2update = [k for k in keys2update if k !=
                   'id' and hasattr(Tb.Comprador, k)]
    with Session(engine) as session:
        req = Tb.Comprador(**dict((k, getattr(comprador, k))
                                  for k in keys2update))
        session.add(req)
        session.commit()
        session.refresh(req)
    # TODO : enviar correo con url para validar
    return req


@router.put("/comprador/{comprador_id}", response_model=Tb.Comprador)
async def actualizar_comprador(comprador_id: int, comprador: Tb.Comprador_register):
    keys2update = list(comprador.__fields__.keys())
    keys2update = [k for k in keys2update if k !=
                   'id' and hasattr(Tb.Comprador, k)]
    with Session(engine) as session:
        res = select(Tb.Comprador).filter(Tb.Comprador.id == comprador_id)
        comp = session.exec(res).one()
        for k in keys2update:
            setattr(comp, k, getattr(comprador, k))
        session.add(comp)
        # se crea punto de validacion
        key = generate_random()
        validate = Tb.ValidateMail(correo=comprador.correo, key=key)
        session.add(validate)
        session.commit()
        sendmail(comprador.correo, 'Código de validación',
                 f'No compartas este código {key}')
        session.refresh(comp)
    return comp


@router.get("/comprador/", response_model=List[Tb.Comprador])
async def leer_compradores(token=Depends(oauth2_scheme), commons=Depends(paginate_parameters)):
    limit = commons['limit']
    with Session(engine) as session:
        res = select(Tb.Comprador).limit(limit)
        res = session.exec(res).all()
    return res


@router.post("/validatemail/{comprador_id}", response_model=bool)
async def validate_mail_comprador(comprador_id: int, validationcode: str):
    with Session(engine) as session:
        res = select(Tb.Comprador).limit(1)
        res = session.exec(res).all()
    return True


@router.get("/comprador/{comprador_id}", response_model=Tb.Comprador)
async def leer_comprador(comprador_id: int, token=Depends(oauth2_scheme)):
    with Session(engine) as session:
        res = select(Tb.Comprador).filter(Tb.Comprador.id == comprador_id)
        res = session.exec(res).one()
    return res


@router.post("/carrito/{comprador_id}", response_model=Tb.Venta)
async def compra_registrar(comprador_id: int, productos: List[int]):
    with Session(engine) as session:
        # se verifica que exista el comprador y el correo esté validado
        _res = select(Tb.Comprador).\
            where(Tb.Comprador.id == comprador_id)
        #  TODO
        # .where(Tb.Comprador.correovalidado==True)

        session.exec(_res)

        # se filtran los productos que existen y no esten registrados en una venta
        _res = select(Tb.Producto).where(Tb.Producto.id.in_(productos)).\
            where(Tb.Producto.ventaid == None)
        productos = session.exec(_res).all()

        # se registra la compra
        venta = Tb.Venta(comprador=comprador_id)
        session.add(venta)
        session.commit()
        session.refresh(venta)
        compraid = venta.id
        for pd in productos:
            pd.ventaid = compraid
        session.add_all(productos)
        session.commit()
        session.refresh(venta)
        # se relacionan los productos a la venta
    return venta


@router.get("/carritoproductos/{venta_id}", response_model=List[Tb.Producto])
async def get_compra_productos(venta_id: int):
    with Session(engine) as session:
        res = select(Tb.Producto).\
            where(Tb.Producto.ventaid == Tb.Venta.id).\
            filter(Tb.Venta.id == venta_id)
        pds = session.exec(res).all()
        # se relacionan los productos a la venta
    return pds


@router.post("/carritoproductos/{venta_id}", response_model=bool)
async def set_compra_productos(venta_id: int, productos: List[int]):
    """Actualiza el listado de productos de un carrito"""
    with Session(engine) as session:
        res = select(Tb.Producto).\
            where(Tb.Producto.ventaid == Tb.Venta.id).\
            filter(Tb.Venta.id == venta_id)
        pds = session.exec(res).all()
        for pd in pds:
            pd.ventaid = None
        session.add_all(pds)
        session.commit()
        # se consultan los productos nuevos seleccionados
        res = select(Tb.Producto).\
            where(Tb.Producto.id.in_(productos)).\
            filter(Tb.Producto.ventaid == None)
        newpds = session.exec(res).all()
        for pd in newpds:
            pd.ventaid = venta_id
        session.add_all(newpds)
        # se relacionan los productos a la venta
        session.commit()
    return True


@router.delete("/carrito/{venta_id}", response_model=bool)
async def delete_compra_productos(venta_id: int):
    """Elimina carrito de venta si no ha sido facturado"""
    with Session(engine) as session:
        res = select(Tb.Venta).where(Tb.Venta.id == venta_id).\
            where(Tb.Venta.recibido == False).\
            where(Tb.Venta.responsableEnviar == None)
        venta = session.exec(res).one()

        res = select(Tb.Producto).where(Tb.Producto.ventaid == venta_id)
        pds = session.exec(res).all()
        # se elimina la asociacion de los  los productos asociados a la venta
        for pd in pds:
            pd.ventaid = None
        session.add_all(pds)
        session.delete(venta)
        session.commit()
        return True


@router.post("/carrito/{venta_id}/{user_id}", response_model=Tb.Venta)
async def compra_asign_resp(venta_id: int, user_id: int, token=Depends(oauth2_scheme)):
    """Asociar responsable de la venta"""
    with Session(engine) as session:
        # se verifica que la venta exista
        res = select(Tb.Venta).where(Tb.Venta.id == venta_id)
        venta = session.exec(res).one()

        # se verifica que el usuario exista
        res = select(Tb.User).where(Tb.User.id == user_id)
        session.exec(res).one()

        venta.responsableEnviar = user_id
        session.add(venta)
        session.commit()
        session.refresh(venta)
    return venta


@router.post("/carritotramit/{venta_id}", response_model=Tb.Venta)
async def compra_tramit(venta_id: int, ventatramit: Tb.VentaTramit, token=Depends(oauth2_scheme)):
    """tramitar la venta"""
    email = token
    with Session(engine) as session:
        # se consulta el usuario sea responsable de la venta
        res = select(Tb.Venta, Tb.User.id).\
            where(Tb.Venta.responsableEnviar == Tb.User.id).\
            where(Tb.User.correo == email)

        venta, userid = session.exec(res).one()
        # se actualiza la venta
        keys2update = list(ventatramit.__fields__.keys())
        keys2update = [k for k in keys2update if k !=
                       'id' and hasattr(Tb.Venta, k)]
        for item in keys2update:
            setattr(venta, item, getattr(ventatramit, item))
        session.add(venta)
        session.commit()
        session.refresh(venta)
    return venta
