# FROM: https://github.com/jrvc/txtMining_plotting-example/blob/master/example.py

from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib as mlp
import re
import nltk
import os

mlp.use('Agg')
# Load the file with the wiki articles
fpath='data/enwiki-20181001-corpus.100-articles.txt'
with open(fpath,'r') as f:
    soup = BeautifulSoup(f,'lxml')

#generate a dictinoary with the entries and the content for each article
example_data = {art['name']:art.text for art in soup.find_all('article') }
frequencies={}
for key in example_data:
    frequencies[key] = nltk.FreqDist(example_data[key].lower().split())

#words=sum(example_data.items(),())
#words=''.join(words)
#words_fdist=nltk.FreqDist(words.split())


#Initialize Flask instance
app = Flask(__name__)

def generate_query_plot(query,matches):
    # create a figure
    fig = plt.figure()
    plt.title("Word distribution per document \n query: "+query)
    # some values we will use to generate a plot
    dist_dict={}
    for match in matches:
        dist_dict[match['name']] = len(match['content'])
    # from a dictionary we can create a plot in two steps:
    #  1) plotting the bar chart
    #  2) setting the appropriate ticks in the x axis
    plt.bar(range(len(dist_dict)), list(dist_dict.values()), align='center')
    plt.xticks(range(len(dist_dict)), list(dist_dict.keys()),rotation=30) # labels are rotated
    # make room for the labels
    plt.gcf().subplots_adjust(bottom=0.30) # if you comment this line, your labels in the x-axis will be cutted
    plt.savefig('static/query_plot.png')


def generate_individual_plots(query,art_name, content, pieces):
    fig = plt.figure()
    plt.title(art_name+'\n Word frequency distribution for query: '+query)
    # YOUR code here:
    plt.bar(range(20), list(frequencies[art_name].values())[:20], align='center')
    plt.xticks(range(20), list(frequencies[art_name].keys())[:20],rotation=30)
    plt.gcf().subplots_adjust(bottom=0.30) # if you comment this line, your labels in the x-axis will be cutted
    #
    plt.savefig('static/'+art_name+'_plt.png')

    #fig
def extract_pieces(query,content):
    start_indexes = [m.start() for m in re.finditer(query,content.lower())]
    pieces=[]
    for i in start_indexes:
        index1=content[max(i-15,0):i].find('\n')+1
        index2=content[i:i+100].find('\n')
        pieces.append('...'+content[max(0,i-15+index1):i+100-(100-index2)*(index2>0)]+'...')
        #print(i, content[i-15+index1:i+100-(100-index2)*(index2>0)])
    return pieces[:min(5,len(pieces))]

#Function search() is associated with the address base URL + "/search"
@app.route('/search')
def search():
    #Delete previous plots, to avoid having too many of them
    os.system('rm -f static/*.png')
    #Get query from URL variable
    query = request.args.get('query')

    #Initialize list of matches
    matches = []

    #If query not empty
    if query:
        #Look at each entry in the example data
        for art_name,content in example_data.items():
            #If an entry name contains the query, add the entry to matches
            if query.lower() in content.lower():
                extracted_content = extract_pieces(query.lower(),content)
                matches.append({'name':art_name,'content':extracted_content,'pltpath':art_name+'_plt.png' })
                generate_individual_plots(query.lower(),art_name,content,extracted_content)
        generate_query_plot(query, matches)
        #Render index.html with matches variable
        return render_template('index.html', matches=matches)
    else:
        return render_template('indexempty.html', matches=[])