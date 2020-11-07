import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

# key
K3 = b'\xe6\xbe\x0e\xbf\xe60\xe2\x89\x99Q\xe6\x14+"D\xb6'

def decrypt_key(encryption_key):
    cipher = AES.new(K3, AES.MODE_ECB)  # Setup cipher
    original_data = cipher.decrypt(encryption_key) 
    return original_data

def decrypt_mode(encrypted_text):
    cipher = AES.new(K3, AES.MODE_ECB)  # Setup cipher
    original_data = unpad(cipher.decrypt(encrypted_text), AES.block_size) 
    return original_data

def decrypt_vector(encrypted_vector):
    cipher = AES.new(K3, AES.MODE_ECB)  # Setup cipher
    original_data = unpad(cipher.decrypt(encrypted_vector), AES.block_size) 
    return original_data

def encrypt_confirmation_message_ecb(key, message):
    cipher = AES.new(key, AES.MODE_ECB) # Create a AES cipher object with the key using the mode ECB
    # no need for padding because key is of 16 bytes, the same as an AES block
    ciphered_data = cipher.encrypt(pad(message.encode('ascii'), AES.block_size))
    return ciphered_data

def encrypt_confirmation_message_ofb(key, message, initialization_vector):
    cipher = AES.new(key, AES.MODE_OFB, initialization_vector)
    ciphered_data = cipher.encrypt(message.encode('ascii'))
    return ciphered_data


ClientSocket = socket.socket()
print('Waiting for connection')
try:
    ClientSocket.connect(('127.0.0.1', 1233))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(1024)
print(Response)
while True:
    Input = input('Say Something: ')
    ClientSocket.send(str.encode(Input))
    #Response = ClientSocket.recv(1024)
    #print(Response.decode('utf-8'))

    # now got 3 answers from server with encryption_mode, key, and initialization_vector
    
    encryption_mode = ClientSocket.recv(1024)
    encryption_key = ClientSocket.recv(1024)
    initialization_vector = ClientSocket.recv(1024)
    print("initialization vector is", initialization_vector)

    # decrypt the final encryption method with K3 sent from the server(ecb or ofb but encrypted)
    final_encryption_mode = decrypt_mode(encryption_mode).decode("utf-8")
    print("The mode we will encrypt is", final_encryption_mode)
    # decrypted the key and stored it inside decrypted_key
    decrypted_key = decrypt_key(encryption_key)
    print("Cheia decriptata folosind K3 este", decrypted_key)
    # decrypt the initialization vector response
    decrypted_vector = decrypt_vector(initialization_vector)
    print("The initialization vector is", decrypted_vector)

    # send confirmation message back to the server
    message = 'Node A'
    if final_encryption_mode == 'ECB':
        #encrypt the message with ecb
        confirmation_message = encrypt_confirmation_message_ecb(decrypted_key, message)
        print("confirmation message is", confirmation_message)
        ClientSocket.send(confirmation_message)
    elif final_encryption_mode == 'OFB':
        #encrypt the message with ofb
        confirmation_message = encrypt_confirmation_message_ofb(decrypted_key, message, decrypted_vector)
        print("confirmation message is", confirmation_message)
        ClientSocket.send(confirmation_message)

ClientSocket.close()