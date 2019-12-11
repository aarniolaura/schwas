# https://www.nltk.org/api/nltk.stem.html

import nltk
from nltk.stem.snowball import SnowballStemmer
print(" ".join(SnowballStemmer.languages))
stemmer = SnowballStemmer("finnish")

word = "lumipallojakaan"
print(word)
print(stemmer.stem(word))

