import re

text_doc = ""
file_name = "meanings_fi.txt"
try:
    file = open(file_name, "r", encoding='utf-8')
    text_doc = file.read()
    file.close()
except OSError:
    print("Error reading the file", file_name)

list = text_doc.split('\n<ENDS HERE>')



with open(file_name, "w", encoding="utf-8") as file:  # change 'w' to 'a' to append
    for item in list:
        pois = item.find("\n")
        item = item[pois+1:]
        item = re.sub("\[edit\]", ": ", item)
        file.write(item + "\n<ENDS HERE>")

file.close()