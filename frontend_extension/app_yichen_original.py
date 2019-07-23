#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 16:27:52 2018

@author: root
"""

from flask import Flask
import ssl
from flask_cors import CORS


#context = SSL.Context(SSL.SSLv23_METHOD)
#context.use_privatekey_file('infocommsociety.com.key')
#context.use_certificate_file('infocommsociety.com.crt')
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('cert1.pem', 'privkey1.pem')
app = Flask(__name__)

@app.route("/<query>")
def main(query):
    return "You ask for " + query


if __name__ == '__main__':
    CORS(app)
    app.run(debug=True,port=5000,host='0.0.0.0', ssl_context=context)