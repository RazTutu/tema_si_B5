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

def decrypt_ecb(key, message):
    cipher = AES.new(key, AES.MODE_ECB)  # Setup cipher
    original_data = cipher.decrypt(message)
    return original_data

def decrypt_ecb_unpad(key, message):
    cipher = AES.new(key, AES.MODE_ECB)  # Setup cipher
    original_data = unpad(cipher.decrypt(message), AES.block_size)
    return original_data

def bxor(ba1, ba2):
    """ XOR two byte strings """
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def simple_ecb_encryption_for_ofb_implementation(key, message):
    cipher = AES.new(key, AES.MODE_ECB) # Create a AES cipher object with the key using the mode ECB
    # no need for padding because key is of 16 bytes, the same as an AES block
    ciphered_data = cipher.encrypt(message)
    return ciphered_data

def own_unpad(string):
    aux_string = ""
    for character in string:
        if(character != "_"):
            aux_string = aux_string + character
    return aux_string


ClientSocket = socket.socket()
print('Waiting for connection')
try:
    ClientSocket.connect(('127.0.0.1', 1234))
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
    message = 'Node B'
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

    
    ClientSocketToA = socket.socket()
    print('Waiting for connection')
    try:
        ClientSocketToA.connect(('127.0.0.1', 1238))
    except socket.error as e:
        print(str(e))

    number_of_messages = 0
    full_text = ""
    blocks_received = 0

    if final_encryption_mode == "ECB":
        while True:
            finished_full_blocks = False
            ResponseNodB = ClientSocketToA.recv(16)
            print("Node B received:", ResponseNodB)
        
            print("size of message received:", len(ResponseNodB))
            original_text = decrypt_ecb(decrypted_key, ResponseNodB)
            print(original_text.decode('utf-8'))
            if original_text.decode('utf-8') != "1234567890123456":
                full_text = full_text + original_text.decode('utf-8')
                blocks_received = blocks_received + 1
                if blocks_received == 10:
                    blocks_received = 0
                    # tell the server you received 10 blocks
                    print("Received 10 blocks")
                    node_B_message = "10"
                    ClientSocket.send(node_B_message.encode("ascii"))
                    response = ClientSocket.recv(2048)
                    plain_response = response.decode('utf-8')
                    print("Server said", plain_response)

            number_of_messages += 1
            if original_text.decode('utf-8') == "1234567890123456":
                ResponseNodB = ClientSocketToA.recv(16)
                original_text = decrypt_ecb(decrypted_key, ResponseNodB)
                after_full_blocks = original_text.decode('utf-8')
            
                if after_full_blocks == "herecomesonemore":
                    ResponseNodB = ClientSocketToA.recv(16)
                    original_text = decrypt_ecb_unpad(decrypted_key, ResponseNodB)
                    print(original_text.decode('utf-8'))
                    full_text = full_text + original_text.decode('utf-8')
                    blocks_received = blocks_received + 1
                    if blocks_received == 10:
                        blocks_received = 0
                        # tell the server you received 10 blocks
                        node_B_message = "10"
                        ClientSocket.send(node_B_message.encode("ascii"))
                        response = ClientSocket.recv(2048)
                        plain_response = response.decode('utf-8')
                        print("Server said", plain_response)
                    break 
                elif after_full_blocks == "nomoreblocksaaaa":
                    break

        print("Full decrypted text:", full_text)
        # Tell the server that we're done
        final_message = "finish"
        ClientSocket.send(final_message.encode("ascii"))
    
    elif final_encryption_mode == "OFB":
        blocks_received = 0
        print("decrypting using OFB")
        final_message = ""
        while True:
            finished_full_blocks = False
            ResponseNodB = ClientSocketToA.recv(16)
            print("Node B received:", ResponseNodB)
        
            print("size of message received:", len(ResponseNodB))
            #implement own decryption method
            block_cipher_encryption = simple_ecb_encryption_for_ofb_implementation(decrypted_key, decrypted_vector)
            decrypted_vector = block_cipher_encryption
            original_text = bxor(ResponseNodB, block_cipher_encryption)

            print("original text is", original_text)
            if original_text.decode('utf-8') != "abc4567890123456":
                final_message = final_message + original_text.decode('utf-8')
                blocks_received = blocks_received + 1
                if blocks_received == 10:
                    blocks_received = 0
                    # tell the server you received 10 blocks
                    print("Received 10 blocks")
                    node_B_message = "10"
                    #ClientSocket.send(node_B_message.encode("ascii"))
                    #response = ClientSocket.recv(2048)
                    #plain_response = response.decode('utf-8')
                    #print("Server said", plain_response)

            number_of_messages += 1
            if original_text.decode('utf-8') == "abc4567890123456":
                ResponseNodB = ClientSocketToA.recv(16)
                #original_text = decrypt_ecb(decrypted_key, ResponseNodB)

                block_cipher_encryption = simple_ecb_encryption_for_ofb_implementation(decrypted_key, decrypted_vector)
                decrypted_vector = block_cipher_encryption
                original_text = bxor(ResponseNodB, block_cipher_encryption)

                after_full_blocks = original_text.decode('utf-8')
            
                if after_full_blocks == "herecomesonemore":
                    ResponseNodB = ClientSocketToA.recv(16)

                    #own unpad function
                    block_cipher_encryption = simple_ecb_encryption_for_ofb_implementation(decrypted_key, decrypted_vector)
                    decrypted_vector = block_cipher_encryption
                    original_text = bxor(ResponseNodB, block_cipher_encryption)
                    original_text = own_unpad(original_text)

                    print(original_text.decode('utf-8'))
                    full_text = full_text + original_text
                    blocks_received = blocks_received + 1
                    if blocks_received == 10:
                        blocks_received = 0
                        # tell the server you received 10 blocks
                        node_B_message = "10"
                        #ClientSocket.send(node_B_message.encode("ascii"))
                        #response = ClientSocket.recv(2048)
                        #plain_response = response.decode('utf-8')
                        #print("Server said", plain_response)
                    break 
                elif after_full_blocks == "nomoreblocksaaaa":
                    break
    final_message_to_server = "finish"
    #ClientSocket.send(final_message.encode("ascii"))
    print(final_message_to_server)
    print(final_message)
    ClientSocketToA.close()

ClientSocket.close()