#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 19:27:38 2018

@author: root
"""
from pipeline import stance

from flask import Flask
from flask_cors import CORS
from flask import request
import numpy as np
#context = SSL.Context(SSL.SSLv23_METHOD)
#context.use_privatekey_file('infocommsociety.com.key')
#context.use_certificate_file('infocommsociety.com.crt')

f_glove = open("glove.6B.50d.txt", "rb")
glove_vectors = {}
for line in f_glove:
    glove_vectors[str(line.split()[0]).split("'")[1]] = np.array(list(map(float, line.split()[1:])))

app = Flask(__name__)
@app.route('/', methods=['POST','GET'])
def main():
    if request.method == 'POST':
        data = request.form['message']
        output = stance(data, glove)
        return (output)

if __name__ == '__main__':
    glove = glove_vectors
    CORS(app)
    app.run(debug=True,host='0.0.0.0')