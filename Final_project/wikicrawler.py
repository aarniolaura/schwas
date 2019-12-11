# FROM: https://dev.to/pranay749254/build-a-simple-python-web-crawler

import requests
from bs4 import BeautifulSoup
from urllib import request
from urllib.request import Request, urlopen
import re

# https://en.wiktionary.org/wiki/Category:English_proverbs
# https://en.wiktionary.org/w/index.php?title=Category:English_proverbs&pagefrom=DANCE+WITH+THE+ONE+WHAT+BRUNG+YA%0Adance+with+the+one+what+brung+ya#mw-pages
# https://en.wiktionary.org/w/index.php?title=Category:English_proverbs&pagefrom=IN+FOR+A+PENNY%2C+IN+FOR+A+POUND%0Ain+for+a+penny%2C+in+for+a+pound#mw-pages
# https://en.wiktionary.org/w/index.php?title=Category:English_proverbs&pagefrom=ONE+HAIR+OF+A+WOMAN+CAN+DRAW+MORE+THAN+A+HUNDRED+PAIR+OF+OXEN%0Aone+hair+of+a+woman+can+draw+more+than+a+hundred+pair+of+oxen#mw-pages
# https://en.wiktionary.org/w/index.php?title=Category:English_proverbs&pagefrom=THE+MORE+THINGS+CHANGE%2C+THE+MORE+THEY+STAY+THE+SAME%0Athe+more+things+change%2C+the+more+they+stay+the+same#mw-pages
# https://en.wiktionary.org/w/index.php?title=Category:English_proverbs&pagefrom=YOU+CAN+CATCH+MORE+FLIES+WITH+HONEY+THAN+VINEGAR%0Ayou+can+catch+more+flies+with+honey+than+vinegar#mw-pages
#
# https://en.wiktionary.org/wiki/Category:Spanish_proverbs
#
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

# returns a list of tuples (proverb, meaning)
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
    # https://en.wiktionary.org/w/index.php?title=Category:English_proverbs&pagefrom=YOU+CAN+CATCH+MORE+FLIES+WITH+HONEY+THAN+VINEGAR%0Ayou+can+catch+more+flies+with+honey+than+vinegar#mw-pages

    pagelist = web(1,'https://en.wiktionary.org/wiki/Category:Finnish_proverbs')

    print(len(pagelist))
    i = 0
    for t, a in pagelist:
        print(i)
        print(t)
        print(a)
        print()
        i +=1

    pagelist = pagelist[39:198]

    meaning_list = add_meanings(pagelist)

    p_list = []
    for title, content in meaning_list:
        p_list.append(title)

    m_list = []
    for title, content in meaning_list:
        m_list.append(content)

    write_to_file(p_list, "proverbs_fi.txt")
    write_to_file(m_list, "meanings_fi.txt")

main()