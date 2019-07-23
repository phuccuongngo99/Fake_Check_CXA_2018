#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 19:22:47 2018

@author: root
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 20:24:00 2018

@author: valaxw
"""
import time
import numpy as np
import re
from collections import defaultdict
from nltk import word_tokenize
from nltk.corpus import stopwords
import nltk
import pickle
import threading

import requests
from bs4 import BeautifulSoup

from pyfasttext import FastText
from sklearn.externals import joblib

###Debugging
"""
f_glove = open("glove.6B.50d.txt", "rb")
glove_vectors = {}
for line in f_glove:
    glove_vectors[str(line.split()[0]).split("'")[1]] = np.array(list(map(float, line.split()[1:])))
"""
###

def stance(claim, glove_vectors):
    print(claim)
    start_time = time.time()
    pattern = re.compile("[^a-zA-Z0-9 ]+")  # Remove punctuation, symbols, etc.
    stop_words = set(stopwords.words('english'))
    
    def fasttext(text):
        test_data = text.replace('\n',' ')
        model = FastText('./model_audit.bin')
        test = test_data+'\n'
        pred = model.predict_proba_single(test, k=2)
        out = pred[0][1]
        return out
    
    def tokenise(text):
        text = pattern.sub('', text.replace('\n', ' ').replace('-', ' ').lower())
        words = word_tokenize(text)
        text2 = []
        for i in range(len(words)):
            if words[i] =="not" and i<len(words)-1:
                text2.append(words[i]+words[i+1])
            else:
                text2.append(words[i])
        text = ' '.join(text2)        
        text = [word for word in word_tokenize(text) if word not in stop_words]
        return text
    
    def consider(statement, num = 20):
        text = tokenise(statement)
        arr = nltk.pos_tag(text)
        
        considered = []
        check = 0
        for i in arr:
            if (i[1] == 'CD' or i[1] == 'JJ' or i[1] == 'JJR' or i[1] == 'JJS' or i[1] == 'NNP' or i[1] == 'NN' or i[1] == 'NNPS' or i[1] == 'NNS' or i[1] == 'VB' or i[1] == 'VBD' or i[1] == 'VBG' or i[1] == 'VBN' or i[1] == "VBP" or i[1] == "VBZ") and check == 0: 
                considered.append(i[0])
            check = 0
        if num is not None:        
            return considered[:num]
        else:
            return considered
    
    def querified(statement, num = 20):
        query_list = consider(statement, num=num)
        query = str(query_list[0])
        
        for i in range(1, len(query_list)):
            query += " "
            query += str(query_list[i])
    
        query = query.replace(" ","+")
        query = ''.join(query)
        
        return query
    
    def doc_to_tf(text, ngram=1):
        words = tokenise(text)
        ret = defaultdict(float)
        for i in range(len(words)):
            for j in range(1, ngram + 1):
                if i - j < 0:
                    break
                word = [words[i - k] for k in range(j)]
                ret[word[0] if ngram == 1 else tuple(word)] += 1.0
        return ret
    
    
    idf = pickle.load(open("idf.pkl", "rb"))
    #print(type(idf))
    
    def doc_to_glove(doc):
        doc_tf = doc_to_tf(doc)
        doc_tf_idf = defaultdict(float)
        for word, tf in doc_tf.items():
            doc_tf_idf[word] = tf * idf[word]
    
        doc_vector = np.zeros(glove_vectors['glove'].shape[0])
        if np.sum(list(doc_tf_idf.values())) == 0.0:  # edge case: document is empty
            return doc_vector
    
        for word, tf_idf in doc_tf_idf.items():
            if word in glove_vectors:
                doc_vector += glove_vectors[word] * tf_idf
        doc_vector /= np.sum(list(doc_tf_idf.values()))
        return doc_vector
    
    # Compute cosine similarity of GLoVe vectors for all headline-body pairs
    def dot_product(vec1, vec2):
        sigma = 0.0
        for i in range(vec1.shape[0]):  # assume vec1 and vec2 has same shape
            sigma += vec1[i] * vec2[i]
        return sigma
    
    
    def magnitude(vec):
        return np.sqrt(np.sum(np.square(vec)))
    
    
    def cosine_similarity(doc):
        headline_vector = doc_to_glove(doc[0])
        body_vector = doc_to_glove(doc[1])
    
        if magnitude(headline_vector) == 0.0 or magnitude(body_vector) == 0.0:  # edge case: document is empty
            return 0.0
    
        return dot_product(headline_vector, body_vector) / (magnitude(headline_vector) * magnitude(body_vector))
    
    # Compute the KL-Divergence of language model (LM) representations of the headline and the body
    def divergence(lm1, lm2):
        sigma = 0.0
        for i in range(lm1.shape[0]):  # assume lm1 and lm2 has same shape
            sigma += lm1[i] * np.log(lm1[i] / lm2[i])
        return sigma
    
    
    def kl_divergence(doc, eps=0.1):
        # Convert headline and body to 1-gram representations
        tf_headline = doc_to_tf(doc[0])
        tf_body = doc_to_tf(doc[1])
    
        # Convert dictionary tf representations to vectors (make sure columns match to the same word)
        words = set(tf_headline.keys()).union(set(tf_body.keys()))
        vec_headline, vec_body = np.zeros(len(words)), np.zeros(len(words))
        i = 0
        for word in words:
            vec_headline[i] += tf_headline[word]
            vec_body[i] = tf_body[word]
            i += 1
    
        # Compute a simple 1-gram language model of headline and body
        lm_headline = vec_headline + eps
        lm_headline /= np.sum(lm_headline)
        lm_body = vec_body + eps
        lm_body /= np.sum(lm_body)
    
        # Return KL-divergence of both language models
        return divergence(lm_headline, lm_body)
    
    # Other feature 1
    def ngram_overlap(doc):
        # Returns how many times n-grams (up to 3-gram) that occur in the article's headline occur on the article's body.
        tf_headline = doc_to_tf(doc[0], ngram=3)
        tf_body = doc_to_tf(doc[1], ngram=3)
        matches = 0.0
        for words in tf_headline.keys():
            if words in tf_body:
                matches += tf_body[words]
        return np.power((matches / len(tokenise(doc[1]))), 1 / np.e)  # normalise for document length
    
    # Define function to convert each document (headline, body) to feature vectors
    
    ftrs = [cosine_similarity, kl_divergence, ngram_overlap]
    
    def to_feature_array(doc):
        vec = np.array([0.0] * len(ftrs))
        for i in range(len(ftrs)):
            vec[i] = ftrs[i](doc)
        return vec
    
    
    pattern = re.compile("[^a-zA-Z0-9 ]+")  # Remove punctuation, symbols, etc.
    stop_words = set(stopwords.words('english'))
    
    #statement1 = input("Search for term: ")
    sent_score = fasttext(claim) * 100
    #print(sent_score)
    '''
    if cls=='sensational':
        quit()
        '''
    query = querified(claim, None)
    
    print(query)
    
    query = "https://www.google.com/search?q=" + query
    print(query)
    
    sites = []
    url = []
    r = requests.get(query)
    #html_doc = r.text
    html_doc = r.content
    soup = BeautifulSoup(html_doc, 'html.parser')
    #print('Hey', soup)
    
    file = open("soup.txt", "w+")
    file.write(soup.text)
    file.close()
    
    
    for link in soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
        sites = sites + re.split(":(?=http)",link["href"].replace("/url?q=",""))
    
    print('Big L')
    
    article = []
    print(len(sites))
    print(sites)
    for site in sites:
        if "PDF" in site:
            sites.remove(site)
    sites = sites[1:]
    
    def googling(site):
        try:
            r = requests.get(site)
            url.append(site)
            contents = r.text
            txt = []
            soup = BeautifulSoup(contents, 'html.parser')
            for g in soup.find_all('p'):
                txt.append(g.text)
            if len(txt)!= 0:
                article.append(''.join(txt))
        except Exception as e:
            print(e)
            print(site)
    
    
    threads = [threading.Thread(target=googling, args=(site,)) for site in sites]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    
    score = []
    
    for i in article:
        score.append(fasttext(i))
        
    int_to_label = ['agree', 'disagree', 'discuss']
    clf = joblib.load('Logistic_Regression.pkl')
    predictions = []
    
    for i in range(len(article)):
        st = article[i]
        x_pred = np.asarray([claim, st])
        x_pred = np.array([to_feature_array(x_pred)])
        y_pred = clf.predict(x_pred)
        predicted = int_to_label[y_pred[0]]
        predictions.append(predicted)
    
    agree_score = 0
    agree_sent = []
    disagree_score = 0
    disagree_sent = []
    discuss_sent = []
    
    for i in range(len(predictions)):
        if predictions[i]=='agree':
            agree_score+=score[i]
            agree_sent.append(url[i])
        elif predictions[i]=='disagree':
            disagree_score+=score[i]
            disagree_sent.append(url[i])
        elif predictions[i]=='discuss':
            discuss_sent.append(url[i])
    
    stance_score = agree_score / (agree_score + disagree_score) * 100
    overall_score = sent_score*0.1 + stance_score*0.9
    score = str(overall_score)+';;;'+str(sent_score)+';;;'+str(stance_score)
    print(len(agree_sent),len(disagree_sent),len(discuss_sent))
    final = []
    
    if overall_score >=50:
        for u in agree_sent:
            final.append("Agree: " + str(u))
        j = 0
        while len(final) < 5:
            try:
                final.append("Discuss: " + str(discuss_sent[j]))
                j+=1
            except:
                break
        k = 0
        while len(final) < 5:
            try:
                final.append("Disagree: " + str(disagree_sent[k]))
                k+=1
            except:
                break
    else:
        for i in disagree_sent:
            final.append("Disagree: " + str(i))
        j = 0
        while len(final) < 5:
            try:
                final.append("Discuss: " + str(discuss_sent[j]))
                j+=1
            except:
                break
        k = 0
        while len(final) < 5:
            try:
                final.append("Agree: " + str(agree_sent[k]))
                k+=1
            except:
                break
    overall = time.time()  - start_time
    print('overall', overall)
    return score + ';;;' + ';;;'.join(final)