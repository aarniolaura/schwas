#!/usr/bin/env python
# coding: utf-8

# # Relevance-ranked search
#
# Let's return to the indexing of toy data, as we did in the tutorial on Boolean search. This new tutorial has also been inspired by course material by Filip Ginter in Turku.
#
# Our documents now look slightly different:

# In[33]:


documents = ["This is a silly silly silly example",
             "A better example",
             "Nothing to see here nor here nor here",
             "This is a great example and a long example too"]

# We can index them as we did before:

# In[34]:


from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

cv = CountVectorizer(lowercase=True, binary=True)
binary_dense_matrix = cv.fit_transform(documents).T.todense()

print("Term-document matrix:\n")
print(binary_dense_matrix)

# Next, we'll remove the `binary=True` optional argument from the `CountVectorizer` constructor. The default value is `binary=False`. What change can we observe?

# In[35]:


cv = CountVectorizer(lowercase=True)
dense_matrix = cv.fit_transform(documents).T.todense()

print("Term-document matrix:\n")
print(dense_matrix)

# Let's recall what term each row in the matrix corresponds to:

# In[65]:


for (row, term) in enumerate(cv.get_feature_names()):
    print("Row", row, "is the vector for term:", term)

# Now, if we run a query on the term "example", we get:

# In[37]:


t2i = cv.vocabulary_  # shorter notation: t2i = term-to-index
print("Query: example")
print(dense_matrix[t2i["example"]])

# Instead of seeing *whether* a term occurs in a document, we now see *how many times* the term occurs in each document:

# In[38]:


hits_list = np.array(dense_matrix[t2i["example"]])[0]

for i, nhits in enumerate(hits_list):
    print("Example occurs", nhits, "time(s) in document:", documents[i])

# When the number and sizes of the documents grow, we may think that the more times a search term occurs in a document, the more relevant the document is. So, if we search for "example" in our toy document collection, the fourth document is most relevant (2 hits), the first and second documents come next (1 hit each) and the third document is irrelevant (0 hits).
#
# If we have multiple search terms, we might think that the more times the search terms occur in total in the document, the more relevant the document is.
#
# Note that the bit-wise logical operators `AND (&)` and `OR (|)` will not work properly anymore when our matrix contains word counts. The same applies to `NOT (1 - x)`.
#
# Let's search for the most relevant document for the query *better example*:

# In[39]:


print("Query: better example")
print("Hits of better:        ", dense_matrix[t2i["better"]])
print("Hits of example:       ", dense_matrix[t2i["example"]])
print("Hits of better example:", dense_matrix[t2i["better"]] + dense_matrix[t2i["example"]])

# We just added the hits together. This means that we did not search for the phrase "better example", nor did we search for "better" AND "example". What we did search for was some kind of "better" OR "example", in which the sum of the number of occurrences of "better" and "example" in a document determines the relevance of the document.
#
# This means that the second document, which contains one occurrence each of "better" and "example" is as good a hit as the fourth document, which contains two occurrences of "example" and no occurrence of "better".
#
# Let's execute another query:

# In[40]:


print("Query: silly example")
print("Hits of silly:        ", dense_matrix[t2i["silly"]])
print("Hits of example:      ", dense_matrix[t2i["example"]])
print("Hits of silly example:", dense_matrix[t2i["silly"]] + dense_matrix[t2i["example"]])

# ... and also rank (sort) the results by relevance. We leave out the document without a single hit:

# In[41]:


# We need the np.array(...)[0] code here to convert the matrix to an ordinary list:
hits_list = np.array(dense_matrix[t2i["silly"]] + dense_matrix[t2i["example"]])[0]
print("Hits:", hits_list)

nhits_and_doc_ids = [(nhits, i) for i, nhits in enumerate(hits_list) if nhits > 0]
print("List of tuples (nhits, doc_idx) where nhits > 0:", nhits_and_doc_ids)

ranked_nhits_and_doc_ids = sorted(nhits_and_doc_ids, reverse=True)
print("Ranked (nhits, doc_idx) tuples:", ranked_nhits_and_doc_ids)

print("\nMatched the following documents, ranked highest relevance first:")
for nhits, i in ranked_nhits_and_doc_ids:
    print("Score of 'silly example' is", nhits, "in document:", documents[i])

# ## Tf-idf
#
# As we may guess, pure word counts are not a good indicator of relevance. Frequently occurring words are not usually very interesting from the point of view of information content.
#
# One approach to weight terms (words) by their relevance is to use *term frequency / inverse document frequency (tf-idf)* weighting. There is another [tutorial on tf-idf](tf-idf-gutenberg.ipynb) that illustrates how this weighting works.
#
# As a matter of fact, the scikit-learn library makes it easy for us to compute the tf-idf scores of terms in a document collection. Instead of the class `CountVectorizer` we can use `TfidfVectorizer`:

# In[42]:


from sklearn.feature_extraction.text import TfidfVectorizer

# The TfidfVectorizer can be used with many different parameter values. One option is to count ordinary term frequencies. In this setup the resulting matrix should produce the same values as the one produced by the CountVectorizer:

# In[66]:


# Parameters with which TfidfVectorizer does same thing as CountVectorizer
tfv1 = TfidfVectorizer(lowercase=True, sublinear_tf=False, use_idf=False, norm=None)
tf_matrix1 = tfv1.fit_transform(documents).T.todense()

print("TfidfVectorizer:")
print(tf_matrix1)

print("\nCountVectorizer:")
print(dense_matrix)

# The values are the same, except that the TfidfVectorizer produces floating-point values, whereas the CountVectorizer produces integer values.
#
# Some useful parameters for the TfidfVectorizer are `sublinear_tf`, `use_idf` and `norm`.
#
# `sublinear_tf=True` uses logarithmic word frequencies instead of linear ones. That is, if a term occurs 20 times, it is not 20 times more important than a term that occurs once:

# In[67]:


tfv2 = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=False, norm=None)
tf_matrix2 = tfv2.fit_transform(documents).T.todense()

print("TfidfVectorizer (logarithmic term frequencies):")
print(tf_matrix2)

# `use_idf=True` factors in the inverse document frequencies. The more documents a term occurs in, the less relevant the term is, in general:

# In[69]:


tfv3 = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm=None)
tf_matrix3 = tfv3.fit_transform(documents).T.todense()

print("TfidfVectorizer (logarithmic term frequencies and inverse document frequencies):")
print(tf_matrix3)

# If additionally, we use the L2 norm `norm="l2"` we normalize all document vectors (columns) to have a (Euclidian) length of one:

# In[70]:


tfv4 = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
tf_matrix4 = tfv4.fit_transform(documents).T.todense()

print("TfidfVectorizer (logarithmic term frequencies and inverse document frequencies, normalized document vectors):")
print(tf_matrix4)

# We can search the index in the same way as above, even if we use tf-idf weighting:

# In[71]:


print("Query: silly example")
print("Hits of silly:        ", tf_matrix4[t2i["silly"]])
print("Hits of example:      ", tf_matrix4[t2i["example"]])
print("Hits of silly example:", tf_matrix4[t2i["silly"]] + tf_matrix4[t2i["example"]])

# ... and we can rank the documents using the tf-idf scores:

# In[72]:


hits_list4 = np.array(tf_matrix4[t2i["silly"]] + tf_matrix4[t2i["example"]])[0]
print("Hits:", hits_list4)

hits_and_doc_ids = [(hits, i) for i, hits in enumerate(hits_list4) if hits > 0]
print("List of tuples (hits, doc_idx) where hits > 0:", hits_and_doc_ids)

ranked_hits_and_doc_ids = sorted(hits_and_doc_ids, reverse=True)
print("Ranked (hits, doc_idx) tuples:", ranked_hits_and_doc_ids)

print("\nMatched the following documents, ranked highest relevance first:")
for hits, i in ranked_hits_and_doc_ids:
    print("Score of 'silly example' is {:.4f} in document: {:s}".format(hits, documents[i]))

# It makes sense that the document "This is a silly silly silly example" comes up on the top, but why does "A better example" now rank higher than "This is a great example and a long example too"? The former one contains only one occurrence of "example" whereas the latter one contains two. Can you figure out the reason?
#
# ### Cosine similarity
#
# When we searched the index above, we scored the documents by summing together the tf-idf values of all the terms in the search query. A more sophisticated way is to transform the query itself into a document vector, in which we score each search term using tf-idf. We then compare the query vector to each document vector in the index. The more similar the query vector is to a document vector, the more relevant that document is for our search.
#
# Let us first create a vector of our query:

# In[49]:


query_vec4 = tfv4.transform(["silly example"]).todense()
print(query_vec4)

# This is actually a matrix with one row (document-term matrix). Since we have looked at term-document matrices above, let's transpose, to understand better:

# In[50]:


print(query_vec4.T)

# We can see that only two terms have non-zero values, and they are (not surprisingly) "example" and "silly":

# In[73]:


print("Tf-idf weight of 'example' on row", t2i["example"], "is:", query_vec4.T[t2i["example"]])
print("Tf-idf weight of 'silly' on row", t2i["silly"], "is: ", query_vec4.T[t2i["silly"]])

# Make sure that you understand why the score of "silly" is higher than that of "example".
#
# To compare two vectors we use *cosine similarity*, which measures the cosine of the angle between the document vectors. If all vectors are guaranteed to be of length 1, which they are when we use the L2 norm, the cosine similarity reduces to the dot product:

# In[74]:


for i in range(0, 4):
    # Go through each column (document vector) in the index
    doc_vector = tf_matrix4[:, i]

    # Compute the dot product between the query vector and the document vector
    # (Some extra stuff here to extract the number from the matrix data structure)
    score = np.array(np.dot(query_vec4, doc_vector))[0][0]

    print("The score of 'silly example' is {:.4f} in document: {:s}".format(score, documents[i]))

# Because of the beauty with matrix and vector algebra, we don't actually need a loop, but we can do all calculations in one single dot product:

# In[53]:


scores = np.dot(query_vec4, tf_matrix4)
print("The documents have the following cosine similarities to the query:", scores)

# If we want to rank the matching documents, we can do it like this:

# In[54]:


ranked_scores_and_doc_ids = sorted([(score, i) for i, score in enumerate(np.array(scores)[0]) if score > 0],
                                   reverse=True)

for score, i in ranked_scores_and_doc_ids:
    print("The score of 'silly example' is {:.4f} in document: {:s}".format(score, documents[i]))

# ## Scaling up to larger document collections with sparse matrices
#
# As we saw in the tutorial on Boolean search, any real-size data requires us to use sparse matrices. Let us go though how to use sparse matrices with tf-idf weighting.
#
# First we index the data:

# In[55]:


tfv5 = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
sparse_matrix = tfv5.fit_transform(documents).T.tocsr()  # CSR: compressed sparse row format => order by terms

print("Sparse term-document matrix with tf-idf weights:")
print(sparse_matrix)

# Then we convert the query string to a sparse vector:

# In[56]:


# The query vector is a horizontal vector, so in order to sort by terms, we need to use CSC
query_vec5 = tfv5.transform(["silly example"]).tocsc()  # CSC: compressed sparse column format

print("Sparse one-row query matrix (horizontal vector):")
print(query_vec5)

# Next we compute the cosine similarity (dot product). Since we are dealing with sparse matrices, any zero values are automatically left out:

# In[57]:


hits = np.dot(query_vec5, sparse_matrix)

print("Matching documents and their scores:")
print(hits)

# We can access the document indexes like this:

# In[58]:


print("The matching documents are:", hits.nonzero()[1])

# We can access the tf-idf scores like this:

# In[59]:


print("The scores of the documents are:", np.array(hits[hits.nonzero()])[0])

# We can rank the documents by scores. It may be hard to see that this works, since the documents happen to be in the right order already.

# In[60]:


ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)

for score, i in ranked_scores_and_doc_ids:
    print("The score of 'silly example' is {:.4f} in document: {:s}".format(score, documents[i]))

# ### Gutenberg corpus
#
# Let's finally index the Gutenberg corpus in NLTK, to get a feel for some real data.
#
# We start by loading the data:

# In[61]:


import nltk

booknames = nltk.corpus.gutenberg.fileids()

bookdata = list(nltk.corpus.gutenberg.raw(name) for name in booknames)

print("There are", len(bookdata), "books in the collection:", booknames)

# Then we index it using the TfidfVectorizer:

# In[62]:


gv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
g_matrix = gv.fit_transform(bookdata).T.tocsr()

print("Number of terms in vocabulary:", len(gv.get_feature_names()))


# Let's create a function for searching this document collection:

# In[63]:


def search_gutenberg(query_string):
    # Vectorize query string
    query_vec = gv.transform([query_string]).tocsc()

    # Cosine similarity
    hits = np.dot(query_vec, g_matrix)

    # Rank hits
    ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]),
                                       reverse=True)

    # Output result
    print("Your query '{:s}' matches the following documents:".format(query_string))
    for i, (score, doc_idx) in enumerate(ranked_scores_and_doc_ids):
        print("Doc #{:d} (score: {:.4f}): {:s}".format(i, score, booknames[doc_idx]))
    print()


# ... and run some searches:

# In[64]:


search_gutenberg("alice")
search_gutenberg("alice entertained harriet")
search_gutenberg("whale hunter")
search_gutenberg("oh thy lord cometh")
search_gutenberg("which book should i read")

# This is all for now.
#
# There are many different ways term-document scores can be computed. In some approaches the query vector is not calculated in the same way as the document vectors. For instance, the idf factor may be used for query vectors, but left out from the document vectors. If you are interested, you can compare some different approaches on your data.
