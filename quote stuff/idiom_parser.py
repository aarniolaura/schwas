# TASK 1: TEXT MINING FROM THE WEB

# 1. Download content from a web page
# 2. Extract plain text from the HTML document
# 3. Extract only certain parts of the text

import requests
from bs4 import BeautifulSoup

# 1. Download the content
url = "https://www.phrases.org.uk/meanings/phrases-and-sayings-list.html"
html = requests.get(url)



# 2. Use beautiful soup to extract the text in the html file
soup = BeautifulSoup(html.content, 'html.parser')
idioms = []
for element in soup.find_all(class_='phrase-list'):
    idioms.append(str(element.get_text()))

for elem in idioms:
    elem = elem.split('\n')

# WEEK 3 TASK PART 2: Refined search


import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from textblob import TextBlob


# Split into lists of strings (each article is a string)
documents = idioms

# Create a dictionary (article name: article contents) if needed

# CREATING THE MATRIX

def textblob_tokenizer(str_input):
    blob = TextBlob(str_input.lower())
    tokens = blob.words
    words = [token.stem() for token in tokens]
    return words

# creates biword term vectors
biword_v = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2", ngram_range=(1, 1), tokenizer=textblob_tokenizer)
biword_matrix = biword_v.fit_transform(documents).T.tocsr()

# creates normal term vectors
gv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2", tokenizer=textblob_tokenizer)
g_matrix = gv.fit_transform(documents).T.tocsr()

def translate(query_string, source_lang):
    query_blob = query_string.translate(from_lang=source_lang, to='en')
    return str(query_blob)

def search_documents(query_string):
    source_lang = TextBlob(query_string).detect_language()
    if source_lang != 'en':
       query_string =  translate(TextBlob(query_string), source_lang)
    else:
        pass

    query_tokens = query_string.split()
    if len(query_tokens) == 2:
        vectorizer = biword_v
        matrix = biword_matrix
    else:
        vectorizer = gv
        matrix = g_matrix

    # Vectorize query string
    query_vec = vectorizer.transform([query_string]).tocsc()

    # Cosine similarity
    hits = np.dot(query_vec, matrix)

    # Rank hits
    ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]),
                                       reverse=True)
    # Output result
    print("Your query '{:s}' matches the following idioms:\n".format(query_string))
    count = 0
    for i, (score, doc_idx) in enumerate(ranked_scores_and_doc_ids):
        print("Idiom #{:d} (score: {:.4f}): {:s}".format(i, score, documents[doc_idx]))
        #if source_lang != 'en':
        #    idiom_blob = TextBlob(documents[doc_idx].translate(from_lang='en', to=source_lang))
        #    print("In your original language: {s}".format(str(idiom_blob)))
        print()
        count += 1
        if count > 2:
            return print("Showing the best three idiom matches", len(ranked_scores_and_doc_ids), "articles.\n")

# MAKING QUERIES
print("Welcome to the search engine!")
print("Data:", len(documents), "Idioms")
print("Number of terms in vocabulary:", len(gv.get_feature_names()))
print("Number of bi-words in vocabulary:", len(biword_v.get_feature_names()))
print()
# Ask the user to type a query
query = str(input("Enter a query: "))


while query != "":
    try:
        search_documents(query)
        query = str(input("Enter a new query (enter blank if you want to quit): "))
    except KeyError:
        query = str(input("Your search failed. Try again: "))
    except IndexError:
        query = str(input("Word(s) not found. Try again: "))

else:
    print("Goodbye!")
