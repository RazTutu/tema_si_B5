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
print(test)