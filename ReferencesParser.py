from csv import reader
from gettext import find
from PyPDF2 import PdfReader
from number import is_number
import string
import os

# reader = PdfReader("papers/123.pdf")

# page = reader.pages[-1]

# text_prepaser = page.extract_text()
# text_pointer = 0
# text_nospace = ''

# while text_pointer < len(text_prepaser):
#     if(text_prepaser[text_pointer]==('\n' or '\r')):
#         text_nospace = text_nospace + ' ' # replace /n or /r with ' '
#     else:
#         text_nospace = text_nospace + text_prepaser[text_pointer]
    
#     text_pointer += 1

# text_nospace = text_nospace[text_nospace.find('References')+11:]

def load_references(path):
    os.chdir(os.path.dirname(__file__))
    reader = PdfReader(path)
    page = reader.pages[-1]

    text_prepaser = page.extract_text()
    text_pointer = 0
    text_posparser = ''

    while text_pointer < len(text_prepaser):
        if(text_prepaser[text_pointer]==('\n' or '\r')):
            text_posparser = text_posparser + ' ' # replace /n or /r with ' '
        else:
            text_posparser = text_posparser + text_prepaser[text_pointer]
    
        text_pointer += 1

    text_posparser = text_posparser[text_posparser.find('References')+11:]
    
    return text_posparser

def find_bracket(str):
    sp = 0
    while sp < len(str)-1:
        if str[sp] == '(':
            if is_number(str[sp+1]):
                i = sp + 1
                while i<len(str)-1:
                    if is_number(str[i]):
                        i += 1
                    else:
                        break
                index = str[sp+1: i]
                if str[i] == ')' :
                    if int(index) == 0:
                        return [-1, -1, -1]
                    return [sp, i+1, int(index)]
                else:
                    sp += 1
            else:
                sp += 1
        else:
            sp += 1
    return [-1, -1, -1]

# str1 = 'hellowor(10)'
# str2 = 'hello(000)'
# str3 = ''
# str4 = 'fawef('
# str5 = '()23123'
# str6 = '(a)2(3)1' # len = 8

# print(find_bracket(str1))
# print(find_bracket(str2))
# print(find_bracket(str3))
# print(find_bracket(str4))
# print(find_bracket(str5))
# print(find_bracket(str6))

def refences_split(paragraph):
    ref_dictionary = {}
    p = 0
    while p < len(paragraph):
        if find_bracket(paragraph[p:])[0] != -1:
            start = p + find_bracket(paragraph[p:])[1]
            end = start + find_bracket(paragraph[start: ])[0]
            if end < start:
                ref_content = paragraph[start: ]
            else:
                ref_content = paragraph[start: end]
            ref_dictionary[find_bracket(paragraph[p:])[2]] = ref_content
            if end < start:
                p = len(paragraph)
            else:
                p = end

    return ref_dictionary

# print(refences_split(load_references("template.pdf")))

def category_information(reference=''):
    reference = reference.strip()
    # Find the first stop word, if it is a comma, this ref start with a name, if it is a space, it start with a statement
    icma = reference.find(',')
    if icma == -1:
        return {'statement': reference}
    ispc = reference.find(' ')
    if icma < ispc:
        if reference[icma+1] != ' ':
            return {'statement': reference}
        rptr = 0
        authurs = []
        while rptr < len(reference):
            if reference[rptr:].find(';') != -1:
                authurs.append(reference[rptr:rptr+reference[rptr:].find(';')])
                rptr = rptr+reference[rptr:].find(';') + 2
            else:
                tmptr = rptr
                rptr = rptr + reference[rptr:].find('.') + 1
                authurs.append(reference[tmptr:rptr])
                tmptr = rptr
                rptr = len(reference)
        rptr = tmptr
        #-----------------------------------------------------
        # find authurs 
        
        tmpstr = reference[rptr:].strip()
        i = tmpstr.find(' ') + 1
        if is_number(tmpstr[i]):
            journal = tmpstr[:i].strip()
            rptr = rptr + i
        else:
            rptr = rptr + reference[rptr:].find('.') + 2
            while is_number(reference[rptr]) == False:
                rptr += 1
                # rptr = rptr + reference[rptr:].find('.') + 2        
            journal = reference[tmptr:rptr].strip()
        #-----------------------------------------------------
        # find journal name
        
        tmptr = rptr
        rptr = rptr + reference[rptr:].find(',')
        year = reference[tmptr:rptr].strip()
        rptr = rptr + 2
        tmptr = rptr
        rptr = rptr + reference[rptr:].find(',')
        vol = reference[tmptr:rptr].strip()
        rptr = rptr + 2
        tmptr = rptr
        rptr = rptr + reference[rptr:].find('.')
        pages = reference[tmptr:rptr].strip()
        dict = {}
        dict['authur'] = authurs
        dict['journal'] = journal
        dict['year'] = year
        dict['vol'] = vol
        dict['pages'] = pages
        return dict
    else:
        return {'statement': reference}

    
# dict = refences_split(load_references("papers/123.pdf"))
# print(category_information(dict[12]))
