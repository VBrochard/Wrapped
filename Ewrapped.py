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

parser =  argparse.ArgumentParser()

parser.add_argument('name',type=str)
parser.add_argument('output',type=str)

filename = parser.parse_args().name
output_name = parser.parse_args().output

filigrane = input('Enter Filigrane : ')
mdp = getpass.getpass(prompt='Enter Encryption Password : ')
reditt = getpass.getpass(prompt='Again Same Password : ')

if mdp != reditt :
    print("Not the same !")
    sys.exit()
else:
    reditt = None

watermark(filename,"watermark.pdf","watermarker.pdf","ALL")
