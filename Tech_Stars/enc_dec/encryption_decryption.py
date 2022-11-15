import json

from Crypto.Cipher import AES
from hashlib import sha256
from base64 import b64encode, b64decode
from decouple import config


class AESCipher:

    def __init__(self, data, key, iv):
        self.block_size = 32
        self.data = data
        self.key = sha256(key.encode()).digest()[:32]
        self.iv = sha256(iv.encode()).digest()[:16]
        self.pad = lambda s: s + (self.block_size - len(s) % self.block_size) * chr(
            self.block_size - len(s) % self.block_size)
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    def encrypt(self):
        plain_text = self.pad(self.data)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return b64encode(cipher.encrypt(plain_text.encode())).decode()

    def decrypt(self):
        cipher_text = b64decode(self.data.encode())
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return self.unpad(cipher.decrypt(cipher_text)).decode()


key = config("KEY")
iv = config("IV")


def aes_encrypt(keyword):
    return AESCipher(str(keyword), key, iv).encrypt()


def aes_decrypt(keyword):
    return AESCipher(str(keyword), key, iv).decrypt()


look = {
    "full_name": "Adekunle Abraham",
    "official_email": "loko873n@afexnigeria.com",
    "self_description": "No Fear!",
    "favorite_meal": "Eba and beans"
}
# test = aes_encrypt(str(look))
# print(test, "Book")

# test_2 = aes_decrypt(
#     "c5eiZD27WSQs3eiL1lLZzGE6VJDxAQGaKm3SJSPEqgzxC9LZLmDBFsz6xOaVqRM+s4pvVS3RpeGVmoikbrO0d4Yp9NLxdrO3DjdOiEmshmTK0R0gJtPUgCy9PMn6Ea/dr6AZWBGoYCyqBoti/7p8UlHfCXrb1udFiGljReUFBfWXvw5HUMTT0AWma5r+o63XdO6m09ssJHDhi5gcKs/uhw==")
# print(test_2)
