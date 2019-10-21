# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 16:05:06 2019

@author: cchang
"""


import tkinter as tk
from tkinter import *
import zipfile
import os
import shutil
from tkinter import ttk
import pprint


def compress_dir(dirname,zip_directory = "N"):
#    init
    #dirname = zip_loc.get("1.0",END).rstrip()
    try:
        print("Directory name:")
        print(os.getcwd())
        print("Zipping every file inside above directory (folder not included)...")
    except:
#         print("Must input a directory")
        raise NameError('Please input valid directory!!')
    



#   zip a directory directly
   
    if zip_directory == "Y":
        file_path = dirname
        os.chdir('\\'.join(dirname.split('\\')[:-1]))
        zipfilename = os.path.basename(dirname)+"_folder"
        shutil.make_archive(zipfilename, 'zip', file_path)
        
    
#    zip a file directly
    
    elif os.path.isfile(dirname):
        print("Directory is a file, it will be zipped immediately!!")
        os.chdir('\\'.join(dirname.split('\\')[:-1]))
        file_path = dirname
        zipfilename = '_'.join(os.path.basename(dirname).split('.'))
        zipfile.ZipFile(zipfilename + '.zip','w',zipfile.ZIP_DEFLATED).write(dirname)


#    zip all files under the directory
#    folders not included
        
    else:
        os.chdir(dirname)
        for file in os.listdir(dirname):
            file_path = os.path.join(dirname, file)
#            print(file_path)
            if os.path.isfile(file_path):
                if (file_path.split('.')[-1] == "zip"):
                    continue
                else:
                    zipfilename = '_'.join(os.path.basename(file_path).split('.'))+'.zip'
                    zipfile_file = os.path.basename(file_path)
                    
                    f = zipfile.ZipFile(zipfilename, 'w',zipfile.ZIP_DEFLATED)
                    print('Zipping ' + zipfilename +' ...')
                    f.write(zipfile_file)
                    f.close()
            else:
                continue
    print("Zip finish!!")           


def retrieve_input():
    input_text = zip_loc.get("1.0",END)
    input_title_cofirm.config(text=input_text.rstrip())
    print(repr(input_text.rstrip()))

root = tk.Tk()
ft = ('Calibri', 18, 'bold')
root.title('SICHANG ZIP')
input_title = Label(root, text="ZIP location", font = ft)
input_title_cofirm = Label(root, text="None", font = ft)
zip_loc= tk.Text(root, height=1, width=30)
zip_loc.insert(tk.END, "please paste your adress here")
#adress = zip_loc.get("1.0",END)
confirm = Button(root, text="OK", command=retrieve_input, font = ft)
zip_in_folder = Label(root, text="zip whole folder?", font = ft)
folder_zip = ttk.Combobox(root,values = ['N','Y'])
folder_zip.current(0)
exec_zip = Button(root, text="GO!", font = ft, command=lambda : compress_dir(zip_loc.get("1.0",END).rstrip(),folder_zip.get()))



input_title.grid(row=0, column=0)
zip_loc.grid(row=0, column=1)
confirm.grid(row=0, column=4)
input_title_cofirm.grid(row=1, column=1)
zip_in_folder.grid(row=3, column=0)
folder_zip.grid(row=3, column=1)
exec_zip.grid(row=3, column=4)
tk.mainloop()

