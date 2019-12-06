# FROM: https://dev.to/pranay749254/build-a-simple-python-web-crawler

import requests
from bs4 import BeautifulSoup
from urllib import request
from urllib.request import Request, urlopen
import re


def web(page,WebUrl):
    if(page>0):
        url = WebUrl
        code = requests.get(url)
        plain = code.text
        s = BeautifulSoup(plain, "html.parser")
        pagelist = []
        for link in s.findAll('a'):
           # tet = link.get('title')
           # print(tet)
            tet_2 = link.get('href')
            #print(tet_2)
            pagelist.append(tet_2)
        return pagelist

def get_text(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    raw = BeautifulSoup(webpage, 'html.parser').get_text()
    return raw

def remove_newlines(document_string):
    text = document_string.strip()
    text = ' '.join(line.strip() for line in text.split('\n') if line.strip())
    return text

pagelist = web(1,'https://www.phrases.org.uk/meanings/phrases-and-sayings-list.html')
print(len(pagelist))

index = 0
for page in pagelist:
    print(index, page)
    index += 1

pagelist = pagelist[82:2352]

meaning_list = []
index = 100
for page in pagelist[100:200]:
    url = "https://www.phrases.org.uk/meanings/" + page
    raw = get_text(url)

    start = raw.find("What's the meaning")
    end = raw.find("What's the origin")

    if start == -1 or end == -1:
        content = "NOT FOUND"
    else:
        content = raw[start:end]
        nline = content.find("\n")
        content = content[nline + 1:]

    re.sub("\n", " ", content)
    content = remove_newlines(content)

    meaning_list.append((index, content))
    index +=1

#file = open("meanings.txt","w+")

with open("meanings.txt", "a", encoding="utf-8") as file:
    for i, m in meaning_list:
        print(i, m)
        print()
        file.write(str(i) + " " + m + "\n")

file.close()

 #   content = crawl(page)
  #  meaning_list.append(content)

# req = Request('https://www.phrases.org.uk/meanings/abracadabra.html', headers={'User-Agent': 'Mozilla/5.0'})
# webpage = urlopen(req).read()
# raw = BeautifulSoup(webpage, 'html.parser').get_text()
# start = raw.find("What's the meaning of the phrase")
# end = raw.find("What's the origin of the phrase")
# content = raw[start:end]
# print(content)

#url = "https://www.phrases.org.uk/meanings/" + url
#url = "https://www.phrases.org.uk//meanings/a-horse-a-horse-my-kingdom-for-a-horse.html"
#html = request.urlopen(url).read().decode('utf8')
#raw = BeautifulSoup(html, 'html.parser').get_text()