import socket
import os
from _thread import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from random import randrange

# 128 bits keys
# keys generated with
# key = get_random_bytes(16) # 16 bytes * 8 = 128 bits
K1 = b'\x0b\x08\x86\xedL\xdfm\xfcP\xe0\x91\xbb\xec\x8b\xd7\x9e'
K2 = b'\xdb\xd3\xea\xf1\xb9\xbf\x06R\xcf\xc5#zh\x0c\xa9q'
K3 = b'\xe6\xbe\x0e\xbf\xe60\xe2\x89\x99Q\xe6\x14+"D\xb6'
# generate the initialization vector here as well
non_initialized_vector = 'textrandombattle'

def encrypt_k1():
    key = K3 
    plaintext = K1
    cipher = AES.new(key, AES.MODE_ECB) # Create a AES cipher object with the key using the mode ECB
    # no need for padding because key is of 16 bytes, the same as an AES block
    ciphered_data = cipher.encrypt(plaintext)
    return ciphered_data

def encrypt_k2():
    key = K3 
    plaintext = K2
    cipher = AES.new(key, AES.MODE_ECB) # Create a AES cipher object with the key using the mode ECB
    # no need for padding because key is of 16 bytes, the same as an AES block
    ciphered_data = cipher.encrypt(plaintext)
    return ciphered_data

def encrypt_ecb_or_ofb_response(ecb):
    key = K3 
    plaintext = ecb.encode("ascii")
    cipher = AES.new(key, AES.MODE_ECB) # Create a AES cipher object with the key using the mode ECB
    # need to pad because it's 3 bytes instead of 16, the size of an AES block
    ciphered_data = cipher.encrypt(pad(plaintext, AES.block_size))
    return ciphered_data

def encrypt_initialization_vector(vec):
    key = K3 
    plaintext = vec.encode("ascii")
    cipher = AES.new(key, AES.MODE_ECB) # Create a AES cipher object with the key using the mode ECB
    # no need for padding because key is of 16 bytes, the same as an AES block
    ciphered_data = cipher.encrypt(pad(plaintext, AES.block_size))
    return ciphered_data

def decrypt_confirmation_ecb(encrypted_text):
    cipher = AES.new(K1, AES.MODE_ECB)  # Setup cipher
    original_data = unpad(cipher.decrypt(encrypted_text), AES.block_size) 
    return original_data

def decrypt_confirmation_ofb(encrypted_message):
    cipher = AES.new(K2, AES.MODE_OFB, non_initialized_vector.encode('ascii'))
    original_data = cipher.decrypt(encrypted_message)
    return original_data

ServerSocket = socket.socket()
try:
    ServerSocket.bind(('127.0.0.1', 1233))
except socket.error as e:
    print(str(e))

ServerSocket2 = socket.socket()
try:
    ServerSocket2.bind(('127.0.0.1', 1234))
except socket.error as e:
    print(str(e))


print('Waitiing for a Connection..')
ServerSocket.listen(5)
ServerSocket2.listen(5)

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    Client.send(str.encode('Do you want ECB or OFB mode?\n'))

    Client2, address2 = ServerSocket2.accept()
    print('Connected to: ' + address2[0] + ':' + str(address2[1]))
    Client2.send(str.encode('Do you want ECB or OFB mode?\n'))

    
    while True:
        #in al doilea while, adica in asta, cred ca comunici efectiv chestii
        decision_node_A = Client.recv(2048)
        reply = 'Server received and Says: ' + decision_node_A.decode('utf-8')
        if not decision_node_A:
            break
        print("Node A decided he wants", decision_node_A.decode('utf-8'))

        decision_node_B = Client2.recv(2048)
        reply2 = 'Server received and Says: ' + decision_node_B.decode('utf-8')
        if not decision_node_B:
            break
        print("Node B decided he wants", decision_node_B.decode('utf-8'))

        answer_from_A = decision_node_A.decode('utf-8')
        answer_from_B = decision_node_B.decode('utf-8')
        final_encryption_mode = ''
        initialization_vector = ''
        encrypted_key = ''
        final_encryption_mode__plaintext = ''
        # see if they want ECB or OFB and give them back the encrypted key
        if answer_from_A == answer_from_B and answer_from_A == 'ECB':
            print("Ambele noduri vor ECB")
            # criptez cheia K1 si o trimit
            final_encryption_mode = encrypt_ecb_or_ofb_response('ECB')
            final_encryption_mode__plaintext = 'ECB'
            encrypted_key = encrypt_k1()
            initialization_vector = encrypt_initialization_vector('no')

        elif answer_from_A == answer_from_B and answer_from_A == 'OFB':
            print("Ambele noduri vor OFB")
            final_encryption_mode = encrypt_ecb_or_ofb_response('OFB')
            final_encryption_mode__plaintext = 'OFB'
            encrypted_key = encrypt_k2()
            # criptez cheia K2 si o trimit, impreuna cu vectorul de initializare
            initialization_vector = encrypt_initialization_vector(non_initialized_vector)
        else:
            print("Nodes didn't give the same input. We will choose the encryption method random :)")
            # aleg random un mod
            random_number = randrange(2) # 0 or 1
            if random_number == 0:
                print("The server decided to choose ECB")
                # ECB
                final_encryption_mode = encrypt_ecb_or_ofb_response('ECB')
                final_encryption_mode__plaintext = 'ECB'
                encrypted_key = encrypt_k1()
                initialization_vector = encrypt_initialization_vector('no')
            elif random_number == 1:
                print("The server decided to choose OFB")
                # OFB
                final_encryption_mode = encrypt_ecb_or_ofb_response('OFB')
                final_encryption_mode__plaintext = 'OFB'
                encrypted_key = encrypt_k2()
                initialization_vector = encrypt_initialization_vector(non_initialized_vector)
            

        print("acum le transmit nodurilor mesajul")
        # send back to the clients the encryption mode
        Client.send(final_encryption_mode)
        Client2.send(final_encryption_mode)
        # send key to the clients
        Client.send(encrypted_key)
        Client2.send(encrypted_key)
        # send the initialization vector(If it's ECB it will be an empty string)
        Client.send(initialization_vector)
        Client2.send(initialization_vector)

        #receive confirmation from the server
        if final_encryption_mode__plaintext == 'ECB':
            confirmation_node_A_enc = Client.recv(2048)
            confirmation_node_A = decrypt_confirmation_ecb(confirmation_node_A_enc) 
            print("Server received confirmation: ", confirmation_node_A.decode('utf-8'))

            confirmation_node_B_enc = Client2.recv(2048)
            confirmation_node_B = decrypt_confirmation_ecb(confirmation_node_B_enc) 
            print("Server received confirmation: ", confirmation_node_B.decode('utf-8'))

        elif final_encryption_mode__plaintext == 'OFB':
            confirmation_node_A_enc = Client.recv(2048)
            confirmation_node_A = decrypt_confirmation_ofb(confirmation_node_A_enc)
            print("Server received confirmation:", confirmation_node_A.decode('utf-8'))

            confirmation_node_B_enc = Client2.recv(2048)
            confirmation_node_B = decrypt_confirmation_ofb(confirmation_node_B_enc)
            print("Server received confirmation:", confirmation_node_B.decode('utf-8'))

    Client2.close()
    Client.close()
    

ServerSocket.close()
ServerSocket2.close()



#DESCHIDE INTREBARILE DE MAI JOS
#https://stackoverflow.com/questions/10810249/python-socket-multiple-clients
#https://docs.python.org/3/library/socketserver.html#socketserver-tcpserver-example