#!/usr/bin/env python
# coding: utf-8

# # Boolean search in Python on toy data
# 
# This code has been adapted and inspired from the notebooks by Filip Ginter for the course *Information Retrieval* given in the spring of 2017 at the University of Turku.
# 
# Let's first create some toy data, that is, four sentences that we consider to be our "documents":

# In[1]:

import nltk, re, pprint
from urllib.request import urlopen

# ## Term-document matrix
# 
# We need to import some functionality from sklearn (also called scikit-learn), which is a free software machine learning library for Python.

# In[3]:


import nltk
from sklearn.feature_extraction.text import CountVectorizer


# We use the CountVectorizer class to create a *term-document* matrix of our data:

# In[3]:


cv = CountVectorizer(lowercase=True, binary=True)
sparse_matrix = cv.fit_transform(documents)

print("Term-document matrix: (?)\n")
print(sparse_matrix)


# Oops, this does not look like a matrix. It is because the matrix is stored in a _sparse_ format to save memory. How do we read this? For instance, the two first rows tell us that in the coordinate (0, 2) of the matrix there is a 1, and in the coordinate (0, 9) there is also a 1.
# 
# All positions in the matrix not explicitly mentioned contain a zero, so we save memory by not storing all zeros. The matrix is assumed to be sparse, that is, most of the elements are zero.
# 
# Anyway, let's print a _dense_ version of this matrix:

# In[4]:


dense_matrix = sparse_matrix.todense()

print("Term-document matrix: (?)\n")
print(dense_matrix)


# This looks better, but... There are four documents, so the rows must now be the documents and the columns the terms (= words). However, we want to have a *term-document* matrix, not a *document-term* matrix.
# 
# Let's *transpose* the matrix, so that the rows and columns change places:

# In[5]:


td_matrix = dense_matrix.T   # .T transposes the matrix

print("Term-document matrix:\n")
print(td_matrix)


# From this matrix we can read, for instance, that the term represented by the first row `[0 0 0 1]` occurs only in the fourth document (_"This is a great and long example"_). It further tells us, for example, that the term on the third row `[1 1 0 1]` occurs in all but the third document.
# 
# So, how can we know which terms the different rows represent?
# 
# Here goes the ordered list of terms:

# In[6]:


print("\nIDX -> terms mapping:\n")
print(cv.get_feature_names())


# So, the first row represents the word "and" and the third row the word "example".
# 
# Let's double-check that:

# In[7]:


terms = cv.get_feature_names()

print("First term (with row index 0):", terms[0])
print("Third term (with row index 2):", terms[2])


# It is also possible to map the other way around, from term to index:

# In[8]:


print("\nterm -> IDX mapping:\n")
print(cv.vocabulary_) # note the _ at the end


# `.vocabulary_` (with a trailing underscore) is a Python dictionary:

# In[9]:


print("Row index of 'example':", cv.vocabulary_["example"])
print("Row index of 'silly':", cv.vocabulary_["silly"])


# ## First simple searches
# 
# Let's "search" for the term "example" in our "document collection":

# In[10]:


t2i = cv.vocabulary_  # shorter notation: t2i = term-to-index
print("Query: example")
print(td_matrix[t2i["example"]])


# The term "example" occurs in all but the third document, which we already knew...
# 
# What about searching for documents containg "example" AND "great"?

# In[11]:


print("Query: example AND great")
print("example occurs in:                            ", td_matrix[t2i["example"]])
print("great occurs in:                              ", td_matrix[t2i["great"]])
print("Both occur in the intersection (AND operator):", td_matrix[t2i["example"]] & td_matrix[t2i["great"]])


# Let's search for "is" OR "see":

# In[12]:


print("Query: is OR see")
print("is occurs in:                            ", td_matrix[t2i["is"]])
print("see occurs in:                           ", td_matrix[t2i["see"]])
print("Either occurs in the union (OR operator):", td_matrix[t2i["is"]] | td_matrix[t2i["see"]])


# Let's find all document that do not contain "this":

# In[13]:


print("Query: NOT this")
print("this occurs in:                     ", td_matrix[t2i["this"]])
print("this does not occur in (complement):", 1 - td_matrix[t2i["this"]]) # 1 - x changes 1 to 0 and 0 to 1


# Finally, let's create a more complex query:

# In[14]:


print("Query: ( example AND NOT this ) OR nothing")
print("example occurs in:                  ", td_matrix[t2i["example"]])
print("this does not occur in:             ", 1 - td_matrix[t2i["this"]])
print("example AND NOT this:               ", td_matrix[t2i["example"]] & (1 - td_matrix[t2i["this"]]))
print("nothing occurs in:                  ", td_matrix[t2i["nothing"]])
print("( example AND NOT this ) OR nothing:", 
      (td_matrix[t2i["example"]] & (1 - td_matrix[t2i["this"]])) | td_matrix[t2i["nothing"]])


# ## Simple query parser
# 
# There is a lot of writing that goes into these queries, so let's create a simple query parser, which does part of the job for us. Now we can type the queries in a much simpler way:

# In[15]:


# Operators and/AND, or/OR, not/NOT become &, |, 1 -
# Parentheses are left untouched
# Everything else interpreted as a term and fed through td_matrix[t2i["..."]]

d = {"and": "&", "AND": "&",
     "or": "|", "OR": "|",
     "not": "1 -", "NOT": "1 -",
     "(": "(", ")": ")"}          # operator replacements

def rewrite_token(t):
    return d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t)) # Can you figure out what happens here?

def rewrite_query(query): # rewrite every token in the query
    return " ".join(rewrite_token(t) for t in query.split())

def test_query(query):
    print("Query: '" + query + "'")
    print("Rewritten:", rewrite_query(query))
    print("Matching:", eval(rewrite_query(query))) # Eval runs the string as a Python command
    print()

test_query("example AND NOT nothing")
test_query("NOT example OR great")
test_query("( NOT example OR great ) AND nothing") # AND, OR, NOT can be written either in ALLCAPS
test_query("( not example or great ) and nothing") # ... or all small letters
test_query("not example and not nothing")


# ## Scaling up to larger document collections
# 
# Our toy document collection is ridiculously small, both in number of documents (4) and in the length of the documents (max 7 words per document). We will next see how we can extend our code to handle more real-sized document collections.
# 
# In order to handle large amounts of data, we need to use the sparse matrix format, in which we only record the non-zero elements. Now, there are two alternatives of doing this: Compressed Sparse Row (CSR) or Compressed Sparse Column (CSC) format. That is, either the matrix "knows" for every row which columns are non-zero, or the matrix "knows" for every column which rows are non-zero.
# 
# Our sparse matrix is CSR, because we can see that the information is ordered by the first (row) coordinate:

# In[16]:


print(sparse_matrix)


# We can convert the sparse matrix to CSC format, such that the information is ordered by the second (column) coordinate instead:

# In[17]:


print(sparse_matrix.tocsc())


# As you might remember from above, this is a *document-term* matrix, whereas we want a *term-document* matrix, so let's transpose:

# In[18]:


print(sparse_matrix.T)


# This matrix is CSC, but we want it to be CSR, so that it is ordered by terms rather than documents for faster lookup. (The search engine primarily tries to find which documents a given term occurs in, not which terms occur in a given document.)
# 
# As a matter of fact, the data structure we have now is a so-called *inverted index*:

# In[19]:


sparse_td_matrix = sparse_matrix.T.tocsr()
print(sparse_td_matrix)


# Unfortunately our Boolean logic does not work on sparse matrices. Every row that we retrieve from the term-document matrix must be made dense before we apply our operations. This is not a big deal unless we have a huge number of documents in the collection. We redefine the `rewrite_token()` function:

# In[20]:


def rewrite_token(t):
    return d.get(t, 'sparse_td_matrix[t2i["{:s}"]].todense()'.format(t)) # Make retrieved rows dense

test_query("NOT example OR great")


# ## Show retrieved documents
# 
# Showing a vector of ones and zeros is maybe not the optimal representation of the matching documents. Let's print the documents instead.

# In[21]:


hits_matrix = eval(rewrite_query("NOT example OR great"))
print("Matching documents as vector (it is actually a matrix with one single row):", hits_matrix)
print("The coordinates of the non-zero elements:", hits_matrix.nonzero())    


# The first array `[0, 0]` shows the matching "x coordinates" (rows) and the second array shows the corresponding "y coordinates" `[2, 3]`. So, we have two matching documents – at positions (0, 2) and (0, 3) of `hits_matrix`.
# 
# The first array will always just contain zeros, because there is only one row, so we only need to bother about the second array. Let's extract it and convert it from a NumPy array to an ordinary Python list:

# In[22]:


hits_list = list(hits_matrix.nonzero()[1])
print(hits_list)


# We can use the hits list to retrieve the matching documents:

# In[23]:


for doc_idx in hits_list:
    print("Matching doc:", documents[doc_idx])


# Let us enumerate the documents:

# In[24]:


for i, doc_idx in enumerate(hits_list):
    print("Matching doc #{:d}: {:s}".format(i, documents[doc_idx]))


# At this point you can write your own simple search engine, which supports Boolean queries. Next you will need to put to together your own program, in which you index a more realistic document collection and run your queries against that collection.
