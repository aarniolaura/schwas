#!/usr/bin/env python
# coding: utf-8

# ### Tf-idf demo on the books in the Gutenberg corpus in NLTK
#
# Let's compute tf-idf scores for words occurring in the different books in the NLTK version of the Gutenberg corpus.
#
# First we take a look at what books there are and how many words each of them contains:

# In[1]:


import nltk

booknames = nltk.corpus.gutenberg.fileids()

for name in booknames:
    print("{:s} contains {:d} word tokens.".format(name, len(nltk.corpus.gutenberg.words(name))))

# Let's have a look how many word tokens and types there are in all books combined.

# In[2]:


ntot_tokens = sum(len(nltk.corpus.gutenberg.words(name)) for name in booknames)
print("Total number of word tokens:", ntot_tokens)

# Can we handle all word types or do we need to drop some?

# In[3]:


ntot_types = len(set(w.lower() for bookname in booknames for w in nltk.corpus.gutenberg.words(bookname)))
print("Total number of word types:", ntot_types)

# This number of word types is not too high, so we can keep them all in our vocabulary.
#
# Let's look at which words are the most common in the corpus as a whole (**term frequencies** in the entire corpus).

# In[4]:


fdist = nltk.FreqDist(w.lower() for bookname in booknames for w in nltk.corpus.gutenberg.words(bookname))

print("The 100 most common word types in the Gutenberg corpus are:")
for w, f in fdist.most_common(100):
    print(w, f)

# What about **document frequencies**? For every word type, we count the number of documents (= books) it occurs in:

# In[25]:


from collections import defaultdict

df = defaultdict(int)

for name in booknames:
    for word in set(w.lower() for w in nltk.corpus.gutenberg.words(name)):
        df[word] += 1

# Next we sort the words by their document frequencies:

# In[26]:


df_sorted_words = sorted(df.keys(), key=lambda w: df[w], reverse=True)

# Let's take a look at some words that occur in _all_ the books:

# In[27]:


print("Examples of words that occur in all books:")
for w in df_sorted_words[0:10]:
    print(w, df[w])

# And some words that only occur in one single book:

# In[28]:


print("Examples of words that occur in only one book:")
for w in df_sorted_words[-10:]:
    print(w, df[w])

# As well as some words that occur in a few books:

# In[29]:


print("Examples of words that occur in some, but not all books:")
for w in df_sorted_words[5000:5010]:
    print(w, df[w])

# From the document frequencies we compute the corresponding **inverse document frequency** (idf) values.

# In[30]:


import math

ndocs = len(booknames)
idf = defaultdict(float)

for w in df.keys():
    idf[w] = math.log(ndocs / df[w])

# What do the idf values look like for words that occur in all documents?

# In[11]:


print("Show the IDF values of some words that occur in all books:")
for w in df_sorted_words[0:10]:
    print(w, idf[w])

# Or words that occur in one document only?

# In[12]:


print("Show the IDF values of some words that occur in only one book:")
for w in df_sorted_words[-10:]:
    print(w, idf[w])

# Or somewhere in between?

# In[13]:


print("Show the IDF values of some words that occur in some, but not all books:")
for w in df_sorted_words[5000:5010]:
    print(w, idf[w])

# For the calculation of the tf-idf scores we also need the *document-specific term frequencies*. Let's look at the 20 most frequent words in each of the documents. Do we see any big differences between the documents?

# In[14]:


for name in booknames:
    fdist = nltk.FreqDist(w.lower() for w in nltk.corpus.gutenberg.words(name))
    print("Most frequent words in {:s}:".format(name))
    for w, f in fdist.most_common(20):
        print(w, f)
    print()

# How does it look, when we compute **tf-idf** scores for the words in the documents and compare? We display the 20 top scoring words for each document.

# In[15]:


# For each document (book) ...
for bookname in booknames:
    tf = {}
    tfidf = {}
    fdist = nltk.FreqDist(w.lower() for w in nltk.corpus.gutenberg.words(bookname))

    # For each word in the document ...
    for w, f in fdist.most_common():
        # Compute the term frequency:
        tf[w] = 1 + math.log10(f)
        # ... as well as the tf-idf score:
        tfidf[w] = tf[w] * idf[w]

    # Sort the words by tf-idf
    tfidf_sorted_words = sorted(tfidf.keys(), key=lambda w: tfidf[w], reverse=True)

    # Show the highest scoring words in this document
    print("Highest tf-idf scoring words in {:s}:".format(bookname))
    for w in tfidf_sorted_words[0:20]:
        print("{:s}: {:.3f} (tf: {:.3f}, idf: {:.3f})".format(w, tfidf[w], tf[w], idf[w]))
    print()

# Let's rerun the the tf-idf calculations, but instead of showing the highest scoring words in each document, we will show the scores of some (arbitrarily) selected words:

# In[16]:


selected_words = ["god", "jesus", "rich", "handsome", "romantic", "secret",
                  "honey", "bear", "ahab", "white", "whale", "alice",
                  "wonderland", "king", "queen", "lazy", "sin", "paradise"]

for bookname in booknames:
    tf = {}
    tfidf = {}
    fdist = nltk.FreqDist(w.lower() for w in nltk.corpus.gutenberg.words(bookname))
    for w, f in fdist.most_common():
        tf[w] = 1 + math.log10(f)
        tfidf[w] = tf[w] * idf[w]

    print("Tf-idf scores of some selected words in {:s}:".format(bookname))
    for w in selected_words:
        if w in tfidf.keys():
            print("{:s}: {:.3f} (tf: {:.3f}, idf: {:.3f})".format(w, tfidf[w], tf[w], idf[w]))
        else:
            print("{:s}: missing".format(w))
    print()

# Does this make sense?
#
# How come the tf-idf score is zero for some words? What might be the consequences of this? Are there any weaknesses in this approach?
