import hashlib
import random
import math
from Crypto import Random
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
import binascii
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import os
import hmac

# Get a list of prime numbers between 2 and 101
# Store the results in a list to be used in diffie hellman
def get_primelist():
    result = []
    for cp in range (2, 100 + 1):
        for i in range (2, cp):
            if (cp % i == 0):
                break
        else:
            result.append(cp)
    return result


# Diffie_Hellman function for senders requesting
# To chat with someone 
def Diffie_Hellman():
    prime = get_primelist()
    # Choose g from our list of prime numbers
    g = random.choice(prime)
    while True:
        if g == prime[0]:
            g = random.choice(prime)
        else:
            break
    second_prime = []
    for x in prime:
        if x < g:
            second_prime.append(x)
        else:
            continue
    # Choose p from our list of prime numbers that are less than g
    p = random.choice(second_prime)
    print("Shared g value:", g)
    print("Shared p value:", p)
    while True:
        try:
            a = int(input("Please enter your secret key: "))
        except ValueError:
            print("Sorry, you need to enter a number")
        else:
            break
    # Calculate the first public key using the entered secret key
    A = (p**a)%g
    File = open("Diffie_Hellman_Communication.txt", "w")
    # Write the g, p and our public key to a file for the recipient to read
    File.write("Public value p is " + str(p) + "\n")
    File.write("Public value g is " + str(g) + "\n")
    File.write("Senders Public key is " + str(A) + "\n")
    File.close()
    print("The information has been sent to the recipient")
    # Check whether there has been a response from our recipient with their
    # Public key 
    while True:
        Answer = input("Press enter to check for a response")
        File = open("Diffie_Hellman_Communication.txt", "r")
        Lines = File.readlines()
        if len(Lines) > 1:
            print("There has been no response to your request yet")
        else:
            break
    Value = Lines[0].split()
    B = int(Value[4])
    File.close()
    # Calculate the secret key using the recipients public key, our private key and g
    Secret_Key = (B**a)%g
    print("Your secret Key is", Secret_Key, "This key will be used for this session of communication only")
    # Remove the text file so that there are no potential security risks
    os.remove("Diffie_Hellman_Communication.txt")
    return Secret_Key

# Diffie_Hellman function for recipients responding
# to a chat request 
def Diffie_Response():
    # Check if someone has requested to chat
    while True:
        print("Checking for message requests")
        try:
            File = open("Diffie_Hellman_Communication.txt", "r")
        except:
            print("There have been no message requests")
            Enter = input("Press enter to try again")
        else:
            break
    Info = []
    for each_line in File:
        value = each_line.split()
        Info.append(value[4])
    File.close()
    # Extract our g, p, and A(Senders public key) values from the text file 
    g = int(Info[1])
    p = int(Info[0])
    A = int(Info[2])
    # Establish a private key for the recipient
    while True:
        try:
            b = int(input("Please enter your private key: "))
        except ValueError:
            print("Sorry, you need to enter a number")
        else:
            break
    # Calculate the recipients public key and sent it back
    # To the sender via the same text file
    B = (p**b)%g
    File = open("Diffie_Hellman_Communication.txt", "w")
    File.write("Recipients public key is " + str(B))
    File.close()
    # Calculate the secret key using, the senders public key, our private key, and g
    Secret_Key = (A**b)%g
    print("Your secret Key is", Secret_Key, "This key will be used for this session of communication only")
    return Secret_Key


# AES class responsible for establising our AES object containing the
# Key as well as functions for encrypting and decrypting messages 
class AESEncryptorDecryptor(object):
    def __init__(self, key, key_len):
        # Establish block size, and key length
        # Then expand the key using the scrypt module and a
        # Pre-established salt value (could be random but would have to be sent)
        self.fixed_block_size = AES.block_size
        key = key.encode()
        salt = b'\xaa\xa6\xa0\xefl\x14Z\xea\xaf\x04\x16-\x8f 2\x00'
        self.master_key = scrypt(key, salt, key_len, N=2**4, r=8, p=1)

    # Function for encrypting plaintext using AES
    # Pads plaintext and establishes a initialization vector for
    # CBC and CFB
    def encrypt(self, plaintext, method):
        plaintext = self.add_padding(plaintext)
        inialization_vector = Random.new().read(self.fixed_block_size)
        # Using the mode of operation chosen, create a cipher object 
        if method == "ECB":
            cipher = AES.new(self.master_key, AES.MODE_ECB)
        if method == "CBC":
            cipher = AES.new(self.master_key, AES.MODE_CBC, inialization_vector)
        if method == "CFB":
            cipher = AES.new(self.master_key, AES.MODE_CFB, inialization_vector)
        # Encrypt the padded plaintext 
        text = cipher.encrypt(plaintext.encode())
        # Return b64 encoded bytes 
        return b64encode(inialization_vector + text).decode("utf-8")

    # Function for decrypting plaintext using AES
    # Decodes the b64 encoded cipher text
    # and establishes an initialization vector for CBC and CFB
    def decrypt(self, text, method):
        text = b64decode(text)
        inialization_vector = text[:self.fixed_block_size]
        # Using the mode of operation chosen, create a cipher object
        if method == "ECB":
            cipher = AES.new(self.master_key, AES.MODE_ECB)
        if method == "CBC":
            cipher = AES.new(self.master_key, AES.MODE_CBC, inialization_vector)
        if method == "CFB":
            cipher = AES.new(self.master_key, AES.MODE_CFB, inialization_vector)
        # Decrypt the cipher text 
        plaintext = cipher.decrypt(text[self.fixed_block_size:]).decode("utf-8")
        # Return the unpadded plaintext 
        return self.remove_padding(plaintext)


    # Pads the plaintext to be a multiple of 128 bits
    def add_padding(self, plaintext):
        extra_bytes = self.fixed_block_size - len(plaintext) % self.fixed_block_size
        extra = chr(extra_bytes)
        padding_str = extra_bytes * extra
        padded_plaintext = plaintext + padding_str
        return padded_plaintext

    # Unpads padded plaintext
    @staticmethod
    def remove_padding(plaintext):
        finalindex = plaintext[len(plaintext) - 1:]
        return plaintext[:-ord(finalindex)]


# Function for sending messages using the secret key created by DH
def Send_Message(Secret_Key):
    # User input for key length and mode of operation
    while True:
        Key_Len = input("What length of bytes would you like your key? 16/24/32: ")
        if Key_Len != "16"  and Key_Len != "24" and Key_Len != "32":
            print("Sorry you have to choose a valid option")
        else:
            break
    while True:
        Method = input("What mode of operation would you like to use? ECB/CBC/CFB: ")
        if Method != "ECB" and Method != "CBC" and Method != "CFB":
            print("Sorry you have to choose a valid option")
        else:
            break
    # Initializing an AESCipher object using the inputs
    Encryptor = AESEncryptorDecryptor(str(Secret_Key), int(Key_Len))
    Plaintext = input("Please enter the message you would like to send: ")
    # Encrypt the plaintext
    Encrypted = Encryptor.encrypt(Plaintext, Method)
    ByteKey = str(Secret_Key).encode()
    ByteEncrypted = Encrypted.encode()
    # Create a HMAC to be sent with the messge 
    h = hmac.new(ByteKey, ByteEncrypted, hashlib.sha256)
    File = open("Sent_Message.txt", "w")
    # Write the encrypted message to a text file for the reciever to read
    File.write(str(h.hexdigest()) + " " + Encrypted)
    File.close()
    print("You have sent a message")


# Function for receiving messages using the secret key created by DH
def Recieve_Message(Secret_Key):
    # User input values 
    while True:
        Key_Len = input("What length of bytes would you like your key? 16/24/32: ")
        if Key_Len != "16"  and Key_Len != "24" and Key_Len != "32":
            print("Sorry you have to choose a valid option")
        else:
            break
    while True:
        Method = input("What mode of operation would you like to use? ECB/CBC/CFB: ")
        if Method != "ECB" and Method != "CBC" and Method != "CFB":
            print("Sorry you have to choose a valid option")
        else:
            break
    # Initializing an AESCipher object using the inputs
    Decryptor = AESEncryptorDecryptor(str(Secret_Key), int(Key_Len))
    #Check if there has been any messages sent 
    while True:
        try:
            File = open("Sent_Message.txt", "r")
        except:
            print("You have recieved no message")
            Enter = input("Press enter to check again")
        else:
            break
    # Obtain the encrypted message and the HMAC 
    Lines = File.readlines()
    Encrypted_Message = Lines[0]
    Encrypted_Message = Encrypted_Message.split()
    HMAC_sender = Encrypted_Message[0]
    Encrypted_Message = Encrypted_Message[1]
    ByteKey = str(Secret_Key).encode()
    Encrypted_Message = Encrypted_Message.encode()
    # Create our own HMAC to compare to the senders
    h = hmac.new(ByteKey, Encrypted_Message, hashlib.sha256)
    print("Your HMAC is: " + str(h.hexdigest()))
    print("Senders HMAC is: " + HMAC_sender)
    File.close()
    os.remove("Sent_Message.txt")
    # If the HMACs are the same, the message is authentic
    # Otherwise alert the user to the third party
    if HMAC_sender == str(h.hexdigest()):
        print("HMAC is the same, the sender is authenticated")
        Decrypted = Decryptor.decrypt(Encrypted_Message, Method)
        print("Message recieved: ", Decrypted)
    else:
        print("This message is from a third party!!")


# Recurrent function that user uses to send and
# Recieve messages
def Message_Function():
    while True:
        Message_Type = input("Would you like to send or recieve a message? S/R: ")
        if Message_Type != "S" and Message_Type != "R":
            print("Sorry, you need to enter a valid option")
        else:
            break
    if Message_Type == "S":
        Send_Message(Secret_Key)
    if Message_Type == "R":
        Recieve_Message(Secret_Key)
    Message_Function()

# Establish who is our sender and who is our reciever 
while True:
    Second = input("Are you requesting communicaiton or are you recieving the request? S/R:   ")
    if Second != "S" and Second != "R":
        print("Sorry, you need to enter a valid option")
    else:
        break
if Second == "S":
    Secret_Key = Diffie_Hellman()
    Message_Function()
if Second == "R":
    Secret_Key = Diffie_Response()
    Message_Function()



