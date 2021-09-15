from datetime import datetime
import json
import socket

CFG = json.load(open('config.json'))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((CFG['HOST'], CFG['PORT']))
    s.listen(CFG['LISTEN'])
    print(f'{datetime.now()} :: [INFO] Servidor online;')

    while True:
        connection, address = s.accept()
        print(f'{datetime.now()} :: [INFO] Conectado a {address[0]}:{address[1]};')

        with connection:
            request = json.loads(connection.recv(CFG['BUFFSIZE']).decode(CFG['ENCODE_FORMAT']))
            print(f'{datetime.now()} :: [DEBUG] Recebido JSON de Requisição = {request};')

            response = request

            connection.sendall(json.dumps(response).encode(CFG['ENCODE_FORMAT']))
            print(f'{datetime.now()} :: [DEBUG] Enviando JSON de Resposta = {response};')
