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
    entries = sorted(filter(lambda e: not e['index'] in read, db.find()), key = lambda e : e['index'])
    index = similarities.MatrixSimilarity(lda[[entry2bow(entry) for entry in entries]])
    sims = index[lda[bow]]
    return sorted(zip([e['index'] for e in entries], sims), key = lambda e: e[1], reverse = True)

def recommend(project, N=5):
    sims = compute_sims(project.bow, project.read_doc)
    docs = [db.find_one({'index': doc[0]}) for doc in sims]
    return docs
