import imp
from sre_parse import TYPE_FLAGS
from typing import Type
from unittest import result
from ReferencesDetector import *
from SVMModel import *
from ReferencesParser import *
import os
import numpy as np
from collections import Counter
from sklearn.naive_bayes import *
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix
import string

# path = 'papers\\123.pdf'

def training_data(path):
    os.chdir(os.path.dirname(__file__))
    tagged_text = tokenlize_text(open_file(path))
    reduced_text = reduce_references(tagged_text, load_gluewords('link-term.txt'))
    references = split_references(reduced_text)
    dictionary = make_dictionary('training-set\\full-training-dir')
    tm = extract_dict_features(references, dictionary)
    train_lables = np.zeros(315)
    train_lables[163:315] = 1
    trainmartrix = extract_features('training-set\\full-training-dir', dictionary)
    LSVCModel = LinearSVC()
    LSVCModel.fit(trainmartrix, train_lables)
    result = LSVCModel.predict(tm)

    results_dict = {}
    for i, v in zip(range(len(result)), references.values()):
        if v in results_dict:
            if(results_dict[v]=='0'):
                results_dict[v] = result[i]
        else:
            results_dict[v] = result[i]        
    references_dict = refences_split(load_references(path))
    refer_result_dict = {}
    for refk in references_dict.keys():
        st = str(refk)
        if st in results_dict:
            refer_result_dict[references_dict[refk]] = ((st), results_dict[st])
        else:
            refer_result_dict[references_dict[refk]] = ((st), -1)
    return refer_result_dict

def predict_result(dict={}):
    total_refnum = len(dict)
    undetected_refnum = 0
    valid_refnum = 0
    invalid_refnum = 0
    for v in dict.values():
        if v[1] == -1:
            undetected_refnum += 1
        elif v[1] == 1:
            valid_refnum += 1
        else:
            invalid_refnum += 1
    detected_refnum = total_refnum - undetected_refnum
    return [total_refnum, detected_refnum, valid_refnum, invalid_refnum]
        
def get_validref_details(dict={}):
    details = {}
    for key in dict.keys():
        if dict[key][1] == 1:
            details[(dict[key])[0]] = category_information(key)
    
    return details

# print(predict_result(training_data(path)))
# print(get_validref_details(training_data(path)))
