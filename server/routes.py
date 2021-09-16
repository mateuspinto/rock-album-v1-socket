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
    QUERY_RESULT = DB_CUR.execute(f'SELECT * FROM sticker_models WHERE name="{request["sticker_name"]}"')
    if len(list(QUERY_RESULT)) == 1:
        return {'error': 0}
    else:
        return {'error': 1, 'error_message': 'Modelo de figurinha não existente!'}


def create_sticker_model(request, database):
    DB_CUR = database.cursor()
    DB_CUR.execute(f'INSERT INTO sticker_models VALUES ("{request["sticker_name"]}")')
    database.commit()
    return {'error': 0}


def print_stickers(request, database):
    if __exist_sticker_model(request, database)['error'] == 1:
        return {'error': 1, 'error_message': 'Falha na impressão das figurinhas! Não existe um modelo de figurinha com esse nome.'}

    DB_CUR = database.cursor()
    for _ in range(request["sticker_print_number"]):
        DB_CUR.execute(f'INSERT INTO sticker_prints (sticker_models_name, owner_user_email, is_pasted, is_for_sale, sale_price) VALUES ("{request["sticker_name"]}", "", 0, 0, 0)')
    database.commit()
    return {'error': 0}


def buy_sticker_pack(request, database):
    DB_CUR = database.cursor()

    if list(DB_CUR.execute('SELECT COUNT(*) FROM sticker_prints WHERE owner_user_email=""'))[0][0] < 2:
        return {'error': 1, 'error_message': 'Falha na compra do pacote de figurinhas! Não existe figurinhas impressas sem dono suficientes'}

    if get_coins(request, database)['coins'] < 10:
        return {'error': 1, 'error_message': 'Falha na compra do pacote de figurinhas! Você não tem moedas o suficiente!'}

    DB_CUR.execute(f'UPDATE users SET coins=coins-10 WHERE email="{request["email"]}"')
    WON_STICKERS = random.sample(list(DB_CUR.execute('SELECT id, sticker_models_name FROM sticker_prints WHERE owner_user_email=""')), 2)
    for sticker in WON_STICKERS:
        DB_CUR.execute(f'UPDATE sticker_prints SET owner_user_email="{request["email"]}" WHERE id="{sticker[0]}"')

    database.commit()

    return {'error': 0, 'won_stickers': [{'id': idf, 'sticker_name': sticker_name} for idf, sticker_name in WON_STICKERS]}


def __is_this_sticker_model_pasted(request, database):
    DB_CUR = database.cursor()
    STICKER_NAME = list(DB_CUR.execute(f'SELECT sticker_models_name FROM sticker_prints WHERE id={request["sticker_id"]}'))[0][0]

    if list(DB_CUR.execute(f'SELECT COUNT(*) FROM sticker_prints WHERE sticker_models_name="{STICKER_NAME}" AND owner_user_email="{request["email"]}" AND is_pasted=1'))[0][0] == 1:
        return {'error': 0}
    else:
        return {'error': 1, 'error_message': 'O modelo de figurinha não está colado!'}


def __is_this_sticker_waiting_for_sale(request, database):
    DB_CUR = database.cursor()

    if list(DB_CUR.execute(f'SELECT COUNT(*) FROM sticker_prints WHERE id="{request["sticker_id"]}" AND is_for_sale=1'))[0][0] == 1:
        return {'error': 0}
    else:
        return {'error': 1, 'error_message': 'Figurinha não está na fila para a venda!'}


def __is_this_sticker_print_owned_by_the_user(request, database):
    DB_CUR = database.cursor()

    if list(DB_CUR.execute(f'SELECT COUNT(*) FROM sticker_prints WHERE id="{request["sticker_id"]}" AND owner_user_email="{request["email"]}"'))[0][0] == 1:
        return {'error': 0}
    else:
        return {'error': 1, 'error_message': 'O usuário não é dono desta figurinha!'}


def paste_sticker(request, database):
    if __is_this_sticker_model_pasted(request, database)['error'] == 0:
        return {'error': 1, 'error_message': 'Não é possível colar esta figurinha! O modelo de figurinha já está colado.'}

    if __is_this_sticker_waiting_for_sale(request, database)['error'] == 0:
        return {'error': 1, 'error_message': 'Não é possível colar esta figurinha! Ela está na fila para a venda.'}

    if __is_this_sticker_print_owned_by_the_user(request, database)['error'] == 1:
        return {'error': 1, 'error_message': 'Erro ao colar figurinha! O usuário não é dono desta figurinha.'}

    DB_CUR = database.cursor()
    DB_CUR.execute(f'UPDATE sticker_prints SET is_pasted=1 WHERE id="{request["sticker_id"]}"')
    database.commit()

    return {'error': 0}


def view_album(request, database):
    DB_CUR = database.cursor()
    return {'error': 0, 'stickers': [x[0] for x in list(DB_CUR.execute(f'SELECT sticker_models_name FROM sticker_prints WHERE owner_user_email="{request["email"]}" AND is_pasted=1'))]}


def view_stickers_waiting_for_sale(request, database):
    DB_CUR = database.cursor()
    return {'error': 0, 'stickers': [x[0] for x in list(DB_CUR.execute(f'SELECT sticker_models_name FROM sticker_prints WHERE owner_user_email="{request["email"]}" AND is_for_sale=1'))]}


def view_free_stickers(request, database):
    DB_CUR = database.cursor()
    return {'error': 0, 'stickers': [{'id': x[0], 'sticker_name': x[1]} for x in list(DB_CUR.execute(f'SELECT id, sticker_models_name FROM sticker_prints WHERE owner_user_email="{request["email"]}" AND is_pasted=0 AND is_for_sale=0'))]}


def sell_sticker(request, database):
    DB_CUR = database.cursor()

    if __is_this_sticker_print_owned_by_the_user(request, database)['error'] == 1:
        return {'error': 1, 'error_message': 'Erro ao colocar figurinha a venda! O usuário não é dono desta figurinha.'}

    DB_CUR.execute(f'UPDATE sticker_prints SET is_for_sale=1, sale_price={request["sale_price"]} WHERE id="{request["sticker_id"]}"')
    database.commit()

    return {'error': 0}


def get_stickers_price(request, database):
    DB_CUR = database.cursor()
    QUERRY_RESULT = list(DB_CUR.execute(f'SELECT sale_price FROM sticker_prints WHERE sale_price=(SELECT MIN(sale_price) FROM sticker_prints WHERE sticker_models_name="{request["sticker_name"]}" AND is_for_sale=1)'))
    if len(QUERRY_RESULT) == 0:
        return {'error': 0, 'error_message': 'Não foi possível retornar preço da figurinha! Não há nenhuma figurinha desse modelo a venda!'}

    return {'error': 0, 'sale_price': QUERRY_RESULT[0][0]}
