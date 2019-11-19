# TASK 1: TEXT MINING FROM THE WEB

# 1. Download content from a web page
# 2. Extract plain text from the HTML document
# 3. Extract only certain parts of the text

import nltk, re, pprint
from urllib import request
from bs4 import BeautifulSoup
from datetime import date

today = date.today()
day = today.strftime("%B %d, %Y")
print("Today is ", day)
print()
print("Historical events that happened on this day according to Wikipedia:\n")

# 1. Download the content
url = "https://en.wikipedia.org/wiki/Main_Page"
html = request.urlopen(url).read().decode('utf8')
#print(html)

# Remove this thumbcaption now because it's easier to find in html:
# <div class="thumbcaption" style="padding: 0.25em 0; word-wrap: break-word;">George Eliot</div></div>
html = re.sub(r'<div class="thumbcaption"', '', html)
html = re.sub(r'style="padding:.*word-wrap:', '', html)
html = re.sub(r'break-word;">.*</div></div>', '', html)

# 2. Use beautiful soup to extract the text in the html file
raw = BeautifulSoup(html, 'html.parser').get_text()

# 3. Extract the wanted segment:
# starting point of the text segment
onthisday = raw.find("On this day")
# ending point of the text segment
anniv = raw.find("More anniversaries:")

raw = raw[onthisday:anniv]

# Remove excess new lines
segment = re.sub('\n\n\n', '\n', raw)
print(segment)
