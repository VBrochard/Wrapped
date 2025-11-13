import argparse
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
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



def watermark(content_pdf: Path, stamp_pdf: Path, pdf_result: Path, page_indices: Union[Literal["ALL"], List[int]] = "ALL"):
    reader = PdfReader(content_pdf)
    if page_indices == "ALL":
        page_indices = list(range(0, len(reader.pages)))
    writer = PdfWriter()
    for index in page_indices:
        content_page = reader.pages[index]
        mediabox = content_page.mediabox
        reader_stamp = PdfReader(stamp_pdf)
        image_page = reader_stamp.pages[0]
        image_page.merge_page(content_page)
        image_page.mediabox = mediabox
        writer.add_page(image_page)
    writer.encrypt(user_password="", owner_password=os.urandom(32).hex(), permissions_flag=-3900, use_128bit=True)
    with open(pdf_result, "wb") as fp:
        writer.write(fp)

def verifCheminExis(content_file, stamp_file):
    content_path = Path(content_file)
    stamp_path = Path(stamp_file)
    if not content_path.exists() or not content_path.is_file():
        raise FileNotFoundError(
            print("Fichier cible non trouvée")
        )
    if content_path.suffix.lower() != '.pdf':
        raise ValueError(
            print("Fichier cible non PDF")
        )
    if not stamp_path.exists() or stamp_path.suffix.lower() != '.pdf':
        raise ValueError(
            print("Filigrane incorrecte")
        )


def derive_key(password,salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt = salt,
        iterations = ITERATIONS)
    return kdf.derive(password.encode())

def encryptFile(input,output,password):
    input_path = Path(input)
    output_path = Path(output)
    watermark(filename,chemin_watermark,output_name,"ALL")
    salt = os.urandom(SALT_LENGTH)
    nonce = os.urandom(NONCE_LENGTH)
    key = derive_key(password,salt)
    with open(input_path, 'rb') as f:
        file_data = f.read()
    aesgcm = AESGCM(key)
    ciphertext_with_tag = aesgcm.encrypt(nonce, file_data, None)
    tag = ciphertext_with_tag[-TAG_LENGTH:]
    ciphertext = ciphertext_with_tag[:-TAG_LENGTH]
    with open(output_path, 'wb') as f:
        f.write(salt)
        f.write(nonce)
        f.write(tag)
        f.write(ciphertext)

parser =  argparse.ArgumentParser()

parser.add_argument('name',type=str)
parser.add_argument('watermarkPath',type=str)
parser.add_argument('output',type=str)


filename = parser.parse_args().name
chemin_watermark = parser.parse_args().watermarkPath
output_name = parser.parse_args().output

try:
        verifCheminExis(filename, chemin_watermark)
except FileNotFoundError as e:
        print(e)
        sys.exit(1) 
except ValueError as e:
        print(e)
        sys.exit(1)

# filigrane = input('Enter Filigrane : ')   on verra après pour le générer de manière personnalisé


mdp = getpass.getpass(prompt='Enter Encryption Password : ')
reditt = getpass.getpass(prompt='Again Same Password : ')


if mdp != reditt :
    while mdp != reditt :
        print("\nNot the same !")
        mdp = getpass.getpass(prompt='Enter Encryption Password : ')
        reditt = getpass.getpass(prompt='Again Same Password : ')

reditt = None

encryptFile(filename,output_name,mdp)
