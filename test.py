
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

dict = {}
for d in docs:
    alku = d.find("<article name=")
    loppu = d.find(">")
    name = d[alku:loppu]
    text = d[loppu + 1:]
    dict[name] = text

for k, v in dict.items():
    print("otsikko")
    print(k)
    print("teksti")
    print(v)
