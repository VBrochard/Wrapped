import argparse
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidTag
import os
import sys
from pypdf import PdfReader, PdfWriter
from typing import Union,Literal,List
from pathlib import Path
import getpass

SALT_LENGTH = 16
NONCE_LENGTH = 12
KEY_LENGTH = 32
TAG_LENGTH = 16
ITERATIONS = 650000 

def derive_key(password,salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt = salt,
        iterations = ITERATIONS)
    return kdf.derive(password.encode())

def decrypt(output_path):
    with open(filename_path,'rb') as f:
        data = f.read()
    salt = data[:SALT_LENGTH]
    nonce = data[SALT_LENGTH:SALT_LENGTH + NONCE_LENGTH]
    tag = data[SALT_LENGTH + NONCE_LENGTH:SALT_LENGTH + NONCE_LENGTH + TAG_LENGTH]
    ciphertext = data[SALT_LENGTH + NONCE_LENGTH + TAG_LENGTH:]
    key = derive_key(mdp,salt)
    aesgcm = AESGCM(key)
    cyphertext_tag = ciphertext + tag
    try:
        data = aesgcm.decrypt(nonce,cyphertext_tag,None)
    except InvalidTag:
        raise InvalidTag("Incorrect")
    if output_path.suffix.lower() != '.pdf':
        output_path = output_path.with_suffix('.pdf')
    with open(output_path,"wb") as f:
        f.write(data)

parser =  argparse.ArgumentParser()
parser.add_argument('name',type=str)
parser.add_argument('output',type=str)

filename = parser.parse_args().name
filename_path = Path(filename)
output = parser.parse_args().output
output_path = Path(output)

mdp = getpass.getpass(prompt='Enter Password : ')

decrypt(output_path)



