def exist_email_registered(request, database):
    DB_CUR = database.cursor()
    return 1 if list(DB_CUR.execute(f'SELECT COUNT(*) FROM users WHERE email="{request["email"]}"'))[0][0] == 1 else 0


def exist_giftcard(request, database):
    DB_CUR = database.cursor()
    return 1 if list(DB_CUR.execute(f'SELECT COUNT(*) FROM giftcards WHERE key="{request["giftcard_key"]}"'))[0][0] == 1 else 0


def exist_sticker(request, database):
    DB_CUR = database.cursor()
    return 1 if list(DB_CUR.execute(f'SELECT COUNT(*) FROM stickers WHERE id="{request["sticker_id"]}"'))[0][0] == 1 else 0


def get_coins(request, database):
    DB_CUR = database.cursor()
    return int(list(DB_CUR.execute(f'SELECT coins FROM users WHERE email="{request["email"]}"'))[0][0])


def is_this_sticker_model_pasted(request, database):
    DB_CUR = database.cursor()
    STICKER_NAME = list(DB_CUR.execute(f'SELECT name FROM stickers WHERE id={request["sticker_id"]}'))[0][0]
    return 1 if list(DB_CUR.execute(f'SELECT COUNT(*) FROM stickers WHERE name="{STICKER_NAME}" AND owner_email="{request["email"]}" AND is_pasted=1'))[0][0] == 1 else 0


def is_this_sticker_owned_by_the_user(request, database):
    DB_CUR = database.cursor()
    return 1 if list(DB_CUR.execute(f'SELECT COUNT(*) FROM stickers WHERE id="{request["sticker_id"]}" AND owner_email="{request["email"]}"'))[0][0] == 1 else 0


def is_this_sticker_waiting_for_sale(request, database):
    DB_CUR = database.cursor()
    return 1 if list(DB_CUR.execute(f'SELECT COUNT(*) FROM stickers WHERE id="{request["sticker_id"]}" AND is_for_sale=1'))[0][0] == 1 else 0
