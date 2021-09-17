import auxiliary as aux


def admin__create_giftcard(REQUEST, DATABASE):
    if aux.exist_giftcard(REQUEST, DATABASE) == 1:
        return {'error': 1, 'error_message': 'Falha na criação do Giftcard! Já existe um Giftcard com essa chave.'}

    DB_CUR = DATABASE.cursor()
    DB_CUR.execute(f'INSERT INTO giftcards VALUES ("{REQUEST["giftcard_key"]}")')
    DATABASE.commit()
    return {'error': 0}


def admin__create_stickers(REQUEST, DATABASE):
    DB_CUR = DATABASE.cursor()
    for _ in range(REQUEST["sticker_number"]):
        DB_CUR.execute(f'INSERT INTO stickers (name, owner_email, is_pasted, is_for_sale, price) VALUES ("{REQUEST["sticker_name"]}", "", 0, 0, 0)')
    DATABASE.commit()
    return {'error': 0}


def admin__draw_lucky_prize(REQUEST, DATABASE):
    DB_CUR = DATABASE.cursor()
    DB_CUR.execute('UPDATE users SET coins=coins+50 WHERE email=(SELECT email FROM users ORDER BY RANDOM() LIMIT 1)')
    DATABASE.commit()
    return {'error': 0}


def admin__op(REQUEST, DATABASE):
    if aux.exist_email_registered(REQUEST, DATABASE) == 0:
        return {'error': 1, 'error_message': 'Não é possível tornar esse usuário um administrador! Email não encontrado.'}

    DB_CUR = DATABASE.cursor()
    DB_CUR.execute(f'UPDATE users SET is_admin = 1 WHERE email="{REQUEST["target_email"]}"')
    DATABASE.commit()
    return {'error': 0}


def admin__unop(REQUEST, DATABASE):
    if aux.exist_email_registered(REQUEST, DATABASE) == 0:
        return {'error': 1, 'error_message': 'Não é possível tornar esse usuário um administrador! Email não encontrado.'}

    DB_CUR = DATABASE.cursor()
    DB_CUR.execute(f'UPDATE users SET is_admin = 0 WHERE email="{REQUEST["target_email"]}"')
    DATABASE.commit()
    return {'error': 0}


def album__get_album(REQUEST, DATABASE):
    DB_CUR = DATABASE.cursor()
    return {'error': 0, 'stickers': [x[0] for x in list(DB_CUR.execute(f'SELECT name FROM stickers WHERE owner_email="{REQUEST["email"]}" AND is_pasted=1'))]}


def album__get_free_stickers(REQUEST, DATABASE):
    DB_CUR = DATABASE.cursor()
    return {'error': 0, 'stickers': [{'id': x[0], 'sticker_name': x[1]} for x in list(DB_CUR.execute(f'SELECT id, name FROM stickers WHERE owner_email="{REQUEST["email"]}" AND is_pasted=0 AND is_for_sale=0'))]}


def album__paste_sticker(REQUEST, DATABASE):
    if aux.exist_sticker(REQUEST, DATABASE) == 0:
        return {'error': 1, 'error_message': 'Não é possível colar esta figurinha! A figurinha não existe.'}

    if aux.is_this_sticker_model_pasted(REQUEST, DATABASE) == 1:
        return {'error': 1, 'error_message': 'Não é possível colar esta figurinha! O modelo de figurinha já está colado.'}

    if aux.is_this_sticker_waiting_for_sale(REQUEST, DATABASE) == 1:
        return {'error': 1, 'error_message': 'Não é possível colar esta figurinha! Ela está na fila para a venda.'}

    if aux.is_this_sticker_owned_by_the_user(REQUEST, DATABASE) == 1:
        return {'error': 1, 'error_message': 'Erro ao colar figurinha! O usuário não é dono desta figurinha.'}

    DB_CUR = DATABASE.cursor()
    DB_CUR.execute(f'UPDATE stickers SET is_pasted=1 WHERE id="{REQUEST["sticker_id"]}"')
    DATABASE.commit()
    return {'error': 0}


def community_market__buy_sticker(REQUEST, DATABASE):
    DB_CUR = DATABASE.cursor()
    QUERRY_RESULT = list(DB_CUR.execute(f'SELECT id, price FROM stickers WHERE price=(SELECT MIN(price) FROM stickers WHERE name="{REQUEST["sticker_name"]}" AND is_for_sale=1 AND owner_email!="{REQUEST["email"]}")'))

    if len(QUERRY_RESULT) == 0:
        return {'error': 0, 'error_message': 'Não foi possível retornar preço da figurinha! Não há nenhuma figurinha desse modelo a venda!'}

    DESIRED_CARD = QUERRY_RESULT[0]

    if aux.get_coins(REQUEST, DATABASE) < DESIRED_CARD[1]:
        return {'error': 1, 'error_message': 'Não foi possível comprar a figurinha! Usuário sem moedas o suficiente'}

    DB_CUR.execute(f'UPDATE users SET coins=coins-{DESIRED_CARD[1]} WHERE email="{REQUEST["email"]}"')
    DB_CUR.execute(f'UPDATE stickers SET owner_email="{REQUEST["email"]}", is_for_sale=0, price=0 WHERE id={DESIRED_CARD[0]}')
    DATABASE.commit()
    return {'error': 0}


def community_market__get_sticker_price(REQUEST, DATABASE):
    DB_CUR = DATABASE.cursor()
    QUERRY_RESULT = list(DB_CUR.execute(f'SELECT price FROM stickers WHERE price=(SELECT MIN(price) FROM stickers WHERE name="{REQUEST["sticker_name"]}" AND is_for_sale=1 AND owner_email!="{REQUEST["email"]}")'))

    if len(QUERRY_RESULT) == 0:
        return {'error': 1, 'error_message': 'Não foi possível retornar preço da figurinha! Não há nenhuma figurinha desse modelo a venda!'}

    return {'error': 0, 'price': QUERRY_RESULT[0][0]}


def community_market__get_stickers_waiting_for_sale(REQUEST, DATABASE):
    DB_CUR = DATABASE.cursor()
    return {'error': 0, 'stickers': [{'sticker_name': x[0], 'price':x[1]} for x in list(DB_CUR.execute(f'SELECT name, price FROM stickers WHERE owner_email="{REQUEST["email"]}" AND is_for_sale=1'))]}


def community_market__put_sticker_to_sell(REQUEST, DATABASE):
    if aux.exist_sticker(REQUEST, DATABASE) == 0:
        return {'error': 1, 'error_message': 'Não é possível vender esta figurinha! A figurinha não existe.'}

    if aux.is_this_sticker_owned_by_the_user(REQUEST, DATABASE) == 0:
        return {'error': 1, 'error_message': 'Erro ao colocar figurinha a venda! O usuário não é dono desta figurinha.'}

    DB_CUR = DATABASE.cursor()
    DB_CUR.execute(f'UPDATE stickers SET is_for_sale=1, price={REQUEST["price"]} WHERE id="{REQUEST["sticker_id"]}"')
    DATABASE.commit()
    return {'error': 0}


def user__get_coins(REQUEST, DATABASE):
    return {'error': 0, 'coins': aux.get_coins(REQUEST, DATABASE)}


def user__is_admin(REQUEST, DATABASE):
    DB_CUR = DATABASE.cursor()
    QUERY_RESULT = DB_CUR.execute(f'SELECT is_admin FROM users WHERE email="{REQUEST["email"]}"')
    if next(QUERY_RESULT)[0] == 1:
        return {'error': 0}
    else:
        return {'error': 1, 'error_message': 'Usuário não é administrador!'}


def user__login(REQUEST, DATABASE):
    DB_CUR = DATABASE.cursor()
    if list(DB_CUR.execute(f'SELECT COUNT(*) FROM users WHERE email="{REQUEST["email"]}" AND password="{REQUEST["password"]}"'))[0][0] == 1:
        return {'error': 0}
    else:
        return {'error': 1, 'error_message': 'Usuário não encontrado!'}


def user__register(REQUEST, DATABASE):
    if aux.exist_email_registered(REQUEST, DATABASE) == 1:
        return {'error': 1, 'error_message': 'Falha no cadastro! Email já está em uso.'}

    DB_CUR = DATABASE.cursor()
    DB_CUR.execute(f'INSERT INTO users VALUES ("{REQUEST["email"]}", "{REQUEST["password"]}", 0, 0)')
    DATABASE.commit()
    return {'error': 0}


def user__retrieve_giftcard(REQUEST, DATABASE):
    if aux.exist_giftcard(REQUEST, DATABASE) == 0:
        return {'error': 1, 'error_message': 'Falha no resgate do Giftcard! Não existe um Giftcard com essa chave.'}

    DB_CUR = DATABASE.cursor()
    DB_CUR.execute(f'UPDATE users SET coins=coins+100 WHERE email="{REQUEST["email"]}"')
    DB_CUR.execute(f'DELETE FROM giftcards WHERE key="{REQUEST["giftcard_key"]}"')
    DATABASE.commit()
    return {'error': 0}


def official_market__buy_sticker_pack(REQUEST, DATABASE):
    DB_CUR = DATABASE.cursor()

    if list(DB_CUR.execute('SELECT COUNT(*) FROM stickers WHERE owner_email=""'))[0][0] < 2:
        return {'error': 1, 'error_message': 'Falha na compra do pacote de figurinhas! Não existe figurinhas impressas sem dono suficientes'}

    if aux.get_coins(REQUEST, DATABASE) < 10:
        return {'error': 1, 'error_message': 'Falha na compra do pacote de figurinhas! Você não tem moedas o suficiente!'}

    DB_CUR.execute(f'UPDATE users SET coins=coins-10 WHERE email="{REQUEST["email"]}"')
    for _ in range(2):
        DB_CUR.execute(f'UPDATE stickers SET owner_email="{REQUEST["email"]}" WHERE id=(SELECT id FROM stickers WHERE owner_email="" ORDER BY RANDOM() LIMIT 1)')

    DATABASE.commit()

    return {'error': 0}
