# Personal knowledge base


## Problem

In the age of information the body of knowledge is in a state of
neverending expansion. It is hard to keep up to date with the newest
developments in large scale but even in a small restricted subset such
as the own academic discipline it is a tremendous work. However, with
the developments in artificial intelligence and data science it
appears to be feasible to ease the workload on the human being by
discovering the semantic structure of the documents the user is
interested in and find similar documents which have relevance to the
already discovered ones. Furthermore with such an approach management
of literature is simplified: All read documents are available,
searchable and ready to export to an output format of the users
choice.

With this project we would like to implement a basic proof of concept
using several techniques to achieve the above.

## Theoretical Approach

### Semantic analysis

In order to expose the semantic structure of the documents we are
dealing with we chose the LDA. Without going into to many details, it
is sufficient to know that it exposes the semantic structure of the
documents.  On a high level this is a rather simple process. First,
vocabularies are probabilities of certain words over an alphabet of words. Each vocabulary represents a topic and we would like to represent a document as a mixture of topics.
For instance when reading papers about computer science the term
``database`` will occur with a bigger probability than when reading
papers about social sciences. However, note that this may be
ambigious, since sometimes certain term are used with different
connations in different ways e.g. traveling as in the traveling
salesman problem and traveling as part of a voyage.
Given a pdf, we first extract the fulltext of it. Clean it up to
 some point by removing fillwords such as is and then. After the
document is translated into a bag of words(bow) representation.
In order, to assign topics to a document, it is sufficent to randomly
draw words from the bow and take a look at the result.

### User model

So given that we know what a document is about, how we can do
recommandations for the user?  Of course, we could just pick the
articles randomly but this would defy the purpose of the system.
There must be some way to connect the user interest and the topics of
the articles he read.  After considering several different approaches,
we came to the conclusion that the simple way is the best: Represent
the user as a document in the vector space of documents. However, he
is different from the other documents, since he can move in the vector
space meanwhile the other documents are stationary. Since the vector
of the documents is generated from their bag of words, we simply
represent the user as a bag of words. In order to achieve this we have
to implement a simple algebra for addition and substraction of bows.
This directly corresponds to the user liking or disliking articles and
topics.


### Suggesting the new article

The recommandation gets very simple with the above user model. Due to
the fact that documents and the user are vectors in a vector space, we
can just calculate the cosine similarity between the user and all
articles he has not read yet and select the article with the greatest similarity.

### Implementation Details

For implementation we have used a couple of different libraries and
external tools.  Most importantly, we have used the gensim library in
order to obtain a LDA model. This model was generated by gensim with
a dump of wikipedia. After we have consulted the literature, we have
decided that the right amount of topics for our purpose was
400. This may be a bad choice though, since we do not have the
experience to make the right call.  The number of topics provides the
resolution with which we can perceive the articles and assign topics
to them. However, a number to large requires too long to generate the
modell meanwhile a number to small makes us blind when we deal with
specialised terms. Solving this dilemma requires some trial and error
for which we did not have the time for.

For persistence we have used mongodb with the python driver. For
faster calculations, we have used numpy with the Anaconda Accelerate
extension.

The source of our articles was arxiv, since it makes a lot of articles
with fulltext available through an API. Parsing of the API was done by beautiful soup.

### Lessons learned

Our initial assumption that this would be complicated and take a long
time to work out was proved wrong. This was a pleasant suprise.

However, the topic decomposition of the articles is quite broad.  We
assume that the reason for this that we have used a common knowledge
corpus and not one with specialised knowledge. This may be remedied by
using an online learning LDA with already given articles as basis for
the corpus. This approach may not be practical though since it
requires the user to have the articles at hand. Therefore a good
initial corpus should be constructed by selecting seminal papers manually.



## Conclusion

All in all the system works better than we have initial expected with
certain details still demanding attention. However, we could make
recommandations which appeared to make sense.