from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


def sign_text(private_key, text):
    # Получаем хэш файла
    h = SHA256.new(text.encode('UTF-8'))

    # Подписываем хэш
    signature = pkcs1_15.new(private_key).sign(h)

    print(private_key.public_key().export_key())

    return signature


def check_signature(signature, pub_key, text):
    if pub_key is None:
        return False

    # pub_key = pub_key.replace("-----BEGIN PUBLIC KEY-----\n", '')
    # pub_key = pub_key.replace("\n-----END PUBLIC KEY-----", '')

    print(pub_key)

    pubkey = RSA.import_key(bytes(pub_key))

    try:
        pkcs1_15.new(pubkey).verify(SHA256.new(text.encode('UTF-8')), signature)
        return True
    except ValueError:
        return False


with open('./id_rsa', "rb") as f:
    key = RSA.import_key(f.read())

sign = sign_text(key, '123')

pub_key = str(key.public_key().export_key())

print(pub_key)

print(check_signature(sign, pub_key, '123'))
