import argparse
import cryptography 
import os
import sys
from PyPDF2 import PdfReader,PdfWriter
from typing import Union,Literal,List
from pathlib import Path
import getpass


def watermark(
    content_pdf: Path,
    stamp_pdf: Path,
    pdf_result: Path,
    page_indices: Union[Literal["ALL"], List[int]] = "ALL",
):
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

parser =  argparse.ArgumentParser()

parser.add_argument('name',type=str)
parser.add_argument('watermarkPath',type=str)
parser.add_argument('output',type=str)


filename = parser.parse_args().name
chemin_watermark = parser.parse_args().watermarkPath
output_name = parser.parse_args().output

try:
        print("Validation des chemins...")
        verifCheminExis(filename, chemin_watermark)
except FileNotFoundError as e:
        print(e)
        sys.exit(1) 
except ValueError as e:
        print(e)
        sys.exit(1)

# filigrane = input('Enter Filigrane : ')   on verra après pour le générer de manière personnalisé

print("\n")
mdp = getpass.getpass(prompt='Enter Encryption Password : ')
reditt = getpass.getpass(prompt='Again Same Password : ')


if mdp != reditt :
    while mdp != reditt :
        print("\nNot the same !\n")
        mdp = getpass.getpass(prompt='Enter Encryption Password : ')
        reditt = getpass.getpass(prompt='Again Same Password : ')

reditt = None
watermark(filename,chemin_watermark,output_name,"ALL")
