from pymongo import MongoClient
from gensim import corpora, models, similarities
import gensim
import recom as r

db = MongoClient().projects.project 

class Project(object):

    def __init__(self, name = ''):
        self.bow = []
        self.name = name

    def add2bow(self, doc):
        docbow = r.entry2bow(doc)
        self.bow = [(e,f+h) for e,f in self.bow for g,h in docbow if e == g] 
        self.bow += [(g,h) for g,h in docbow for e in [e for e,f in self.bow] if  g != e ]
    
    def subfrombow(self, doc):
        pass

    def save(self):
        db.save(self)
        
    def load(self, name=''):
        p = db.find_one({'name': name})
        self.bow = p.bow
        self.name = p.name
        

    
        
