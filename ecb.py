from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

key = b'}\xdf\x1d\xa6-f\x8a\x9ac\xdb\x02\xe1\x85\x00\xb375\x8c\x10\x12w\xdc\xeew\x84\x1f\xd8\xdb\xeaI\xa1f'
output_file = 'ecbEncryptedText.bin'
data = b'aaaaaaaaaaaaaaaaaaaae' # Must be a bytes object

# Create cipher object and encrypt the data
cipher = AES.new(key, AES.MODE_ECB) # Create a AES cipher object with the key using the mode CBC
ciphered_data = cipher.encrypt(pad(data, AES.block_size)) # Pad the input data and then encrypt

print(ciphered_data)

# Decrypt
DecryptCipher = AES.new(key, AES.MODE_ECB)  # Setup cipher
original_data = unpad(DecryptCipher.decrypt(ciphered_data), AES.block_size) # Decrypt and then up-pad the result
print("decrypted data is:", original_data.decode("UTF-8")) # the initial value is in binary. I decoded to string

