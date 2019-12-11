from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from textblob import TextBlob
import spacy
from spacy import displacy
from pathlib import Path
import re

# data (from phrases.org.uk)
# with open('proverbs.txt', 'r') as f:
#     proverb_document = f.read().splitlines()
#
# with open('meanings.txt', 'r') as f:
#     meaning_document = f.read().splitlines()

# DATA from wiktionary

def data_from_file(file_name):
    text_doc = ""
    try:
        file = open(file_name, "r", encoding='utf-8')
        text_doc = file.read()
        file.close()
    except OSError:
        print("Error reading the file", file_name)
    return text_doc

text_doc = data_from_file("proverbs_en.txt")
proverbs_en = text_doc.split('\n<ENDS HERE>')

text_doc = data_from_file("meanings_en.txt")
meanings_en = text_doc.split('\n<ENDS HERE>')

text_doc = data_from_file("proverbs_es.txt")
proverbs_es = text_doc.split('\n<ENDS HERE>')

text_doc = data_from_file("meanings_es.txt")
meanings_es = text_doc.split('\n<ENDS HERE>')

text_doc = data_from_file("proverbs_fi.txt")
proverbs_fi = text_doc.split('\n<ENDS HERE>')

text_doc = data_from_file("meanings_fi.txt")
meanings_fi = text_doc.split('\n<ENDS HERE>')

# tokenizer for stemming
def textblob_tokenizer(str_input):
    blob = TextBlob(str_input.lower())
    tokens = blob.words
    words = [token.stem() for token in tokens]
    return words

def get_matrix(doc):
    g_matrix = gv.fit_transform(doc).T.tocsr()
    return g_matrix

def translate_query(query_string, source_lang, target_lang):
    query_blob = query_string.translate(from_lang=source_lang, to=target_lang)
    return str(query_blob)

def search_documents(query_string, doc, language):
    target_lang = language
    source_lang = TextBlob(query_string).detect_language()
    if source_lang != target_lang:
        query_string = translate_query(TextBlob(query_string), source_lang, target_lang)
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

# create a dependency tree for a proverb (svg image)
def create_tree(doc, nlp):
    doc = nlp(doc)
    options = {"color": "#D3F4F8", "bg": "#082F49"}
    svg = displacy.render(doc, style="dep", options=options, jupyter=False)
    file_name = '-'.join([w.text for w in doc if not w.is_punct]) + ".svg"
    print(file_name)
    output_path = Path("static/" + file_name)
    output_path.open("w", encoding="utf-8").write(svg)
    return output_path

# create normal tf-idf vectors with stemming
gv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2", tokenizer=textblob_tokenizer)

#Initialize Flask instance
app = Flask(__name__)

#Function search() is associated with the address base URL + "/search"
@app.route('/search')
def search():

    # remember to delete old images from static!

    # for creating dependency trees
    nlp_en = spacy.load("en_core_web_sm")
    nlp_es = spacy.load("es_core_news_sm") # HUOM! muista ladata: python -m spacy download es_core_news_sm
    # finnish dependency data does not exist yet in spacy

    #Get query from URL variable
    proverb_query = request.args.get('proverb')
    meaning_query = request.args.get('meaning')

    # get language from url variable
    language = request.args.get('language')
    print(str(language))

    # default = english
    proverb_document = proverbs_en
    meaning_document = meanings_en
    nlp = nlp_en

    if language == 'es':
        proverb_document = proverbs_es
        meaning_document = meanings_es
        nlp = nlp_es

    elif language == 'fi':
        proverb_document = proverbs_fi
        meaning_document = meanings_fi

    #Initialize list of matches
    proverb_matches = [] # all the docs that matched the proverb or meaning query
    meaning_matches = []
    proverb_results = [] # a list of dicts {'name': doc, 'pltpath': output_path(of the image)}
    meaning_results = []

    matches = []

    # if user enters a query into the first search field:
    if proverb_query:
        try:
            matches = search_documents(proverb_query, proverb_document, language)

            # matches is a list of tuples (relevance_score, doc_id)
            for elem in matches:
                # make a list of all matching documents:
                doc_id = elem[1]
                proverb_matches.append(proverb_document[elem[1]])

                # create image

                proverb = proverb_document[doc_id]
                if language != 'fi':
                    output_path = create_tree(proverb, nlp)
                else:
                    output_path = Path("static/000_no_image.svg")

                meaning = meaning_document[doc_id]

                proverb_results.append({'name': proverb, 'meaning':meaning, 'pltpath': output_path})
                matches = proverb_results

        except IndexError:
            print("Something went wrong")

    # if user enters a query into the second search field:
    elif meaning_query:
        try:
            matches = search_documents(meaning_query, meaning_document)

            # matches is a list of tuples (relevance_score, doc_id)
            for elem in matches:
                # make a list of all matching documents:
                doc_id = elem[1]
                meaning_matches.append(proverb_document[doc_id])

                # create image
                proverb = proverb_document[doc_id]
                output_path = create_tree(proverb, nlp)

                meaning = meaning_document[doc_id]

                meaning_results.append({'name': proverb, 'meaning': meaning, 'pltpath': output_path})
                matches = meaning_results
        except IndexError:
            print("Something went wrong")

    #Render index.html with matches variable
    return render_template('index.html', matches=matches[:5])

# IndexError
#
# IndexError: too many indices for array
# textblob.exceptions.NotTranslated