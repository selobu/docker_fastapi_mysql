from fastapi import status, Depends, HTTPException, \
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
    prefix="/Producto",
    tags=["Producto"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)

Tb = settings.app.Tb
engine = settings.engine


@router.get("/", response_model=List[Tb.Producto])
async def read_products(commons: dict = Depends(paginate_parameters),
                        token: str = Depends(oauth2_scheme)):
    email = token
    limit = commons['limit']
    with Session(engine) as session:
        res = select(Tb.Producto).limit(limit)
        productos = session.exec(res).all()
    return productos


@router.get("/{product_id}", response_model=Tb.UserOut)
async def read_product_by_id(product_id: int,
                             token: str = Depends(oauth2_scheme), q: Union[str, None] = None):
    email = token
    with Session(engine) as session:
        res = select(Tb.Producto).filter(Tb.Producto.id == product_id)
        productos = session.exec(res).one()
    return productos


@router.get("/ubicacion/", response_model=List[Tb.Ubicaciones])
async def read_locations(token: str = Depends(oauth2_scheme), commons: dict = Depends(paginate_parameters)):
    email = token
    limit = commons['limit']
    with Session(engine) as session:
        res = select(Tb.Ubicaciones)
        ubicaciones = session.exec(res).all()
    return ubicaciones


@router.post("/", response_model=Tb.Producto)
async def register_product(product: Tb.Product_register, token: str = Depends(oauth2_scheme)):
    email = token
    keys2update = list(product.__fields__.keys())
    keys2update = [k for k in keys2update if k !=
                   'id' and hasattr(Tb.Producto, k)]
    with Session(engine) as session:
        pd = Tb.Producto(**dict((k, getattr(product, k)) for k in keys2update))
        session.add(pd)
        session.commit()
        session.refresh(pd)
    return pd


@router.put("/{product_id}", response_model=Tb.Producto)
async def register_product(product_id: int, product: Tb.Product_register, token: str = Depends(oauth2_scheme)):
    email = token
    keys2update = list(product.__fields__.keys())
    keys2update = [k for k in keys2update if k !=
                   'id' and hasattr(Tb.Producto, k)]
    with Session(engine) as session:
        # se consulta el producto
        res = select(Tb.Producto).filter(Tb.Producto.id == product_id)
        pd = session.exec(res).one()
        for k in keys2update:
            setattr(pd, k, getattr(product, k))
        session.add(pd)
        session.commit()
        session.refresh(pd)
    return pd


@router.post("/ubicacion/", response_model=Tb.Ubicaciones)
async def save_locations(ubicacion: Tb.Ubicaciones_register, token: str = Depends(oauth2_scheme)):
    email = token
    keys2update = list(ubicacion.__fields__.keys())
    keys2update = [k for k in keys2update if k !=
                   'id' and hasattr(Tb.Ubicaciones, k)]
    with Session(engine) as session:
        ubica = Tb.Ubicaciones(**dict((k, getattr(ubicacion, k))
                               for k in keys2update))
        session.add(ubica)
        session.commit()
        session.refresh(ubica)
    return ubica


@router.put("/ubicacion/{ubicacion_id}", response_model=Tb.Ubicaciones)
async def save_locations(ubicacion_id: int, ubicacion: Tb.Ubicaciones_register, token: str = Depends(oauth2_scheme)):
    email = token
    keys2update = list(ubicacion.__fields__.keys())
    keys2update = [k for k in keys2update if k !=
                   'id' and hasattr(Tb.Ubicaciones, k)]
    with Session(engine) as session:
        res = select(Tb.Ubicaciones).filter(Tb.Ubicaciones.id == ubicacion_id)
        ubi = session.exec(res).one()
        for k in keys2update:
            setattr(ubi, k, getattr(ubicacion, k))
        session.add(ubi)
        session.commit()
        session.refresh(ubi)
    return ubi
