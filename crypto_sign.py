from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA


def sign_text(str_public_key, text):
    signature = get_sign(str_public_key, text)

    return signature


def check_signature(str_signature, str_pub_key, text):
    if str_pub_key is None:
        return False

    signature = get_sign(str_pub_key, text)

    print(str_signature)
    print(signature)

    return signature == str_signature


def get_sign(str_pub_key, text):
    print(text)
    print(str_pub_key)
    h = SHA256.new(text.encode('UTF-8')).hexdigest()
    print(h)
    public_key = RSA.import_key(str_pub_key.replace("b'", "").replace("'", "").replace("\\n", "\n"))
    rsa_public_key = PKCS1_OAEP.new(public_key)
    print(h.encode())
    return rsa_public_key.encrypt(h.encode())

# with open('./id_rsa', "rb") as f:
#     key = RSA.import_key(f.read())
#
# pub_key = str(key.public_key().export_key()).replace("b'", "").replace("'", "").replace("\\n", "\n")
#
# sign = sign_text(pub_key, '123')
#
# print(check_signature(sign, pub_key, '123'))
#
# public_key = serialization.load_pem_public_key(
#     pub_key.encode(),
#     backend=default_backend()
# )
#
# encrypted = public_key.encrypt(
#     'message'.encode(),
#     padding.OAEP(
#         mgf=padding.MGF1(algorithm=hashes.SHA256()),
#         algorithm=hashes.SHA256(),
#         label=None
#     )
# )
#
# print(encrypted)
