from tkinter import *
from tkinter import messagebox
import base64

def base_64_encrypt(message):
    encode_message=message.encode("ascii")
    base64_bytes=base64.b64encode(encode_message)
    encrypt=base64_bytes.decode("ascii")

    return encrypt

def base_64_decrypt(message):
    decode_message=message.encode("ascii")
    base64_bytes=base64.b64decode(decode_message)
    decrypt=base64_bytes.decode("ascii")

    return decrypt

def encrypt(message, codebook, shift):
    encrypted = ""
    for c in message:
        if c.isalpha():
            idx = codebook.index(c)
            e_c = codebook[(idx+shift)%len(codebook)]
            encrypted += e_c
        else:
            encrypted += c

    return base_64_encrypt(encrypted)

def decrypt(message, codebook, shift):
    message = base_64_decrypt(message)
    decrypted = ""
    for c in message:
        if c.isalpha():
            idx = codebook.index(c)
            e_c = codebook[(idx-shift)%len(codebook)]
            decrypted += e_c
        else:
            decrypted += c
    return decrypted
