import requests
from bs4 import BeautifulSoup
from urllib import request
from urllib.request import Request, urlopen


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

def crawl(url):
    url = "https://www.phrases.org.uk/meanings/" + url
    html = request.urlopen(url).read().decode('utf8')
    raw = BeautifulSoup(html, 'html.parser').get_text()
    return raw


#web(1,'https://www.phrases.org.uk/meanings/phrases-and-sayings-list.html')

pagelist = []
pagelist = web(1,'https://www.phrases.org.uk/meanings/phrases-and-sayings-list.html')

print(len(pagelist))
index = 0
for page in pagelist:
    print(index, page)
    index += 1

pagelist = pagelist[82:]



#url = "https://www.phrases.org.uk/meanings/" + url
#url = "https://www.phrases.org.uk//meanings/a-horse-a-horse-my-kingdom-for-a-horse.html"
#html = request.urlopen(url).read().decode('utf8')
#raw = BeautifulSoup(html, 'html.parser').get_text()

meaning_list = []

for page in pagelist:
    url = "https://www.phrases.org.uk/meanings/" + page
    print(url)

    req = Request(url,
                  headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    raw = BeautifulSoup(webpage, 'html.parser').get_text()
    start = raw.find("What's the meaning of")
    end = raw.find("What's the origin of the phrase")
    content = raw[start:end]

    print(content)

 #   content = crawl(page)
  #  meaning_list.append(content)


req = Request('https://www.phrases.org.uk/meanings/abracadabra.html', headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
raw = BeautifulSoup(webpage, 'html.parser').get_text()
start = raw.find("What's the meaning of the phrase")
end = raw.find("What's the origin of the phrase")
content = raw[start:end]
print(content)