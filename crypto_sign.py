import binascii

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_ssh_private_key, load_der_public_key
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend


def sign_text(p_key, text):
    sign = p_key.sign(
        text.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    ).decode('latin1')

    return sign


def check_sign(str_public_key, text, sign):
    print(str_public_key.replace("b'", "").replace("'", "").replace("\\n", "\n").encode())

    pub_key = load_der_public_key(str_public_key.encode())

    try:
        pub_key.verify(
            sign.encode('latin1'),
            text,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except:
        return False

    #
    # with open('./id_rsa', "rb") as f:
    #     key = RSA.import_key(f.read())
    #
    # print(key.export_key().decode())
    #
    # sign = sign_text(key, '123')
    # print(sign)
    # print(bytes(sign))
    #
    # pub_key = key.public_key().exportKey().decode()
    #
    # print(pub_key)
    #
    # print(check_sign(pub_key, '123', str(sign)))

    # генерируем пару ключей


with open('./id_rsa', "rb") as f:
    private_key = load_ssh_private_key(f.read(), password=None, backend=default_backend())

# подписываем сообщение
message = b'Hello, World!'
signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
).decode('latin1')

public_key = private_key.public_key()

print(public_key)
print(signature)

# верифицируем подпись
try:
    public_key.verify(
        signature.encode('latin1'),
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("Подпись верна.")
except:
    print("Подпись неверна.")
