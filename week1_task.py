# TASK 1: TEXT MINING FROM THE WEB

# 1. Download content from a web page
# 2. Extract plain text from the HTML document
# 3. Extract only certain parts of the text

# From nltk book ch 3:
from urllib import request

url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
html = request.urlopen(url).read().decode('utf8')
html[:60]
'<!doctype html public "-//W3C//DTD HTML 4.0 Transitional//EN'
print(html)


# To parse a document, pass it into the BeautifulSoup constructor. You can pass in a string or an open filehandle:

from bs4 import BeautifulSoup

#with open("index.html") as fp:
#    soup = BeautifulSoup(fp)

#soup = BeautifulSoup("<html>data</html>")

