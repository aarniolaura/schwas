import spacy
from spacy import displacy
from pathlib import Path

nlp = spacy.load("en_core_web_sm")
doc = nlp("This is a sentence.")

options = {"color": "#D01271", "bg": "#B5FFF6"}
svg = displacy.render(doc, style="dep", options=options, jupyter=False)

file_name = '-'.join([w.text for w in doc if not w.is_punct]) + ".svg"
print(file_name)
output_path = Path("static/" + file_name)
output_path.open("w", encoding="utf-8").write(svg)

# python -m spacy download es_core_news_sm
# nlp = spacy.load("es_core_news_sm")