This is an search engine application that allows you to search for proverbs in multiple languages. You can choose to search for English, Spanish or Finnish proverbs and you can enter you query in any language. There are two query fields: the first one is for finding a proverbs that contains a specific word or words; while the second one is for finding proverbs that have a certain meaning. Results will display the most relevant proverbs, their meanings, and images related to them.  

The data for all languages comes from Wiktionary (https://en.wiktionary.org/wiki/Category:English_proverbs, https://en.wiktionary.org/wiki/Category:Spanish_proverbs, https://en.wiktionary.org/wiki/Category:Finnish_proverbs). All the data is already contained in the Final_project directory in text files.  
TD-IDF weighting is used to calculate the relevance score of the proverb documents compared to the search query.  
Stemming is used for queries made in (or translated to) English.  

Instructions for getting the proverb search engine running:

1. Copy the directory Final_project into your directory.

2. Create and activate a virtual environment (e.g. .../virtualenv/scripts/activate.bat).

3. Once the venv is activated, install the following packages into it:  
  pip install Flask  
  pip install sklearn  
  pip install textblob  
  pip install beautifulsoup4  
  pip install google_images_download  
  (also install scipy if for some reason not already installed)  
  (also install spacy if you want to print dependency trees with create_tree function (commented out by default)  

4. Type the following commands:  
  set FLASK_APP=proverb_search.py  
  set FLASK_ENV=development  
  set FLASK_RUN_PORT=8000  

5. Type: flask run

6. Open a web browser and go to the address given in your command line + "/search".

7. Find exciting proverbs! :)
