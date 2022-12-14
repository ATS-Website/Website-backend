import decimal
import json

from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from decouple import config
from Cryptodome.Util.Padding import pad, unpad


class AESCipher:

    def __init__(self, key, iv):
        self.block_size = 32
        self.key = bytes(key, "ascii")
        self.iv = bytes(iv, "ascii")

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return b64encode(cipher.encrypt(pad(data.encode(), AES.block_size))).decode()

    def decrypt(self, data):
        cipher_text = b64decode(data.encode())
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return unpad(cipher.decrypt(cipher_text), AES.block_size).decode()

    def versatile_encrypt(self, the_object):
        if isinstance(the_object, dict):
            for key, value in the_object.items():
                if isinstance(value, float) or isinstance(value, int) or isinstance(value, str):
                    the_object[key] = self.encrypt(str(value))
                else:
                    the_object[key] = self.versatile_encrypt(value)
        elif isinstance(the_object, list):
            for index, value in enumerate(the_object):
                the_object[index] = self.versatile_encrypt(value)
        elif isinstance(the_object, tuple):
            the_object = self.versatile_encrypt(list(the_object))
        else:
            the_object = self.encrypt(str(the_object))

        return the_object

    def versatile_decrypt(self, the_object):
        if isinstance(the_object, dict):
            for key, value in the_object.items():
                if isinstance(value, str):
                    the_object[key] = self.decrypt(value)
                else:
                    the_object[key] = self.versatile_decrypt(value)
        elif isinstance(the_object, list):
            for index, value in enumerate(list):
                the_object[index] = self.versatile_decrypt(value)

        elif isinstance(the_object, tuple):
            the_object = self.versatile_decrypt(list(the_object))
        else:
            the_object = self.decrypt(str(the_object))

        return the_object


key = config("KEY")
iv = config("IV")


def aes_encrypt(keyword):
    return AESCipher(key, iv).versatile_encrypt(keyword)


def aes_decrypt(keyword):
    return AESCipher(key, iv).versatile_decrypt(keyword)


data = {
    "date_time": "2022-12-12 08:13",
    "email": "sazubuine@afexnigeria.com",
    "latitude": "7.892345655",
    "longitude": "3.98736254"
}


enc = aes_encrypt(data)
print(enc)


dec = aes_decrypt(data)
print(dec)


