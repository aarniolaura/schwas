import re

text_doc = ""
file_name = "meanings_en.txt"
try:
    file = open(file_name, "r", encoding='utf-8')
    text_doc = file.read()
    file.close()
except OSError:
    print("Error reading the file", file_name)

list = text_doc.split('\n<ENDS HERE>')


filename = "edit_mean.txt"

with open(filename, "w", encoding="utf-8") as file:  # change 'w' to 'a' to append
    for item in list:
        pois = item.find("\n")
        item = item[pois+1:]
        item = re.sub("\[edit\]", ": ", item)
        file.write(item + "\n<ENDS HERE>")

file.close()