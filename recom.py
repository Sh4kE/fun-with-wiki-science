from pymongo import MongoClient
from gensim import corpora, models, similarities
import gensim

db = MongoClient().articles.entries

lda = gensim.models.LdaModel.load('data/lda_model')
dic = gensim.corpora.Dictionary.load_from_text('data/wiki_en_wordids.txt')

def entry2bow(entry):
    return dic.doc2bow(entry['text'].lower().split())
    
def bow2topics(bow):
    return lda[bow]

def entry2topics(entry):
    return bow2topics(entry2bow(entry))
    
