
import sys
import os

import docx2txt
import random

from docx import Document
from docx.shared import Inches

import argparse

import os.path

print(
"""
  ___________________       _______         _____________________      __________  ___________    ____  ______________
 /   _____/\______   \____  \      \    ____\_   _____/\______   \ ____\______   \ \__    ___/___ \   \/  /\__    ___/
 \_____  \  |     ___/  _ \ /   |   \  / ___\|    __)_  |    |  _//  _ \|    |  _/   |    |_/ __ \ \     /   |    |   
 /        \ |    |  (  <_> )    |    \/ /_/  >        \ |    |   (  <_> )    |   \   |    |\  ___/ /     \   |    |   
/_______  / |____|   \____/\____|__  /\___  /_______  / |______  /\____/|______  /   |____| \___  >___/\  \  |____|   
        \/                         \//_____/        \/         \/              \/               \/      \_/           
_________         ___________   ____          ___________   __________                                                
\_   ___ \  ____  \      \   \ /   /__________\__    ___/___\______   \                                               
/    \  \/ /  _ \ /   |   \   Y   // __ \_  __ \|    |_/ __ \|       _/                                               
\     \___(  <_> )    |    \     /\  ___/|  | \/|    |\  ___/|    |   \                                               
 \______  /\____/\____|__  /\___/  \___  >__|   |____| \___  >____|_  /                                               
        \/               \/            \/                  \/       \/   
""")


def spongebobify(text=None, file_to_convert=None):

    if text == None and file_to_convert == None:
        raw_text = input("EntEr The TexT YOu WaNT tO cONvERt:\n")
        file_to_convert = "spongebob"

    elif file_to_convert != None:
        if '.docx' not in file_to_convert and '.txt' not in file_to_convert:
            print("sPEcIFy .dOcX or .Txt AnD rUn aGaiN")
            sys.exit(0)

        if file_to_convert in os.listdir():
            if '.docx' in file_to_convert:
                raw_text = docx2txt.process(file_to_convert)
            elif '.txt' in file_to_convert:
                with open(file_to_convert, 'r') as file:
                    raw_text = file.read()
        else:
            print("FIle DoeS NOt EXisT")
            sys.exit(0)

    elif text != None:
        raw_text = text
        file_to_convert = "spongebob"

    file_to_convert = file_to_convert.replace('.', "_spongebob.")
    sponge_file = str(toSpongebobText(file_to_convert.split('.')[0]) + ".docx")


    sponge_text = toSpongebobText(raw_text)
    width = os.get_terminal_size().columns - 3
    print("+" + ''.join(['-' for _ in range(width)]) + "+")
    print("|" + sponge_file.center(width) + "|")
    print("+" + ''.join(['-' for _ in range(width)]) + "+")
    print(sponge_text)
    print("+" + ''.join(['-' for _ in range(width)]) + "+")

    # 4) Insert picture midway
    newlines = sponge_text.split('\n')
    if len(newlines)>2:
        newlines.insert(int(len(newlines)/2), "|SPONGEPIC|")
    elif len(newlines) == 1:
        newwords = newlines[0].split(' ')
        if len(newwords) > 2:
            newwords.insert(int(len(newwords)/2), "|SPONGEPIC|")
        else:
            newwords.append("|SPONGEPIC|")
        newlines[0] = ' '.join(newwords)

    out_text = '\n'.join(newlines)

    # 5) Write to docx
    my_path = os.path.abspath(os.path.dirname(__file__))
    pic_path = os.path.join(my_path, 'spongebob.jpg')
    text_segs = out_text.split("|SPONGEPIC|")

    document = Document()

    document.add_paragraph(text_segs[0])
    document.add_picture(pic_path, width=Inches(6))
    document.add_paragraph(text_segs[1])

    document.save(sponge_file)

    return sponge_text


def toSpongebobText(raw_text):
    raw_text = raw_text.lower()
    length = 2 + int(len(raw_text)/2)
    cases = [0]*length + [1]*length
    random.shuffle(cases)

    last, prev = 0, 0
    for i in range(len(cases)):
        if cases[i] == last and cases[i] == prev: # Three in a row
            #print(last, prev, cases[i], 1 - cases[i])
            cases[i] = 1 - cases[i]

        last = prev
        prev = cases[i]

    sponge_text = ''
    for i in range(len(raw_text)):
        if cases[i] == 1:
            sponge_text += raw_text[i].upper()
        else:
            sponge_text += raw_text[i]
    
    return sponge_text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert text into SpOngEBOb TExT") #"Convert text into SpOngEBOb TExT"
    parser.add_argument("--file_to_convert", help="TeXt fiLe to CoNVerT") #, type=int)
    args = parser.parse_args()

    spongebobify(file_to_convert=args.file_to_convert)

