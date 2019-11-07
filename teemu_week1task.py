# To parse a document, pass it into the BeautifulSoup constructor. You can pass in a string or an open filehandle:

from urllib import request
import requests
from bs4 import BeautifulSoup
from nltk import word_tokenize
import csv


url = "https://old.reddit.com/r/Showerthoughts/"
html = request.urlopen(url).read().decode('utf8')
headers = {'User-Agent': 'Mozilla/5.0'}
page = requests.get(url, headers=headers)

soup = BeautifulSoup(page.text, 'html.parser')
domains = soup.find_all("span", class_="domain")

for domain in domains:
    if domain != "(self.showerthoughts)":
        continue
    print(domain)

title = post.find('p', class_="title").text