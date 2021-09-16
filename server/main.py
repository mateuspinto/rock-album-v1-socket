from datetime import datetime
import json
import socket
import sqlite3

from common import router

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
