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


parser =  argparse.ArgumentParser()

parser.add_argument('name',type=str)

filename = parser.parse_args().name
filename_path = Path(filename)