from encodings import utf_8
import encodings
from operator import le
from re import A, X
from PyPDF2 import PdfReader
from number import is_number
import os

def open_file(path):
    os.chdir(os.path.dirname(__file__))
    # Open PDF
    print(path)
    reader = PdfReader(path)
    text = ''
    
    # Extract page and tokenlize it
    lens = reader.numPages
    for i in range(lens):
        page = reader.pages[i]
        pagetext = page.extract_text()
        text = text + pagetext
    
    text = text[:text.find('Acknowledgment')-2]
    
    return text

def tokenlize_text(text):
    text_postokenlize = ''
    text_pointer = 0    
    while text_pointer < len(text)-1:
        if(text[text_pointer]==('\n' or '\r')):
            if is_number(text[text_pointer+1]):
                j = text_pointer + 1
                while(is_number(text[j])):
                    if j < len(text)-1:
                        j += 1            
                refindex = text[text_pointer+1:j]            
                text_postokenlize = text_postokenlize + ' ' # Add a space before the token
                text_postokenlize = text_postokenlize + refindex 
                text_postokenlize = text_postokenlize + '<ref>' # Add references token
                text_pointer = j
            else:
                text_postokenlize = text_postokenlize + ' ' # Normal enter/space will be replaced by black
                text_pointer += 1
        else:
            text_postokenlize = text_postokenlize + text[text_pointer]
            text_pointer += 1
            if(text[text_pointer]==('.' or ',')):
                text_postokenlize = text_postokenlize + '<sent>' # Add sentense token
                
    return text_postokenlize

def load_gluewords(path):
    os.chdir(os.path.dirname(__file__))
    glue_list = []
    with open(path) as pf:
        glue = pf.readline().split()
        glue_list += glue
        
    return glue_list

def reduce_references(text, gluewords):
    prgf_pointer = 0
    text_posprocess = ''

    while prgf_pointer < len(text):
        i = text.find('<ref>', prgf_pointer)
        refvalidity = True
        if i != -1:
            sentence = text[prgf_pointer: i]
            if(len(sentence)==0):
                break
            words = sentence.split()
            for prep in gluewords:
                if len(words) >= 2:
                    if words[-2] == prep:
                        text_posprocess = text_posprocess + sentence
                        refvalidity = False
                        break
            if refvalidity == True:
                text_posprocess = text_posprocess + sentence +'<ref>'
            else:
                refvalidity = True
            prgf_pointer = i + 5
        else:
            text_posprocess = text_posprocess + text[prgf_pointer: len(text)]
            prgf_pointer = len(text)
            
    return text_posprocess

def split_references(references):
# split paragraph into sentense 
    paragraph = references.split('<ref>') # split the references by token <ref>
    reference_list = {}

    for i in paragraph:
        
        sentense = [] 
        for j in i.split('.'):
            for k in j.split(','):
                sentense.append(k)
        if len(sentense) > 1:
            if is_number(sentense[-1]):
                reference_list[sentense[-2]] = sentense[-1].strip()     
            else:
                if is_number(sentense[-1].split()[-1].strip()):
                    reference_list[sentense[-1]] = sentense[-1].split()[-1].strip()
                    
    return reference_list

# please try this line of code to see the whole references dictionary of 'template.pdf'
# print(split_references(reduce_references(tokenlize_text(open_file('template.pdf')), load_gluewords('link-term.txt'))))