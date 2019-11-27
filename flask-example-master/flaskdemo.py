from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from textblob import TextBlob
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib as mlp
import re
import nltk
import os


with open('proverbs.txt', 'r') as f:
    documents = f.readlines()
# Split into lists of strings (each article is a string)

# Create a dictionary (article name: article contents) if needed

# CREATING THE MATRIX

def textblob_tokenizer(str_input):
    blob = TextBlob(str_input.lower())
    tokens = blob.words
    words = [token.stem() for token in tokens]
    return words

# creates normal term vectors
gv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2", tokenizer=textblob_tokenizer)
g_matrix = gv.fit_transform(documents).T.tocsr()

def translate_query(query_string, source_lang):
    query_blob = query_string.translate(from_lang=source_lang, to='en')
    return str(query_blob)

def search_documents(query_string):
    source_lang = TextBlob(query_string).detect_language()
    if source_lang != 'en':
       query_string = translate_query(TextBlob(query_string), source_lang)
    else:
        pass

    query_tokens = query_string.split()
    vectorizer = gv
    matrix = g_matrix

    # Vectorize query string
    query_vec = vectorizer.transform([query_string]).tocsc()

    # Cosine similarity
    hits = np.dot(query_vec, matrix)

    # Rank hits
    ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]),
                                       reverse=True)

    return ranked_scores_and_doc_ids

def generate_query_plot(query,matches):
    # create a figure
    fig = plt.figure()
    plt.title("Word distribution per document \n query: "+query)
    # some values we will use to generate a plot
    dist_dict={}
    for match in matches:
        dist_dict[match['name']] = len(match['content'])
    # from a dictionary we can create a plot in two steps:
    #  1) plotting the bar chart
    #  2) setting the appropriate ticks in the x axis
    plt.bar(range(len(dist_dict)), list(dist_dict.values()), align='center')
    plt.xticks(range(len(dist_dict)), list(dist_dict.keys()),rotation=30) # labels are rotated
    # make room for the labels
    plt.gcf().subplots_adjust(bottom=0.30) # if you comment this line, your labels in the x-axis will be cutted
    plt.savefig('static/query_plot.png')



#Initialize Flask instance
app = Flask(__name__)

#Function search() is associated with the address base URL + "/search"
@app.route('/search')
def search():
    matches = []
    #Get query from URL variable
    query = request.args.get('query')
    #Initialize list of matches
    matches2 = []
    scores = []
    if query:
        matches = search_documents(query)
        for elem in matches:
            matches2.append(documents[elem[1]])
            scores.append(documents[elem[0]])




    #Render index.html with matches variable
    return render_template('index.html', matches=matches2[:5])

