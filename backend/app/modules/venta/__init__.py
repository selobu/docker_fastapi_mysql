from . import model


def init_app(app):
    from . import routes
    app.include_router(routes.router)
