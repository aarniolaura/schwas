# TASK 1: TEXT MINING FROM THE WEB

# 1. Download content from a web page
# 2. Extract plain text from the HTML document
# 3. Extract only certain parts of the text

import re
import requests
from bs4 import BeautifulSoup
from urllib import request

# 1. Download the content
url = "https://www.goodreads.com/quotes?page=1"
page = requests.get(url)

url2 = "https://www.goodreads.com/quotes?page=1"
html = request.urlopen(url).read().decode('utf8')

# 2. Use beautiful soup to extract the text in the html file
soup = BeautifulSoup(page.content, 'html.parser')
authors = []
quotes = []

def get_authors(soup, authors):
    count = 0
    while count != 30:
        authors.append(soup.find_all(class_='authorOrTitle')[count].get_text())
        count += 1
        authors = [x.replace('\n', '') for x in authors]

    else:
        print(authors)
        return authors

def get_quotes(soup, quotes):
    count = 0
    result = re.findall(r'ldquo(.*?)ldquo', html)
    print(result)
    #while count != 30:
    #    quotes.append(soup.find_all('&ldquo;')[count].get_text())
    #    count += 1
    #else:
    #    print(quotes)
    #    return quotes

#get_authors(soup, authors)
get_quotes(html, quotes)
