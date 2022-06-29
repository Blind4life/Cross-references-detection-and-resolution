import os
import numpy as np
from collections import Counter
from sklearn.naive_bayes import *
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix

def remove_gluewords(path, dict={}):
    os.chdir(os.path.dirname(__file__))
    with open(path) as sf:
        glues = sf.readline().split()
    for sw in glues:
        if sw in dict:
            del dict[sw]
    return dict

def make_dictionary(directory_path):
    os.chdir(os.path.dirname(__file__))
    all_words = []
    filenames = os.listdir(directory_path)
    filepath_strs = []
    for fname in filenames:
        filepath_strs.append(directory_path+'\\'+fname)
    
    for fpstr in filepath_strs:
        with open(fpstr) as f:
            for i,line in enumerate(f):
                if i >= 1:
                    words = line.lower().split() 
                    all_words += words
                    
    dictionary = Counter(all_words)
    
    list_todel = dictionary.keys()
    
    for obj in list(list_todel):
        if obj.isalpha() == False or len(obj) == 1:
            del dictionary[obj]
            
    dictionary = remove_gluewords('glues.txt', dictionary)
    dictionary = dictionary.most_common(1000)
    return dictionary 

def extract_features(directory_path, dictionary):
    os.chdir(os.path.dirname(__file__))
    filenames = os.listdir(directory_path)
    filepath_strs = []
    for fname in filenames:
        filepath_strs.append(directory_path+'\\'+fname)
    
    ftmatrix = np.zeros((len(filepath_strs), 1000))
    txtID = 0
    for fil in filepath_strs:
        with open(fil) as f:
            for i,line in enumerate(f):
                if i >= 1:
                    words = line.split()
                    for word in words:
                        wordID = 0
                        for i,d in enumerate(dictionary):
                            if word == d[0]:
                                wordID = i
                                ftmatrix[txtID, wordID] = words.count(word)
            txtID += 1
    
    return ftmatrix
        
def extract_dict_features(references_dict, dictionary):
    # Change the working dir to current file path
    os.chdir(os.path.dirname(__file__))
    # Generate feature matrix
    ftmatrix = np.zeros((len(references_dict), 1000))
    refID = 0
    for key in references_dict.keys():
        words = key.split()
        for word in words:
            wordID = 0
            for i,d in enumerate(dictionary):
                # first element of the tuple is the word itself
                if word == d[0]:
                    wordID = i
                    ftmatrix[refID, wordID] = words.count(word)
        refID +=1
    
    return ftmatrix

# dictionary = make_dictionary('training-set\\full-training-dir')
# tm = extract_features('training-set\\full-training-dir', dictionary)
# print(tm)
