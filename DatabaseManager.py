import pymongo as pm
from ReferenceAnalyzer import *

def add_keys(dict={}):
    doclist = []
    for i in dict.keys():
        doc = dict[i]
        doc_fullkeys = {}
        copy_data('authur', doc, doc_fullkeys)
        copy_data('journal', doc, doc_fullkeys)
        copy_data('year', doc, doc_fullkeys)
        copy_data('vol', doc, doc_fullkeys)
        copy_data('pages', doc, doc_fullkeys)
        copy_data('statement', doc, doc_fullkeys)
        doclist.append(doc_fullkeys)
    return doclist
        
def copy_data(str, source={}, target={}):
    if str in source.keys():
        target[str] = source[str]
    else:
        target[str] = '-'

def insert_data(datalist=[]):
    client = pm.MongoClient("mongodb://localhost:27017/")
    mydb = client["references"]
    mycol = mydb['reference_information']
    mycol.insert_many(datalist)
    
def read_data():
    client = pm.MongoClient("mongodb://localhost:27017/")
    mydb = client["references"]
    mycol = mydb['reference_information']
    doclist = []
    for i in mycol.find():
        doclist.append(i)
    return doclist
 
# insert_data(add_keys(get_validref_details(training_data('papers\\123.pdf'))))   