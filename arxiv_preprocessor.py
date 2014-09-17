import sh
from pymongo import MongoClient

pdf2txt = sh.Command('pdf2txt.py').bake('-c ascii')

def update_db_with_pdf_texts():
  client = MongoClient()
  db = client.articles.entries

  for entry in db.find():
    if not entry.has_key('text'):
      db.save(preprocess(entry))

def preprocess(entry):
    entry['text'] = pdf2txt(entry['path']).encode('ascii')
    return entry
