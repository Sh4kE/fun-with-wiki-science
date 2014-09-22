from bs4 import BeautifulSoup
import urllib
import config as c
from pymongo import MongoClient

client = MongoClient()
db = client.articles.entries

def gen_index(seed=db.count()):
  i = seed
  while True:
    i +=1
    yield i

index = gen_index()

def generate_filename(entry, directory = c.ARTICLE_DIR):
  authors = [a.split()[-1] for a in entry['authors']]
  authors = authors[0]+'_et.al' if len(authors) > 1 else authors[0]
  title = entry['title'].replace(' ', '_')
  return ''.join([directory, authors,'-',title , '.pdf'])

def fetch(url):
  html_doc = urllib.urlopen(url).read()
  s = BeautifulSoup(html_doc)
  entries = [{
    'pdf' : e.findAll('link',attrs={'type': 'application/pdf'})[0]['href'],
    'url' : e.findAll('link',attrs={'type': 'text/html'})[0]['href'],
    'authors': [a.text.strip() for a in e.findAll('author')],
    'title': str(e.title.next),
    'id': str.split(str(e.id.next),'/')[-1],
    'index': next(index)
            } for e in s.findAll('entry')]
  entries = filter(lambda e: db.find_one({'id': e['id']}) == None, entries)
  for entry in entries:
    entry['path'] = generate_filename(entry)
  map(lambda e: urllib.urlretrieve(e['pdf'], e['path']), entries)
  if entries:
    db.insert(entries)
  return [e['index'] for e in entries]
