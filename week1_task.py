# TASK 1: TEXT MINING FROM THE WEB

# 1. Download content from a web page
# 2. Extract plain text from the HTML document
# 3. Extract only certain parts of the text

import nltk, re, pprint
from nltk import word_tokenize
from urllib import request
from bs4 import BeautifulSoup

# From nltk book ch 3:

# download the document
url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
html = request.urlopen(url).read().decode('utf8')
#print(html)

# Use beautiful soup to find the text in the file
raw = BeautifulSoup(html, 'html.parser').get_text()
tokens = word_tokenize(raw)
print(tokens)

# create an NLTK text from this list of tokens
text = nltk.Text(tokens)
print(type(text))
print(text)


