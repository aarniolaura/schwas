# WEEK 2 Task: Search engine

# Data:
wikipedia = ""
file_name = "enwiki-20181001-corpus.100-articles.txt"
try:
    file = open(file_name, "r", encoding='utf-8')
    wikipedia = file.read()
    file.close()
except OSError:
    print("Error reading the file", file_name)

# Split into lists of strings (each article is a string)
docs = wikipedia.split('</article>')

print(len(docs))

for i in docs:
    print(i)

# Create a dictionary (article name: article contents) if needed
dict = {}
for d in docs:
    alku = d.find("<article name=")
    loppu = d.find(">")
    name = d[alku:loppu]
    text = d[loppu + 1:]
    dict[name] = text