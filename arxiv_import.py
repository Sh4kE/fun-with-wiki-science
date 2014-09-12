from bs4 import BeautifulSoup
import urllib
import config as c
from pymongo import MongoClient

client = MongoClient()
db = client.articles.entries

def generate_filename(entry, directory = ''):
  authors = [a.split()[-1] for a in entry['authors']]
  authors = authors[0]+'_et.al' if len(authors) > 1 else authors[0]
  title = entry['title'].replace(' ', '_')
  return ''.join([directory, authors,'-',title , '.pdf'])

def dl_pdf_from_arxiv(url):
  html_doc = urllib.urlopen(url).read()
  s = BeautifulSoup(html_doc)
  entries = [{
    'pdf' : e.findAll('link',attrs={'type': 'application/pdf'})[0]['href'],
    'url' : e.findAll('link',attrs={'type': 'text/html'})[0]['href'],
    'authors': [str(a.next.next.next) for a in e.findAll('author')],
    'title': str(e.title.next),
    'id': str.split(str(e.id.next),'/')[-1]
            } for e in s.findAll('entry')]
  entries = filter(lambda e: db.find_one({'id': e['id']}) == None, entries)
  print "entries: ", entries
  map(lambda e: urllib.urlretrieve(e['pdf'], generate_filename(e, directory = c.ARTICLE_DIR)), entries)


def stripAllTags(html):
        if html is None:
                return None
        return ''.join( BeautifulSoup( html ).findAll() )
