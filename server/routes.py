import random


def login(request, database):
    DB_CUR = database.cursor()
    QUERY_RESULT = DB_CUR.execute(f'SELECT * FROM users WHERE email="{request["email"]}" AND password="{request["password"]}"')
    if len(list(QUERY_RESULT)) == 1:
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
    if len(list(QUERY_RESULT)) == 1:
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
    if len(list(QUERY_RESULT)) == 1:
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


def get_coins(request, database):
    DB_CUR = database.cursor()
    QUERY_RESULT = DB_CUR.execute(f'SELECT coins FROM users WHERE email="{request["email"]}"')
    return {'error': 0, 'coins': list(QUERY_RESULT)[0][0]}


def __exist_sticker_model(request, database):
    DB_CUR = database.cursor()
    QUERY_RESULT = DB_CUR.execute(f'SELECT * FROM sticker_models WHERE name="{request["sticker_model_name"]}"')
    if len(list(QUERY_RESULT)) == 1:
        return {'error': 0}
    else:
        return {'error': 1, 'error_message': 'Modelo de figurinha não existente!'}


def create_sticker_model(request, database):
    DB_CUR = database.cursor()
    DB_CUR.execute(f'INSERT INTO sticker_models VALUES ("{request["sticker_model_name"]}")')
    database.commit()
    return {'error': 0}


def print_stickers(request, database):
    if __exist_sticker_model(request, database)['error'] == 1:
        return {'error': 1, 'error_message': 'Falha na impressão das figurinhas! Não existe um modelo de figurinha com esse nome.'}

    DB_CUR = database.cursor()
    for _ in range(request["sticker_print_number"]):
        DB_CUR.execute(f'INSERT INTO sticker_prints (sticker_models_name, owner_user_name, is_pasted, is_for_sale, sale_price) VALUES ("{request["sticker_model_name"]}", "", 0, 0, 0)')
    database.commit()
    return {'error': 0}


def buy_sticker_pack(request, database):
    DB_CUR = database.cursor()

    if list(DB_CUR.execute('SELECT COUNT(*) FROM sticker_prints WHERE owner_user_name=""'))[0][0] < 2:
        return {'error': 1, 'error_message': 'Falha na compra do pacote de figurinhas! Não existe figurinhas impressas sem dono suficientes'}

    if get_coins(request, database)['coins'] < 10:
        return {'error': 1, 'error_message': 'Falha na compra do pacote de figurinhas! Você não tem moedas o suficiente!'}

    DB_CUR.execute(f'UPDATE users SET coins=coins-10 WHERE email="{request["email"]}"')
    WON_STICKERS = random.sample(list(DB_CUR.execute('SELECT id, sticker_models_name FROM sticker_prints WHERE owner_user_name=""')), 2)
    for sticker in WON_STICKERS:
        DB_CUR.execute(f'UPDATE sticker_prints SET owner_user_name="{request["email"]}" WHERE id="{sticker[0]}"')

    database.commit()

    return {'error': 0, 'won_stickers': [{'id': idf, 'sticker_model_name': sticker_model_name} for idf, sticker_model_name in WON_STICKERS]}
