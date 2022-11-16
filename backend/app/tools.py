# coding:utf-8
import random
import hashlib
from typing import Union

def digest(text):
    if isinstance(text, str):
        text = bytearray(text, 'utf-8')
    hash_object = hashlib.sha256(text)
    return hash_object.hexdigest()

async def paginate_parameters(
    q: Union[str, None] = None, skip: int = 0, limit: int = 20
):
    return {"q": q, "skip": skip, "limit": limit}


class TbContainer(object):
    pass

# punto comun para acceder a las tablas
Tb = TbContainer()


def map_name_to_table(cls):
    #globals()[clase.__name__] = clase
    # table_mappers['Tb'+clase.__name__] = clase
    if hasattr(Tb, cls.__name__):
        raise Exception(f'Ya está declarada la tabla {cls.__name__}')
    setattr(Tb, cls.__name__, cls)

def generate_random(largo=6):
    # https://www.askpython.com/python/examples/generate-random-strings-in-python
    random_string = ''
    for _ in range(largo):
        # Considering only upper and lowercase letters
        random_integer = random.randint(97, 97 + 26 - 1)
        flip_bit = random.randint(0, 1)
        # Convert to lowercase if the flip bit is on
        random_integer = random_integer - 32 if flip_bit == 1 else random_integer
        # Keep appending random characters using chr(x)
        random_string += (chr(random_integer))

    return random_string


def sendmail(destination, bodycontent,*args, **kwarg):
    # TODO
    pass