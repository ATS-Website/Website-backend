import json

from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from decouple import config
from Cryptodome.Util.Padding import pad, unpad


class AESCipher:

    def __init__(self, data, key, iv):
        self.block_size = 32
        self.data = data
        self.key = bytes(key, "ascii")
        self.iv = bytes(iv, "ascii")

    def encrypt(self):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return b64encode(cipher.encrypt(pad(self.data.encode(), self.block_size))).decode()

    def decrypt(self):
        cipher_text = b64decode(self.data.encode())
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return unpad(cipher.decrypt(cipher_text), self.block_size).decode()


key = config("KEY")
iv = config("IV")


def aes_encrypt(keyword):
    return AESCipher(json.dumps(keyword), key, iv).encrypt()


def aes_decrypt(keyword):
    return AESCipher(json.dumps(keyword), key, iv).decrypt()


look = {
    "full_name": "John Doe",
    "official_email": "loko873n@afexnigeria.com",
    "self_description": "No Fear!",
}
test = aes_encrypt(look)
print(test)
#
# test_2 = aes_decrypt("qLiaHhtouPPj8F7S6tGHCyG6/E5PmyjlBRN8sxJDfOTVo7VF3mUCaTdoHye/dYDBGOg98rkcpPJ0UTLsQVsIMnlGScolsrpCJjEkjzJ5JpVwNcg6H3GZvLznhztEc7fj39CzcR3sySbGlivdEkyrkEx9aUjacAZ+e1drTFJT4uE=")
# print(test_2)
#
# tesss = aes_decrypt("F+qx9sFEhX8uxGqPAwIvOOwt5DgvnwiAiBXwT+Ltmrn35NQtEulfUghH/MqcyPHHvfmQbDNol1ksGhb3MHWi3Bv"
#                     "/lh1TQ300glh+5Ls+UxYuPykjv9ZhJOE2QWFV2hSChUJ+KQnGBMlzC03zrIjYhFb0gZC0tB+L4W8Gm"
#                     "/OXcorYZpeZfa9WwZEh3tKTeF/7Yc6s4WEs1tvmoOEMO4bz7hRcto06iTvoYEqIpPPVNrWLyBuJwSu9kx4lHSRDPTyU")
# print(tesss)


