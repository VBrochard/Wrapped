import argparse
import cryptography 
import os
import sys
import PyPDF2
import getpass



parser =  argparse.ArgumentParser()

parser.add_argument('name',type=str)

filename = parser.parse_args().name

print(filename)
