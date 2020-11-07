from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad


#ENCRYPTION
key = b'\x9f\xdcf\xacF\xb1\xbdlQ\xde`\xfei\xc1\xe0\x04' # key of 128 bits
output_file = 'ecbEncryptedText.bin'
plaintext_file = 'plaintextECB.txt'
plaintext_data = None

# the plaintext will be stored inside plaintext_data
# it is already in bytes because of the rb parameter
file_in = open(plaintext_file, 'r') # Open the file to read bytes
plaintext_data = file_in.read()
file_in.close()
file_out = open(output_file, "wb") # Open file to write bytes

counter = 0
substring = ""
for character in plaintext_data:
    substring = substring + character
    counter = counter + 1
    if counter == 16:
        # encrypt this block and write it to file
        binary_substring = substring.encode("ascii") #convert it to binary so this can be encrypted
        cipher = AES.new(key, AES.MODE_ECB) # Create a AES cipher object with the key using the mode ECB
        ciphered_data = cipher.encrypt(binary_substring) # Pad the input data and then encrypt
        file_out.write(ciphered_data) # Write the varying length ciphertext to the file (this is the encrypted data)

        substring = ""
        counter = 0

padded_string = ""
if counter != 0:
    for i in range(len(plaintext_data) - counter, len(plaintext_data)):
        padded_string = padded_string + plaintext_data[i]
        # here we will pad the string. padded_string needs to be padded and encrypted and wrote to the file
    binary_substring = substring.encode("ascii") #convert it to binary so this can be encrypted
    cipher = AES.new(key, AES.MODE_ECB) # Create a AES cipher object with the key using the mode ECB
    ciphered_data = cipher.encrypt(pad(binary_substring, AES.block_size)) # Pad the input data and then encrypt
    file_out.write(ciphered_data) # Write the varying length ciphertext to the file (this is the encrypted data)
file_out.close()

# DECRYPTION
key = b'\x9f\xdcf\xacF\xb1\xbdlQ\xde`\xfei\xc1\xe0\x04' # key of 128 bits
encrypted_file = 'ecbEncryptedText.bin'
file_in = open(encrypted_file, 'rb') # Open the file to read bytes
encrypted_data = file_in.read()
file_in.close()

counter = 0
aux_list = []
initial_plaintext = ""
for i in range(len(encrypted_data) - 16):
    counter = counter + 1
    aux_list.append(encrypted_data[i])
    if counter == 16:
        # decrypt
        cipher = AES.new(key, AES.MODE_ECB)  # Setup cipher
        original_data = cipher.decrypt(bytes(aux_list)) # Decrypt and then up-pad the result
        initial_plaintext = initial_plaintext + original_data.decode("UTF-8")
        counter = 0
        aux_list = []

unpadded_text = []
for i in range(len(encrypted_data) - 16, len(encrypted_data)):
    unpadded_text.append(encrypted_data[i])
cipher = AES.new(key, AES.MODE_ECB)  # Setup cipher
original_data = unpad(cipher.decrypt(bytes(unpadded_text)), AES.block_size) # Decrypt and then up-pad the result
initial_plaintext = initial_plaintext + original_data.decode("UTF-8")


print("initial plaintext is:",initial_plaintext)