#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 16:27:52 2018

@author: root
"""
from flask import Flask
import ssl
from flask_cors import CORS
from flask import request
from pyfasttext import FastText
#context = SSL.Context(SSL.SSLv23_METHOD)
#context.use_privatekey_file('infocommsociety.com.key')
#context.use_certificate_file('infocommsociety.com.crt')
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('cert1.pem', 'privkey1.pem')
app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def main():
    if request.method == 'POST':
        data = request.form['message']
        print(data)
        data_list = data.split('. ')
        mode = 'test'
        if mode == 'test':
            model = FastText('./model.bin')
            #test = ['Says the Annies List political group supports third-trimester abortions on demand.\n']
            list_out = []
            for sentence in data_list:
                test = [sentence+'.\n']
                test_pred = model.predict(test, k=1)
                output = test_pred[0][0]
                out = sentence + '._' + output + '\n'
                list_out.append(out)
            str_out = ''.join(list_out)
        return ("Prediction:\n"+str_out)
if __name__ == '__main__':
    CORS(app)
    app.run(debug=True,port=5000,host='0.0.0.0', ssl_context=context)