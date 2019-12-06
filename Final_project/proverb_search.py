from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from textblob import TextBlob
import spacy
from spacy import displacy
from pathlib import Path
import re


with open('proverbs.txt', 'r') as f:
    proverb_document = f.read().splitlines()

with open('meanings.txt', 'r') as f:
    meaning_document = f.read().splitlines()
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

def get_matrix(doc):
    g_matrix = gv.fit_transform(doc).T.tocsr()

    return g_matrix

def translate_query(query_string, source_lang):
    query_blob = query_string.translate(from_lang=source_lang, to='en')
    return str(query_blob)

def search_documents(query_string, doc):
    source_lang = TextBlob(query_string).detect_language()
    if source_lang != 'en':
        query_string = translate_query(TextBlob(query_string), source_lang)
    else:
        pass

    vectorizer = gv
    matrix = get_matrix(doc)

    # Vectorize query string
    query_vec = vectorizer.transform([query_string]).tocsc()

    # Cosine similarity
    hits = np.dot(query_vec, matrix)


    # Rank hits
    ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]),
                                       reverse=True)

    return ranked_scores_and_doc_ids


#Initialize Flask instance
app = Flask(__name__)

#Function search() is associated with the address base URL + "/search"
@app.route('/search')
def search():
    #nlp = spacy.load("en")

    nlp = spacy.load("en_core_web_sm")
    #Get query from URL variable
    proverb_query = request.args.get('proverb')
    meaning_query = request.args.get('meaning')
    #Initialize list of matches
    proverb_matches = []
    meaning_matches = []
    proverb_results = []
    meaning_results = []
    if proverb_query:
        matches = search_documents(proverb_query, proverb_document)
        for elem in matches:
            proverb_matches.append(proverb_document[elem[1]])
            doc = nlp(proverb_document[elem[1]])
            svg = displacy.render(doc, style="dep", jupyter=False)
            file_name = '-'.join([w.text for w in doc if not w.is_punct]) + ".svg"
            print(file_name)
            output_path = Path("static/" + file_name)
            output_path.open("w", encoding="utf-8").write(svg)
            proverb_results.append({'name': doc, 'pltpath': output_path})
    elif meaning_query:
        matches2 = search_documents(meaning_query, meaning_document)
        for elem in matches2:
            meaning_matches.append(meaning_document[elem[1]])
            doc = nlp(meaning_document[elem[1]])
            meaning_results.append({'name2': doc})

    #Render index.html with matches variable
    return render_template('index.html', matches=proverb_results[:5], matches2=meaning_results[:5])

