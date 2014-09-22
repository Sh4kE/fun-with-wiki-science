import sh
import magic
from pymongo import MongoClient

mime = magic.Magic(mime=True)
db = MongoClient().articles.entries
pdftotext = sh.Command('pdftotext').bake('-enc', 'ASCII7')

def update_db_with_pdf_texts(indices=[e['index'] for e in db.find() if not e.has_key('text')]):
  for entry in [db.find_one({'index': index}) for index in indices]:
    if entry and is_pdf(entry) and not entry.has_key('text'):
        db.save(preprocess(entry))
    if not is_pdf(entry):
      db.remove(entry)
      #TODO: DELETE PDF!

def is_pdf(entry):
    return mime.from_file(entry['path']) == 'application/pdf'

def preprocess(entry):
  entry['text'] = pdftotext(entry['path'], '-').encode('ascii')
  return entry
