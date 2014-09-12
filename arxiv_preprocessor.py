from bs4 import BeautifulSoup
import sh

pdf2txt = sh.Command('pdf2txt.py')

def preprocess(entry):
    result = pdf2txt(entry['
