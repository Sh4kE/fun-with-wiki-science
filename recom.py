from pymongo import MongoClient
from gensim import corpora, models, similarities
import gensim

db = MongoClient().articles.entries

lda = gensim.models.LdaModel.load('data/lda400')
dic = gensim.corpora.Dictionary.load_from_text('data/wiki_en_wordids.txt')

def entry2bow(entry):
    return dic.doc2bow(entry['text'].lower().split())
    
def bow2topics(bow):
    return lda[bow]

def entry2topics(entry):
    return bow2topics(entry2bow(entry))
    
def compute_sims(bow, read=[]):
    entries = list(enumerate(db.find()))
    index = similarities.MatrixSimilarity(lda[[entry2bow(entry[1]['text']) for entry in entries]])
    sims = index[lda[bow]]
    return sims

    
    
