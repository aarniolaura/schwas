from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from textblob import TextBlob


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
    if query:
        matches = search_documents(query)
        for elem in matches:
            matches2.append(documents[elem[1]])
    print(matches2)



    #Render index.html with matches variable
    return render_template('index.html', matches=matches2[:5])

