import routes as rt


def router(request, database):
    MW = {
        'login': rt.login,
        'register': rt.register,
    }

    return MW[request['method']](request, database)
