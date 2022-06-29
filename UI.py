from distutils.command.config import config
from turtle import width
from ReferenceAnalyzer import *
from asyncio.windows_events import NULL
from cProfile import label
from distutils.cmd import Command
from email import header, message
from email.mime import image
from fileinput import filename
from re import L, M
from tkinter.font import BOLD, NORMAL
from PyPDF2 import PdfReader
from tkinter import ACTIVE, BOTH, CENTER, DISABLED, LEFT, N, RIGHT, TOP, VERTICAL, Y, ttk
from ExportToll import *

import tkinter as tk
from tkinter import filedialog as fd
import tkinter
from tkinter.messagebox import showinfo
from DatabaseManager import *

root = tk.Tk()
root.geometry('900x500')
root.title('Detection and Resolution of Chemistry References')
root.resizable(False, False)

home_page = tk.Frame(root)
home_page.pack(side=TOP, anchor=CENTER)
database_page = tk.Frame(root)
result_page = tk.Frame(root)
details_page = tk.Frame(root)
details_page_btnframe = tk.Frame(root)

labletext = tkinter.StringVar(home_page)
fpath = tkinter.StringVar(home_page)

os.chdir(os.path.dirname(__file__))

def select_file():
    type = (('PDF files', '*.pdf'),)    
    f_name = fd.askopenfilename(title = 'Open', initialdir = '/', filetypes = type)
    if f_name == '':
        showinfo(title = 'Open a PDF', message = 'No file selected!')
        return
    showinfo(title = 'Open a PDF', message = f_name)
    labletext.set(f_name)
    fpath.set(f_name.replace("/", "\\"))
    active_btn()    
def home_to_db():
    home_page.pack_forget()    
    dbpage_treeframe.pack(side=TOP, anchor=N)
    database_page.pack(side=TOP, anchor=CENTER)
    disable_db_btn()
    doclist = read_data()
    index = 0
    for i in dbtree.get_children():
        dbtree.delete(i)
    for i in doclist:
        dbtree.insert('', index+1, values=
                       (index+1, i['authur'], i['journal'], i['year'], i['vol'], i['pages'], i['statement'])
                       )
        index += 1
def home_to_rst():
    home_page.pack_forget()
    result_page.pack(side=TOP, anchor=CENTER, expand=True, padx=100, pady=30)
    disable_db_btn()
def db_to_home():
    database_page.pack_forget()
    dbpage_treeframe.pack_forget()
    home_page.pack()
    active_db_btn()
def rst_to_dtls():
    result_page.pack_forget()
    details_page.pack(side=TOP, anchor=N)
    tree_frame.pack(side=TOP, anchor=N)
    details_page_btnframe.pack(side=TOP, anchor=N)
    doclist = add_keys(get_validref_details(training_data(fpath.get())))
    index = 0
    for i in detailsview.get_children():
        detailsview.delete(i)
    for i in doclist:
        detailsview.insert('', index+1, values=
                       (index+1, i['authur'], i['journal'], i['year'], i['vol'], i['pages'], i['statement'])
                       )
        index += 1
def disable_db_btn():
    navagator.entryconfig(2, state=DISABLED)
def active_db_btn():
    navagator.entryconfig(2, state=ACTIVE)
def active_btn():
    filemenue.entryconfig(1, state=ACTIVE)
    predict_btn['state'] = ACTIVE    
def predict():
    home_to_rst()
    filename = labletext.get().split('/')[-1]
    PdfName.set(filename)
    rst =  predict_result(training_data(fpath.get()))
    dectedinall = str(rst[1]) + '/' + str(rst[0])
    dtref.set(dectedinall)
    vref.set(str(rst[2]))
    inref.set(str(rst[3]))
def svtodb():
    doclist = add_keys(get_validref_details(training_data(fpath.get())))
    insert_data(doclist)
def generate_report():
    export(fpath.get(), labletext.get().split('/')[-1])
    showinfo(title = 'Export report', message = 'Report generated at ' + os.path.dirname(__file__)+'\\report.pdf')
def details_to_home():
    details_page.pack_forget()
    tree_frame.pack_forget()
    details_page_btnframe.pack_forget()
    home_page.pack(side=TOP, anchor=CENTER)
    active_db_btn()

# navagator
navagator = tk.Menu(root)
filemenue =tk.Menu(navagator, tearoff=False)
filemenue.add_command(label='Open', command=select_file)
file_export = filemenue.add_command(label='Export', state=DISABLED, command=generate_report)
filemenue.add_separator()
filemenue.add_command(label='Exit', command=root.destroy)
navagator.add_cascade(label='File', menu=filemenue)
databasemenu = tk.Menu(navagator, tearoff=False)
navagator.add_command(label='Database', command=home_to_db)
navagator.add_command(label='Introduction')
navagator.add_command(label='More')
root.config(menu=navagator)

# database pagge widget
dbpage_treeframe = tk.Frame(root, pady=50)
columns = ('id', 'Authurs', 'Journal', 'Year', 'Vol', 'Pages', 'Ohter')
headers = ('#', 'Authurs', 'Journal', 'Year', 'Vol', 'Pages', 'Ohter')
column_width = (30, 70, 120, 50, 50, 100, 200)
dtscroll = tk.Scrollbar(dbpage_treeframe, orient=VERTICAL)
dtscroll.pack(side=RIGHT, fill=Y)
dbtree = ttk.Treeview(dbpage_treeframe, show='headings', columns=columns, yscrollcommand=dtscroll.set)
for (c, cw, h) in zip(columns, column_width, headers):
    dbtree.column(c, width=cw, anchor='w')
    dbtree.heading(c, text=h)
dbtree.pack(side=LEFT)
dtscroll.config(command=dbtree.yview)
tk.Button(database_page, text='Back to home', command=db_to_home).pack()

#h homepage widget
app_icon = tk.PhotoImage(file='icon.gif')
icon = tk.Label(home_page, image=app_icon, padx=0, pady=20, borderwidth=0).grid(row=5,column=1, rowspan=2, pady=130)
tk.Button(home_page, command=select_file, text='Open').grid(row=6, column=2)
tk.Entry(home_page, textvariable=labletext, font=24).grid(row=6, column=1,padx=10)
predict_btn =  tk.Button(home_page, command=predict, text='Analyze', state=DISABLED)
predict_btn.grid(row=7, column=1)

# result page widget
PdfName = tk.StringVar(result_page)
dtref = tk.StringVar(result_page)
vref = tk.StringVar(result_page)
inref = tk.StringVar(result_page)
tk.Label(result_page, text='References detection and resolution results', font=5, height=3).grid(row=2, column=1, columnspan=3)
tk.Label(result_page, text='File name: ', height=3).grid(row=3, column=1)
tk.Label(result_page, textvariable=PdfName, height=3).grid(row=3, column=3)
tk.Label(result_page, text='Detected/toal references :', height=3).grid(row=4, column=1)
tk.Label(result_page, textvariable=dtref, height=3).grid(row=4, column=3)
tk.Label(result_page, text='Valid references: ', height=3).grid(row=5, column=1)
tk.Label(result_page, textvariable=vref, height=3).grid(row=5, column=3)
tk.Label(result_page, text='Invalid references: ', height=3).grid(row=6, column=1)
tk.Label(result_page, textvariable=inref, height=3).grid(row=6, column=3)
tk.Button(result_page, text='Show details', pady=5, command=rst_to_dtls).grid(row=10, column=2, pady=5)

# details page widget
tk.Label(details_page, text='Resolution details', font=10, pady=20).pack(side=TOP, anchor=CENTER, expand=True)
tree_frame = tk.Frame(root)
columns = ('id', 'Authurs', 'Journal', 'Year', 'Vol', 'Pages', 'Ohter')
headers = ('#', 'Authurs', 'Journal', 'Year', 'Vol', 'Pages', 'Ohter')
column_width = (30, 70, 120, 50, 50, 100, 200)
dtscroll = tk.Scrollbar(tree_frame, orient=VERTICAL)
dtscroll.pack(side=RIGHT, fill=Y)
detailsview = ttk.Treeview(tree_frame, show='headings', columns=columns, yscrollcommand=dtscroll.set)
for (c, cw, h) in zip(columns, column_width, headers):
    detailsview.column(c, width=cw, anchor='w')
    detailsview.heading(c, text=h)
detailsview.pack(side=LEFT)
dtscroll.config(command=detailsview.yview)
tk.Button(details_page_btnframe, text='Save to DB', pady=5, command=svtodb).pack(side=LEFT, anchor=CENTER)
tk.Button(details_page_btnframe, text='Back to home', pady=5, command=details_to_home).pack(side=RIGHT, anchor=CENTER)

root.mainloop()