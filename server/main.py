from datetime import datetime
import json
import socket
import sqlite3

import routes


def router(request, database):
    MW = {
        'user/login': routes.user__login,
        'user/register': routes.user__register,
        'user/is_admin': routes.user__is_admin,
        'user/retrieve_giftcard': routes.user__retrieve_giftcard,
        'user/get_coins': routes.user__get_coins,

        'admin/op': routes.admin__op,
        'admin/unop': routes.admin__unop,
        'admin/create_giftcard': routes.admin__create_giftcard,
        'admin/create_stickers': routes.admin__create_stickers,

        'official_market/buy_sticker_pack': routes.official_market__buy_sticker_pack,

        'album/paste_sticker': routes.album__paste_sticker,
        'album/get_album': routes.album__get_album,
        'album/get_free_stickers': routes.album__get_free_stickers,

        'community_market/put_sticker_to_sell': routes.community_market__put_sticker_to_sell,
        'community_market/get_sticker_price': routes.community_market__get_sticker_price,
    }

    return MW[request['method']](request, database)


CFG = json.load(open('config.json'))

with sqlite3.connect(CFG['SQLITE_FILE']) as DB, socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SCK:
    SCK.bind((CFG['HOST'], CFG['PORT']))
    SCK.listen(CFG['LISTEN'])
    print(f'{datetime.now()} :: [INFO] Servidor online;')

    while True:
        connection, address = SCK.accept()
        print(f'{datetime.now()} :: [INFO] Conectado a {address[0]}:{address[1]};')

        with connection:
            request = json.loads(connection.recv(CFG['BUFFSIZE']).decode(CFG['ENCODE_FORMAT']))
            print(f'{datetime.now()} :: [DEBUG] Recebido JSON de Requisição = {request};')

            response = router(request, DB)

            connection.sendall(json.dumps(response).encode(CFG['ENCODE_FORMAT']))
            print(f'{datetime.now()} :: [DEBUG] Enviando JSON de Resposta = {response};')
