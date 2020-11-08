# 128 bits keys

# keys generated with
# key = get_random_bytes(16) # 16 bytes * 8 = 128 bits

K1 = b'\x0b\x08\x86\xedL\xdfm\xfcP\xe0\x91\xbb\xec\x8b\xd7\x9e'
K2 = b'\xdb\xd3\xea\xf1\xb9\xbf\x06R\xcf\xc5#zh\x0c\xa9q'
K3 = b'\xe6\xbe\x0e\xbf\xe60\xe2\x89\x99Q\xe6\x14+"D\xb6'

#print(len(K3))

initialization_vector = str.encode('textrandombattle')

# try ofb
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
data = b"secret"
initialization_vector = b"vectordeinitiali"
key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_OFB, initialization_vector)
enc_mess = cipher.encrypt(data)
#print("encrypted message is", enc_mess)

from random import randrange
test = randrange(2)
#print(test)

def bxor(ba1, ba2):
    """ XOR two byte strings """
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

#OFB - CRIPTARE
non_initialized_vector = 'textrandombattle'
message = "1234567890123456"
K2 = b'\xdb\xd3\xea\xf1\xb9\xbf\x06R\xcf\xc5#zh\x0c\xa9q'
# criptez non_initialized_vector si K2 cu ECB
cipher = AES.new(key, AES.MODE_ECB) # Create a AES cipher object with the key using the mode ECB
# no need for padding because key is of 16 bytes, the same as an AES block
ciphered_data = cipher.encrypt(non_initialized_vector.encode("ascii"))
print("encrypted data is", ciphered_data)

next_vector = ciphered_data 
flag = bxor(K2, ciphered_data)
print("xored value is", flag)

#faci xor intre rezultatu de mai devreme si ciphered_data, iti da K2
flag2 = bxor(flag, ciphered_data)
print("tre sa dea k2 cred", flag2)
