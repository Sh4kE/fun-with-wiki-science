import sh
from pymongo import MongoClient

pdf2txt = sh.Command('pdf2txt.py')

def update_db_with_pdf_texts():
  client = MongoClient()
  db = client.articles.entries
  [db.update({'_id' : entry['_id'], {'text': preprocess(entry)}) for entry in db.find()]

def preprocess(entry):
    result = pdf2txt(entry['path'])
    return result
