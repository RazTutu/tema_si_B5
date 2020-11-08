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


    # Node A becomes a server
    ServerSocketA = socket.socket()
    try:
        ServerSocketA.bind(('127.0.0.1', 1238))
    except socket.error as e:
        print(str(e))
    ServerSocketA.listen(5)
    blocks_sent = 0

    while True:
        ClientB, addressB = ServerSocketA.accept()
        print('Someone connected to us: ' + addressB[0] + ':' + str(addressB[1]))
        #ClientB.send(str.encode('You just connected to node A server\n'))

        if final_encryption_mode == 'ECB':
            # encrypt ECB
            plaintext_file = 'message.txt'
            file_in = open(plaintext_file, 'r') # Open the file to read bytes
            plaintext_data = file_in.read()
            file_in.close()
            counter = 0
            blocks_sent = 0
            substring = ""
            for character in plaintext_data:
                substring = substring + character
                counter = counter + 1
                if counter == 16:
                    blocks_sent = blocks_sent + 1
                    # encrypt this block and send it to node B
                    binary_substring = substring.encode("ascii") #convert it to binary so this can be encrypted
                    cipher = AES.new(decrypted_key, AES.MODE_ECB) # Create a AES cipher object with the key using the mode ECB
                    ciphered_data = cipher.encrypt(binary_substring) # Pad the input data and then encrypt

                    #now send it to node B
                    ClientB.send(ciphered_data)
                    # tell the server that A sent 10 blocks
                    if blocks_sent == 10:
                        blocks_sent = 0
                        print("Sent 10 blocks to node B, let's tell that to the server!")
                        node_A_message = "10"
                        ClientSocket.send(node_A_message.encode("ascii"))
                        
                        response = ClientSocket.recv(2048)
                        plain_response = response.decode('utf-8')
                        print("Server said", plain_response)

                    substring = ""
                    counter = 0

            sent_full_blocks = "1234567890123456"
            sent_full_blocks_binary = sent_full_blocks.encode("ascii")
            cipher = AES.new(decrypted_key, AES.MODE_ECB)
            ciphered_data = cipher.encrypt(sent_full_blocks_binary)
            ClientB.send(ciphered_data)
            # send this and send if there is needed one more decryption with padding
            padded_string = ""
            more_or_not = ""
            if counter != 0:
                # tell node B that one more is coming
                more_or_not = "herecomesonemore"
                more_or_not_binary = more_or_not.encode("ascii")
                cipher = AES.new(decrypted_key, AES.MODE_ECB)
                ciphered_data = cipher.encrypt(more_or_not_binary)
                ClientB.send(ciphered_data)
                for i in range(len(plaintext_data) - counter, len(plaintext_data)):
                    padded_string = padded_string + plaintext_data[i]
                    # here we will pad the string. padded_string needs to be padded and encrypted and sent
                binary_substring = padded_string.encode("ascii") #convert it to binary so this can be encrypted
                cipher = AES.new(decrypted_key, AES.MODE_ECB) # Create a AES cipher object with the key using the mode ECB
                ciphered_data = cipher.encrypt(pad(binary_substring, AES.block_size)) # Pad the input data and then encrypt
                ClientB.send(ciphered_data)

                blocks_sent = blocks_sent + 1
                # tell the server that A sent 10 blocks
                if blocks_sent == 10:
                    blocks_sent = 0
                    print("Sent 10 blocks to node B, let's tell that to the server!")
                    node_A_message = "10"
                    ClientSocket.send(node_A_message.encode("ascii"))
                    response = ClientSocket.recv(2048)
                    plain_response = response.decode('utf-8')
                    print("Server said", plain_response)
            

            else:
                more_or_not = "nomoreblocksaaaa"
                more_or_not_binary = more_or_not.encode("ascii")
                cipher = AES.new(decrypted_key, AES.MODE_ECB)
                ciphered_data = cipher.encrypt(more_or_not_binary)
                ClientB.send(ciphered_data)

            # Tell the server that we're done
            final_message = "finish"
            ClientSocket.send(final_message.encode("ascii"))
            break

    ClientB.close()
    ServerSocketA.close()

ClientSocket.close()