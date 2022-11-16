#coding:utf-8
__version__ = "0.0.1"

default_modules = ['users','bodega','pqr','venta']


def init_app(app, enabled_modules=None, **kwargs):
    from importlib import import_module
    if enabled_modules is not None:
        enabled_modules.extend(default_modules)
    else:
        enabled_modules = default_modules
    res = []
    for module_name in enabled_modules:
        res.append(import_module(f'.{module_name}', package=__name__))
    # el init app se hace luego de importar todos los modulos para que
    # todas las tablas sean accesible antes de las rutas.
    for r in res:
        r.init_app(app, **kwargs)
