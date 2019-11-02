# testing feedparser

import feedparser
import nltk, re, pprint
from nltk import word_tokenize
from urllib import request
from bs4 import BeautifulSoup


llog = feedparser.parse("http://languagelog.ldc.upenn.edu/nll/?feed=atom")
print(llog['feed']['title'])

print(len(llog.entries))

post = llog.entries[2]
print(post.title)

content = post.content[0].value
print(content[:70])

raw = BeautifulSoup(content, 'html.parser').get_text()
print(word_tokenize(raw))