import json
import socket

CFG = json.load(open('config.json'))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((CFG['HOST'], CFG['PORT']))
    request = {'method': 'community_market/get_sticker_price', 'email': 'joao.das.neves@ufv.br', 'sticker_name': 'The Darkside of the Moon'}

    s.sendall(json.dumps(request).encode(CFG['ENCODE_FORMAT']))
    response = json.loads(s.recv(CFG['BUFFSIZE']).decode(CFG["ENCODE_FORMAT"]))
    print(f'Recebido {response}')
