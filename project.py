from pymongo import MongoClient
from gensim import corpora, models, similarities
import gensim
import recom as r

db = MongoClient().projects.project

class Project(object):

    def __init__(self, name = ''):
        self.bow = []
        self.name = name
        self.read = []

    def add2bow(self, doc):
        docbow = r.entry2bow(doc)
        self.bow = [(e,f+h) for e,f in self.bow for g,h in docbow if e == g]
        es = [e for e,_ in self.bow]
        self.bow += filter(lambda (g,h): not g in es, docbow) if self.bow != [] else docbow
        
    def subfrombow(self, doc):
        docbow = r.entry2bow(doc)
        self.bow = [(e,f-h) for e,f in self.bow for g,h in docbow if e == g]
        self.bow = filter(lambda (e,f): f > 0, self.bow)

    def save(self):
        db.save(self)

    def load(self, name=''):
        p = db.find_one({'name': name})
        self.bow = p.bow
        self.name = p.name

    def read(self, doc):
        read += doc['index']
