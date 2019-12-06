# DATA
text_doc = ""
file_name = "proverbs_A-D_en.txt"
try:
    file = open(file_name, "r", encoding='utf-8')
    text_doc = file.read()
    file.close()
except OSError:
    print("Error reading the file", file_name)

# Split into lists of strings (each article is a string)
proverb_document = text_doc.split('\n<ENDS HERE>')

text_doc = ""
file_name = "meanings_A-D_en.txt"
try:
    file = open(file_name, "r", encoding='utf-8')
    text_doc = file.read()
    file.close()
except OSError:
    print("Error reading the file", file_name)

meaning_document = text_doc.split('<ENDS HERE>')

print(proverb_document[5:10])
