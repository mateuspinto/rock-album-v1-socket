import routes as rt


def router(request, database):
    MW = {
        'login': rt.login,
        'register': rt.register,
        'is_admin': rt.is_admin,
        'op': rt.op,
        'unop': rt.unop,
    }

    return MW[request['method']](request, database)
