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
