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
    "full_name": "Adekunle, Abraham",
    "official_email": "loko873n@afexnigeria.com",
    "self_description": "No Fear!",
    "favorite_meal": "Eba and beans"
}
test = aes_encrypt(look)
print(test)

test_2 = aes_decrypt("tfaj0vDQeEF2QFycXYrAIk0g5x4UqHPjrvVXVXwLspjO4yLJhDDxDJMN/L7f5cBJFNsm9w4B9JCf4N+j74AZY9oS9mCviJaBXdLZwwvREpEn61VkiNTBKRlAtBMEclY/BOgqpbVcTcJvtT5my7d8YOsH3/LmruVULtlQrW1fHsY9obWOPNtANy6nW3iZtPXp87oOH4yAWaXj9aMETvm9pQ==")
print(test_2)


