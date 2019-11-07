# WEEK 2 Task: Search engine

import nltk
from sklearn.feature_extraction.text import CountVectorizer

# Data:
wikipedia = ""
file_name = "enwiki-20181001-corpus.100-articles.txt"
try:
    file = open(file_name, "r", encoding='utf-8')
    wikipedia = file.read()
    file.close()
except OSError:
    print("Error reading the file", file_name)

# Split into lists of strings (each article is a string)
documents = wikipedia.split('</article>')

#print(len(documents))

#for i in documents:
#    print(i)

# Create a dictionary (article name: article contents) if needed
dict = {}
for d in documents:
    alku = d.find("<article name=")
    loppu = d.find(">")
    name = d[alku:loppu]
    text = d[loppu + 1:]
    dict[name] = text

cv = CountVectorizer(lowercase=True, binary=True)

# print a sparse matrix
sparse_matrix = cv.fit_transform(documents)

#print("Document-term matrix: (?)\n")
#print(sparse_matrix)

# Anyway, let's print a _dense_ version of this matrix:
dense_matrix = sparse_matrix.todense()

#print("Document-term matrix: (?)\n")
#print(dense_matrix)

td_matrix = dense_matrix.T   # .T transposes the matrix
terms = cv.get_feature_names()
t2i = cv.vocabulary_  # shorter notation: t2i = term-to-index

# ## Simple query parser

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

def show_doc(query):
    hits_matrix = eval(rewrite_query(query))
    hits_list = list(hits_matrix.nonzero()[1])
#   print(hits_list)
    count = 0
    for doc_idx in hits_list:
        print("Matching doc:", documents[doc_idx][:200] + "...")
        print()
        count += 1
        if count > 4:
            return print("Showing the first five of",len(hits_list),"articles.")


# Ask the user to type a query
query = str(input("Enter a query: "))
while query != "":
    # hits_matrix = eval(rewrite_query(query))
    test_query(query)
    show_doc(query)


    query = str(input("Enter a new query (enter blank if you want to quit): "))
else:
    print("Goodbye!")

