from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

#cbc
key = b'}\xdf\x1d\xa6-f\x8a\x9ac\xdb\x02\xe1\x85\x00\xb375\x8c\x10\x12w\xdc\xeew\x84\x1f\xd8\xdb\xeaI\xa1f'
output_file = 'encryptedMessage.txt'
data = b'16blocks of text let just put a lot of text here longer than 16t' # Must be a bytes object

# Create cipher object and encrypt the data
cipher = AES.new(key, AES.MODE_CBC) # Create a AES cipher object with the key using the mode CBC
ciphered_data = cipher.encrypt(pad(data, AES.block_size)) # Pad the input data and then encrypt

file_out = open(output_file, "wb") # Open file to write bytes
file_out.write(cipher.iv) # Write the iv to the output file (will be required for decryption)
file_out.write(ciphered_data) # Write the varying length ciphertext to the file (this is the encrypted data)
file_out.close()

print(ciphered_data)

# Read the data from the file
file_in = open(output_file, 'rb') # Open the file to read bytes
iv = file_in.read(16) # Read the iv out - this is 16 bytes long
ciphered_data = file_in.read() # Read the rest of the data
file_in.close()

cipher = AES.new(key, AES.MODE_CBC, iv=iv)  # Setup cipher
original_data = unpad(cipher.decrypt(ciphered_data), AES.block_size) # Decrypt and then up-pad the result
print("original data: ")
print(original_data)


