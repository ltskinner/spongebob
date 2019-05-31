
import sys
import os

import docx2txt
import random

from docx import Document
from docx.shared import Inches

import argparse

import os.path

f = open("banner.txt", 'r', encoding='utf-8')
print(f.read())
f.close()


def spongebobify(text=None, file_to_convert=None):
    if text is None and file_to_convert is None:
        raw_text = input("EntEr The TexT YOu WaNT tO cONvERt:\n")
        file_to_convert = "spongebob"

    elif file_to_convert is not None:
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

    elif text is not None:
        raw_text = text
        file_to_convert = "spongebob"

    sponge_text = to_spongebob_text(raw_text)
    docx_text = insert_picture_to_docx(sponge_text)

    sponge_file = name_docx_file(file_to_convert)
    write_to_docx(docx_text, sponge_file)
    display_text_to_terminal(sponge_text, sponge_file)

    return sponge_text


def to_spongebob_text(raw_text):
    raw_text = raw_text.lower()
    length = 2 + int(len(raw_text)/2)
    cases = [0]*length + [1]*length
    random.shuffle(cases)

    last, prev = 0, 0
    for i in range(len(cases)):
        if cases[i] == last and cases[i] == prev:  # Three in a row
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


def name_docx_file(file_to_convert):
    file_to_convert = file_to_convert.replace('.', "_spongebob.")
    return str(to_spongebob_text(file_to_convert.split('.')[0]) + ".docx")


def write_to_docx(docx_text, sponge_file):
    my_path = os.path.abspath(os.path.dirname(__file__))
    pic_path = os.path.join(my_path, 'spongebob.jpg')
    text_segs = docx_text.split("|SPONGEPIC|")

    document = Document()
    document.add_paragraph(text_segs[0])
    document.add_picture(pic_path, width=Inches(6))
    document.add_paragraph(text_segs[1])

    document.save(sponge_file)


def insert_picture_to_docx(sponge_text):
    newlines = sponge_text.split('\n')
    if len(newlines) > 2:
        newlines.insert(int(len(newlines)/2), "|SPONGEPIC|")
    elif len(newlines) == 1:
        newwords = newlines[0].split(' ')
        if len(newwords) > 2:
            newwords.insert(int(len(newwords)/2), "|SPONGEPIC|")
        else:
            newwords.append("|SPONGEPIC|")
        newlines[0] = ' '.join(newwords)

    return '\n'.join(newlines)


def display_text_to_terminal(sponge_text, sponge_file):
    width = os.get_terminal_size().columns - 3
    print("+" + ''.join(['-' for _ in range(width)]) + "+")
    print("|" + sponge_file.center(width) + "|")
    print("+" + ''.join(['-' for _ in range(width)]) + "+")
    print(sponge_text)
    print("+" + ''.join(['-' for _ in range(width)]) + "+")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert text into SpOngEBOb TExT")
    parser.add_argument("--file_to_convert", help="TeXt fiLe to CoNVerT")
    args = parser.parse_args()

    spongebobify(file_to_convert=args.file_to_convert)
