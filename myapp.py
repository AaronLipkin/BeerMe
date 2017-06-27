from __future__ import print_function # In python 2.7
import sys
import flask
from flask import request, render_template
from flask_cors import CORS, cross_origin
import json
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pickle
import jinja2

reload(sys)
sys.setdefaultencoding('utf-8')

app = flask.Flask(__name__)
CORS(app)
print(app.static_folder, file=sys.stderr)

#-------- MODEL GOES HERE -----------#
pkl_file = open('/var/www/html/myapp/scaled2.pkl', 'rb')
scaled = pickle.load(pkl_file)

pkl_file = open('/var/www/html/myapp/name_pop.pkl', 'rb')
names = pickle.load(pkl_file)
choices = list(names['name'])

def recommend_by_id(x, pop, res):
    sims = cosine_similarity(scaled,scaled.loc[x,:].values.reshape(1, -1)).ravel()
    sims0 = {}
    counter = 0
    for i in list(scaled.index):
        sims0[i] = sims[counter]
        counter += 1
    sims1 = pd.Series(sims0)
    sims1.sort_values(inplace=True)
    sims1 = sims1[::-1]
    listo = list(sims1[:100].index)
    resut = []
    for i in listo:
        resut.append([i,names.loc[i,'name'], names.loc[i,'pop']])
    return pd.DataFrame(resut)[pd.DataFrame(resut)[2] > pop].iloc[:res,:]

def find_beer(name):
    if name in choices:
	return names[names['name'] == name].index.tolist()[0],name
    try:
    	found = process.extractOne(name, choices, scorer=fuzz.token_set_ratio)
    except:
	try:
	    found = process.extractOne(name, choices, scorer=fuzz.QRatio)
	except:
	    try:
		found = process.extractOne(name, choices, scorer=fuzz.WRatio)
	    except:
		pass
    return names[names['name'] == found[0]].index.tolist()[0],found[0]

#-------- ROUTES GO HERE -----------#

@app.route('/')
@cross_origin()
def page():
   return app.send_static_file('index.html')


@app.route('/suggestions', methods=['GET','POST'])
@cross_origin()
def result():
    '''Gets prediction using the HTML form'''
    if flask.request.method == 'POST':
        beer =  str(request.form['beer'])
	popularity = int(request.form['pop'])
	resi = int(request.form['results'])
        beer,name =  find_beer(beer)
        result = recommend_by_id(int(beer),popularity,resi)
	result = result.values.tolist()
        results = {'input':name, 'recommendations':[]}
        for i,j,k in result:
            results['recommendations'].append({'name':j,'ABV':names.loc[i,'ABV']})
        return render_template('output.html', input = results['input'], beers=results['recommendations'])

if __name__ == '__main__':
    '''Connects to the server'''
    app.run()
