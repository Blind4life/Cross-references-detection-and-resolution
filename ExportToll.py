from math import ceil
from tkinter.font import BOLD, ITALIC
from fpdf import FPDF
import os
from ReferenceAnalyzer import *


def export_report(result=[], information={}, filename=''):
    os.chdir(os.path.dirname(__file__))
    pdf=FPDF()
    pdf.add_page() 
    pdf.set_xy(0,0)
    pdf.set_font('times', 'B', size=12)
    pdf.cell(70,10,'',0,2,'C')
    pdf.cell(60)
    pdf.cell(70,10,'Report',0,2,'C')
    pdf.set_font('times', '', size=9)
    pdf.cell(70,10,'',0,2,'C')
    pdf.cell(-30)
    pdf.cell(60, 10, "PDF name : ", border=0, ln=0, align='C',fill=False)
    pdf.cell(10, 10, filename, border=0, ln=0, align='C',fill=False)
    pdf.ln()
    pdf.cell(20)    
    pdf.cell(60, 10, "Detected/Total References : ", border=0, ln=0, align='C',fill=False)
    dtRef = str(result[1]) + '/' + str(result[0])
    pdf.cell(10, 10, dtRef, border=0, ln=0, align='C',fill=False)
    pdf.ln()
    pdf.cell(20)
    pdf.cell(60, 10, "Valid References : ", border=0, ln=0, align='C',fill=False)
    pdf.cell(10, 10, str(result[2]), border=0, ln=0, align='C',fill=False)
    pdf.ln()
    pdf.cell(20)
    pdf.cell(60, 10, "Invalid References : ", border=0, ln=0, align='C',fill=False)
    pdf.cell(10, 10, str(result[3]), border=0, ln=0, align='C',fill=False)
    pdf.ln()
    pdf.set_font('times', 'B', size=10)
    pdf.cell(-20)
    pdf.cell(70,10,'',0,2,'C')
    pdf.cell(70,10,'Details:',0,2,'C')
    pdf.set_font('times', 'B', size=7)
    pdf.cell(25)
    pdf.cell(7, 7, "Index", border=1, ln=0, align='C',fill=False)
    pdf.cell(20, 7, "Authur", border=1, ln=0, align='C',fill=False)
    pdf.cell(30, 7, "Journal", border=1, ln=0, align='C',fill=False)
    pdf.cell(15, 7, "Year", border=1, ln=0, align='C',fill=False)
    pdf.cell(15, 7, "Vol ", border=1, ln=0, align='C',fill=False)
    pdf.cell(20, 7, "Pages", border=1, ln=0, align='C',fill=False)
    pdf.cell(70, 7, "More", border=1, ln=0, align='C',fill=False)
    
    for index in information.keys():
        pdf.ln()
        pdf.cell(5)
        pdf.cell(7, 7, index, border=1, ln=0, align='C',fill=False)
        idict = information[index]
        if 'authur' in idict.keys():
            pdf.cell(20, 7, idict['authur'][0], border=1, ln=0, align='C',fill=False)
        else:
            pdf.cell(20, 7, '-', border=1, ln=0, align='C',fill=False)
        if 'journal' in idict.keys():
            pdf.cell(30, 7, idict['journal'], border=1, ln=0, align='C',fill=False)
        else:
            pdf.cell(30, 7, '-', border=1, ln=0, align='C',fill=False)
        if 'year' in idict.keys():
            pdf.cell(15, 7, idict['year'], border=1, ln=0, align='C',fill=False)
        else:
            pdf.cell(15, 7, '-', border=1, ln=0, align='C',fill=False)
        if 'vol' in idict.keys():
            pdf.cell(15, 7, idict['vol'], border=1, ln=0, align='C',fill=False)
        else:
            pdf.cell(15, 7, '-', border=1, ln=0, align='C',fill=False)
        if 'pages' in idict.keys():
            pdf.cell(20, 7, idict['pages'], border=1, ln=0, align='C',fill=False)
        else:
            pdf.cell(20, 7, '-', border=1, ln=0, align='C',fill=False)
        if 'statement' in idict.keys():
            more =  idict['statement']
            if len(more) > 65:
                pdf.cell(70, 7, more[:65]+'...', border=1, ln=0, align='C',fill=False)
            else:
                pdf.cell(70, 7, more, border=1, ln=0, align='C',fill=False)
        else:
            pdf.cell(70, 7, '-', border=1, ln=0, align='C',fill=False)
    
    pdf.output(filename[:filename.find('.')]+'-report.pdf', 'F')
    
def export(path, filename):
    export_report(predict_result(training_data(path)), get_validref_details(training_data(path)), filename)

# path = 'papers\\123.pdf'
# export_report(predict_result(training_data(path)), get_validref_details(training_data(path)))

