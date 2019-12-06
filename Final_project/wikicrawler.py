# FROM: https://dev.to/pranay749254/build-a-simple-python-web-crawler

import requests
from bs4 import BeautifulSoup
from urllib import request
from urllib.request import Request, urlopen
import re

# https://en.wiktionary.org/wiki/Category:English_proverbs
# https://en.wiktionary.org/wiki/Category:Spanish_proverbs
# https://en.wiktionary.org/wiki/Category:Finnish_proverbs

def web(page,WebUrl):
    if(page>0):
        url = WebUrl
        code = requests.get(url)
        plain = code.text
        s = BeautifulSoup(plain, "html.parser")
        pagelist = []

        for link in s.find_all("div", class_="mw-category-generated"):

            for link in s.find_all('a'):
                title = link.get('title')
                addr = link.get('href')
                pagelist.append((title, addr))
        return pagelist

def get_text(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    raw = BeautifulSoup(webpage, 'html.parser').get_text()
    return raw

def remove_newlines(document_string):
    text = document_string.rstrip()
    text = '\n'.join(line.strip() for line in text.split('\n') if line.strip())
    return text

def add_meanings(pagelist):
    meaning_list = []
    index = 0
    for t, a in pagelist:
        url = "https://en.wiktionary.org" + a
        raw = get_text(url)

        start = raw.find("Proverb[edit]")
        start = start + 13
        end = raw.find("Translations[edit]")
        if end == -1:
            end = raw.find("References[edit]")
            if end == -1:
                end = raw.find("Retrieved from")

        if start == -1 or end == -1:
            content = "NOT FOUND"
        else:
            content = raw[start:end]

        content = remove_newlines(content)
        # print("\nTitle: ", t)
        # print(content)

        meaning_list.append((t, content))
        index += 1

    return meaning_list

def write_to_file(list, filename):
    with open(filename, "w", encoding="utf-8") as file: # change 'w' to 'a' to append
        for item in list:
            file.write(item + "\n<ENDS HERE>")
            # add some word to split the file later (<END>)

    file.close()

def main():

    pagelist = web(1,'https://en.wiktionary.org/wiki/Category:English_proverbs')
    pagelist = pagelist[62:260]

    meaning_list = add_meanings(pagelist)

    p_list = []
    for title, content in meaning_list:
        p_list.append(title)

    m_list = []
    for title, content in meaning_list:
        m_list.append(content)

    write_to_file(p_list, "proverbs_A-D_en.txt")
    write_to_file(m_list, "meanings_A-D_en.txt")

main()