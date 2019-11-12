# WEEK 2 Task: Search engine

import nltk
from sklearn.feature_extraction.text import CountVectorizer

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
    loppu = d.find(">")
    name = d[alku:loppu]
    text = d[loppu + 1:]
    dict[name] = text


# CREATING THE MATRIX
# use scikit's count vectorizer to convert documents to a matrix of tokens
# binary=true --> all non zero counts are set to 1
# -->(doesn't measure token counts but whether the term is in the document or not)
cv = CountVectorizer(lowercase=True, binary=True)

# print a sparse matrix
# cv learns the vocabulary dictionary and returns a document-term matrix
sparse_matrix = cv.fit_transform(documents)

# dense version of the same matrix:
dense_matrix = sparse_matrix.todense()

# transpose into term-document matrix:
# rows=terms, columns=documents (ordered by terms for faster lookup)
td_matrix = dense_matrix.T   # .T transposes the matrix
terms = cv.get_feature_names()  # list of all terms

# term-to-index vocabulary {"term" : <index>}
t2i = cv.vocabulary_


# SIMPLE QUERY PARSER

# operator replacements
operators = {"and": "&", "AND": "&",
     "or": "|", "OR": "|",
     "not": "1 -", "NOT": "1 -",
     "(": "(", ")": ")"}

# rewrites the operators (and, or, not), or
# if the token is not an operator, returns the row for the term in term-document matrix:
def rewrite_token(t):
    if t in operators.keys():
        newtoken = operators.get(t)
    elif t in terms:
        newtoken = 'td_matrix[t2i["{:s}"]]'.format(t)
    else:
        newtoken = "NOTFOUND"

    #return operators.get(t, 'td_matrix[t2i["{:s}"]]'.format(t))
    return newtoken


# splits query into tokens, rewrites all tokens and joins them together:
def rewrite_query(query):
    # query in a list form:
    tokens = [rewrite_token(t) for t in query.split()]
    print(tokens)

    if "NOTFOUND" in tokens:
        idx = tokens.index("NOTFOUND")

        if len(tokens) == 1: # only 1 word in query (NOTFOUND)
            print("Word was not found.")

        # when query includes "NOT NOTFOUND"
        if idx > 0: # NOTFOUND is not first token
            if tokens[idx - 1] == "1 -":
                print("NOT this word")
                if len(tokens) == 2: # only NOT NOTFOUND
                    print("this should return every article")

                if len(tokens) > 2: # there are other words
                    print("remove not notfound and make the other part of the query")
                    # remove | or & sign from either side

        if len(tokens) > 2:
            if idx < (len(tokens) - 1):
                if tokens[idx + 1] == "&":  # NOTFOUND and ...
                    print("return 0 results: word not found")
                if tokens[idx + 1] == "|":  # NOTFOUND or ...
                    print("remove notfound or and make the other part of the query")

            if idx > 1:
                if tokens[idx - 1] == "&":  # ... & NOTFOUND
                    print("return 0 results: word not found")
                if tokens[idx - 1] == "|":  # ... | NOTFOUND
                    print("remove or notfound and make the other part of the query")

        return -1


    else: # all terms exist, query is fine
        newquery = " ".join(rewrite_token(t) for t in query.split())
        return newquery

    #return " ".join(rewrite_token(t) for t in query.split())

def test_query(query):
    print("Query: '" + query + "'")
    print("Rewritten:", rewrite_query(query))
    print("Matching:", eval(rewrite_query(query))) # Eval runs the string as a Python command
    print()

def show_doc(query):
    # matching documents as a matrix of one row:
    q = rewrite_query(query)

    if q == -1:
        print("Problem with one of the words. Try again.")

    else:
        hits_matrix = eval(rewrite_query(query))  # runs the query

        # the y-coordinates (doc indexes) of the non-zero elements converted to a list:
        hits_list = list(hits_matrix.nonzero()[1])

        #   print(hits_list)
        count = 0
        for doc_idx in hits_list:
            print("<Matching article:", documents[doc_idx][15:200] + "...")
            print()
            count += 1
            if count > 4:
                print("Showing the first five of", len(hits_list), "articles.")
                return


# MAKING QUERIES
print("Welcome to the search engine!")
print("Data: 1000 Wikipedia articles")
# Ask the user to type a query
query = str(input("Enter a query: "))
while query != "":
    # hits_matrix = eval(rewrite_query(query))
    try:
        #test_query(query)
        show_doc(query)
        query = str(input("Enter a new query (enter blank if you want to quit): "))
    except KeyError:
        query = str(input("Your search failed. Try again: "))
else:
    print("Goodbye!")

