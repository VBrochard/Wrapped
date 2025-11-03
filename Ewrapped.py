import argparse
import cryptography 
import os
import sys
import PyPDF2
import getpass



parser =  argparse.ArgumentParser()

parser.add_argument('name',type=str)
parser.add_argument('output',type=str)

filename = parser.parse_args().name
output_name = parser.parse_args().output

print(filename)
print(output_name)



