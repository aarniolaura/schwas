# WEEK 3 TASK PART 2: Refined search

import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from textblob import TextBlob

# DATA
wikipedia = ""
file_name = "enwiki-20181001-corpus.1000-articles.txt"
try:
    file = open(file_name, "r", encoding='utf-8')
    wikipedia = file.read()
    file.close()
except OSError:
    print("Error reading the file", file_name)

# Split into lists of strings (each article is a string)
documents = wikipedia.split('</article>')

# Create a dictionary (article name: article contents) if needed
dict = {}
for d in documents:
    alku = d.find("<article name=")
    loppu = d.find('">')
    name = d[16:loppu]
    text = d[loppu + 2:]
    dict[name] = text

def read_article(title):
    if title in dict.keys():
        print("\n*****************************************")
        print("\n" + title)
        print(dict.get(title))
        print("*****************************************\n")
    else:
        print("No such article found.")

# CREATING THE MATRIX

def textblob_tokenizer(str_input):
    blob = TextBlob(str_input.lower())
    tokens = blob.words
    words = [token.stem() for token in tokens]
    return words

# creates biword term vectors
biword_v = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2", ngram_range=(2, 2), tokenizer=textblob_tokenizer)
biword_matrix = biword_v.fit_transform(documents).T.tocsr()

# creates normal term vectors
gv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2", tokenizer=textblob_tokenizer)
g_matrix = gv.fit_transform(documents).T.tocsr()

def translate(query_string, source_lang):
    query_string = TextBlob(query)
    source_lang = query_string.detect_language()
    print(source_lang)
    query_blob = query_string.translate(from_lang=source_lang, to='en')
    print(query_blob)
    return str(query_blob)

def search_documents(query_string):

    query_blob = TextBlob(query_string)
    source_lang = query_blob.detect_language()
    if source_lang != 'en':
       query_string =  translate(query_blob, source_lang)
       print("Your search was made in the", source_lang, "language. Showing results in English")
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
    print("Your query '{:s}' matches the following documents:".format(query_string))
    count = 0
    for i, (score, doc_idx) in enumerate(ranked_scores_and_doc_ids):
        print("Matching article #{:d} (score: {:.4f}): {:s}".format(i, score, documents[doc_idx][15:200]) + "...")
        print()
        count += 1
        if count > 4:
            return print("Showing the first five of", len(ranked_scores_and_doc_ids), "articles.\n")

# MAKING QUERIES
print("Welcome to the search engine!")
print("Data: 1000 Wikipedia articles")
print("Number of terms in vocabulary:", len(gv.get_feature_names()))
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