
wikipedia = ""
file_name = "enwiki-20181001-corpus.100-articles.txt"
try:
    file = open(file_name, "r", encoding='utf-8')
    wikipedia = file.read()
    file.close()
except OSError:
    print("Error reading the file", file_name)

print(wikipedia[:100])

print(wikipedia.find("</article>"))

docs = wikipedia.split('</article>')

print(len(docs))

for i in docs:
    print(i)
