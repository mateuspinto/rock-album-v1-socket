from functools import reduce


def login(request, database):
    DB_CUR = database.cursor()
    QUERY_RESULT = DB_CUR.execute(f'SELECT * FROM users WHERE email="{request["email"]}" AND password="{request["password"]}"')
    if reduce(lambda a, x: a + 1, QUERY_RESULT, 0) == 1:
        return {'error': 0}
    else:
        return {'error': 1, 'error_message': 'Usuário não encontrado!'}


def is_admin(request, database):
    DB_CUR = database.cursor()
    QUERY_RESULT = DB_CUR.execute(f'SELECT is_admin FROM users WHERE email="{request["email"]}" AND password="{request["password"]}"')
    if next(QUERY_RESULT)[0] == 1:
        return {'error': 0}
    else:
        return {'error': 1, 'error_message': 'Usuário não é administrador!'}


def __is_email_available(request, database):
    DB_CUR = database.cursor()
    QUERY_RESULT = DB_CUR.execute(f'SELECT * FROM users WHERE email="{request["email"]}"')
    if reduce(lambda a, x: a + 1, QUERY_RESULT, 0) == 1:
        return {'error': 1, 'error_message': 'Email já cadastrado!'}
    else:
        return {'error': 0}


def register(request, database):
    if __is_email_available(request, database)['error'] == 1:
        return {'error': 1, 'error_message': 'Falha no cadastro! Email já está em uso.'}

    DB_CUR = database.cursor()
    DB_CUR.execute(f'INSERT INTO users VALUES ("{request["email"]}", "{request["password"]}", 0, 0)')
    database.commit()
    return {'error': 0}


def op(request, database):
    DB_CUR = database.cursor()
    DB_CUR.execute(f'UPDATE users SET is_admin = 1 WHERE email="{request["target_email"]}"')
    database.commit()
    return {'error': 0}


def unop(request, database):
    DB_CUR = database.cursor()
    DB_CUR.execute(f'UPDATE users SET is_admin = 0 WHERE email="{request["target_email"]}"')
    database.commit()
    return {'error': 0}


def __exist_giftcard(request, database):
    DB_CUR = database.cursor()
    QUERY_RESULT = DB_CUR.execute(f'SELECT * FROM giftcards WHERE key="{request["giftcard_key"]}"')
    if reduce(lambda a, x: a + 1, QUERY_RESULT, 0) == 1:
        return {'error': 0}
    else:
        return {'error': 1, 'error_message': 'Giftcard não existente!'}


def create_giftcard(request, database):
    if __exist_giftcard(request, database)['error'] == 0:
        return {'error': 1, 'error_message': 'Falha na criação do Giftcard! Já existe um Giftcard com essa chave.'}

    DB_CUR = database.cursor()
    DB_CUR.execute(f'INSERT INTO giftcards VALUES ("{request["giftcard_key"]}")')
    database.commit()
    return {'error': 0}


def retrieve_giftcard(request, database):
    if __exist_giftcard(request, database)['error'] == 1:
        return {'error': 1, 'error_message': 'Falha no resgate do Giftcard! Não existe um Giftcard com essa chave.'}

    DB_CUR = database.cursor()
    DB_CUR.execute(f'UPDATE users SET coins=coins+100 WHERE email="{request["email"]}"')
    DB_CUR.execute(f'DELETE FROM giftcards WHERE key="{request["giftcard_key"]}"')
    database.commit()
    return {'error': 0}
