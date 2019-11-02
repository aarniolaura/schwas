# TASK 1: TEXT MINING FROM THE WEB

# 1. Download content from a web page
# 2. Extract plain text from the HTML document
# 3. Extract only certain parts of the text

import nltk, re, pprint
from nltk import word_tokenize
from urllib import request
from bs4 import BeautifulSoup
from datetime import date

today = date.today()
day = today.strftime("%B %d, %Y")
print("Today is ", day)

print("Historical events that happened on this day according to Wikipedia:\n")

# From nltk book ch 3:

# download the document
url = "https://en.wikipedia.org/wiki/Main_Page"
html = request.urlopen(url).read().decode('utf8')
#print(html)

# Use beautiful soup to find the text in the file
raw = BeautifulSoup(html, 'html.parser').get_text()

# starting point of the text segment
onthisday = raw.find("On this day")
# ending point of the text segment
anniv = raw.find("More anniversaries:")

raw = raw[onthisday:anniv]
print(raw)

# removes all new lines:
sentence = " ".join(re.split("\s+", raw, flags=re.UNICODE))
print(sentence)


# tokenization (if needed)

# tokens = word_tokenize(raw)
# print(tokens)

# create an NLTK text from this list of tokens (if needed)

# text = nltk.Text(tokens)
# print(type(text))
# print(text)
