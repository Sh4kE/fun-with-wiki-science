from pymongo import MongoClient
from gensim import corpora, models, similarities
import gensim
import recom as r

db = MongoClient().projects.project

class Project(object):

    def __init__(self, name = ''):
        self.bow = []
        self.name = name
        self.read_doc = []

    def add2bow(self, doc):
        docbow = r.entry2bow(doc)
        self.bow = [(e,f+h) for e,f in self.bow for g,h in docbow if e == g]
        es = [e for e,_ in self.bow]
        self.bow += filter(lambda (g,h): not g in es, docbow) if self.bow != [] else docbow

    def subfrombow(self, doc):
        docbow = r.entry2bow(doc)
        self.bow = [(e,f-h) for e,f in self.bow for g,h in docbow if e == g]
        self.bow = filter(lambda (e,f): f > 0, self.bow)

    def serialize(self):
        return self.__dict__

    def save(self):
        db.save(self.serialize())

    def load(self, name=''):
        p = db.find_one({'name': name})
        self.bow = p['bow']
        self.name = p['name']
        self.read_doc = p['read_doc']

    def read(self, doc):
      self.read_doc.append(doc['index'])

    def up(self, doc):
      self.read(doc)
      self.add2bow(doc)
      self.save()

    def down(self, doc):
      self.read(doc)
      self.subfrombow(doc)
      self.save()
