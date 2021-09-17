import json
import socket

CFG = json.load(open('config.json'))


def contact_to_server(REQUEST):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SCK:
        SCK.connect((CFG['HOST'], CFG['PORT']))
        SCK.sendall(json.dumps(REQUEST).encode(CFG['ENCODE_FORMAT']))

        return json.loads(SCK.recv(CFG['BUFFSIZE']).decode(CFG["ENCODE_FORMAT"]))


def is_admin(EMAIL):
    REQUEST = {
        'method': 'user/is_admin',
        'email': EMAIL
    }

    RESPONSE = contact_to_server(REQUEST)

    return not RESPONSE['error']


def login():
    while True:
        REQUEST = {
            'method': 'user/login',
            'email': input('Digite o seu email: '),
            'password': input('Digite a sua senha: ')
        }

        RESPONSE = contact_to_server(REQUEST)

        if RESPONSE['error'] == 1:
            print(f'Erro! {RESPONSE["error_message"]} Tente novamente...\n')
        else:
            return REQUEST['email']


def register():
    while True:
        REQUEST = {
            'method': 'user/register',
            'email': input('Digite o email a ser cadastrado: '),
            'password': input('Digite a sua senha: ')
        }

        RESPONSE = contact_to_server(REQUEST)

        if RESPONSE['error'] == 1:
            print(f'Erro! {RESPONSE["error_message"]} Tente novamente...\n')
        else:
            return REQUEST['email']
