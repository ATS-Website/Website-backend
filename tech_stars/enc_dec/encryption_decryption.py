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
        return b64encode(cipher.encrypt(pad(data.encode(), self.block_size))).decode()

    def decrypt(self, data):
        cipher_text = b64decode(data.encode())
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return unpad(cipher.decrypt(cipher_text), self.block_size).decode()

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


# look = {
#     "email": "John Doe",
#     "official_email": "loko873n@afexnigeria.com",
#     "self_description": "No Fear!",
# }

# look = {"email": "sazubuine@afexnigeria.com", "date_time": "2022-11-28T09:06:52.827Z", "device_id": "RP1A.200720.011", "longitude": "3.9320336", "latitude": "7.4035462"}
# test = aes_encrypt(look)
# print(test)

# testst = aes_decrypt(
#     "qLiaHhtouPPj8F7S6tGHCyG6/E5PmyjlBRN8sxJDfOTVo7VF3mUCaTdoHye/dYDBGOg98rkcpPJ0UTLsQVsIMnlGScolsrpCJjEkjzJ5JpVwNcg6H3GZvLznhztEc7fj39CzcR3sySbGlivdEkyrkEx9aUjacAZ+e1drTFJT4uE=")
# print

# new = {'full_name': 'P8in3dmAqDUidUMiVJXiAekiYzOzcyGaYuFmUW+qitY=',
#        'official_email': 'pKuF/hhPBcYzc/YDbKgzMV/DmzBUgqdZZLD0Y3s2KNo=',
#        'self_description': '+7FVTzcAjtg2hpyE5J+u0lfGy0Mt6Ow2+CPigxjis54='}


new = {
    "email": "N1aeh+wNVBH5k6Cu9aR98zfMfQv7bKawdl6z3T7KNqU=",
    "date_time": "kYTECjzNWn86IL0f0I7MUxrvdL8OWYPZD9YfOxn3UGo=",
    "device_id": "RbMQ/agoVQpHh6ABEly6lg==",
    "longitude": "3gVTjOKvCakqY6cl4t3caA==",
    "latitude": "Pw7jR0uw01sf3f1gMGIWGg=="
}
# print(aes_decrypt("XAaH2f93y8EYWm+x2ZEta1fWSGAp+etcwhC33QdF8/P3QKYQrQ997VeZTmEowLPGpVkFigJVbw2VyBD/jyuY8Q=="))
print(aes_decrypt(new))
