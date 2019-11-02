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
url = "https://en.wikipedia.org/wiki/Main_Page"
html = request.urlopen(url).read().decode('utf8')
#print(html)

# Use beautiful soup to find the text in the file
raw = BeautifulSoup(html, 'html.parser').get_text()
tokens = word_tokenize(raw)
print(tokens)
onthisday = raw.find("On this day")
print(onthisday)

anniv = raw.find("More anniversaries:")
print(anniv)

print(raw[onthisday:anniv])


# create an NLTK text from this list of tokens
text = nltk.Text(tokens)
print(type(text))
length = len(text)
print(text[length-100:length-1])
