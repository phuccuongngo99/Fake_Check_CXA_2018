#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 09:14:48 2018

@author: root
"""
import time
import threading
from pyfasttext import FastText

text = 'Says the Annies List political group supports third-trimester abortions on demand.'


text = text
def fast_text(text):
    test_data = text.replace('\n',' ')
    model = FastText('./model_audit.bin')
    test = test_data+'\n'
    pred = model.predict_proba_single(test, k=2)
    
    out = pred[0][1]
    return out

start = time.time()
fast_text(text)
end = time.time()

print(end-start)