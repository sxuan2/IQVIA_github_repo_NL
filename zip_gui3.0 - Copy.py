# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 10:22:01 2020

@author: Sijian Xuan, CCHANG
"""


import tkinter as tk
from tkinter import *
from tkinter import ttk
import zipfile
import os
import shutil
import datetime

def get_time(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)



def compress_dir(dirname,zip_directory = "N",delete = "N"):


#   zip a directory directly
   
    if zip_directory == "Y":
        print("Zipping the whole folder: {}".format(os.getcwd()))
        file_path = dirname
        os.chdir('\\'.join(file_path.split('\\')[:-1]))
        zipfilename = os.path.basename(file_path)+"_folder_archive"
        shutil.make_archive(zipfilename, 'zip', file_path)

       
            
        
    
#    zip a file directly
    
    elif os.path.isfile(dirname):
        
        file_path = dirname # file_path, dirname is full location
        zipfilename = '_'.join(os.path.basename(dirname).split('.')) # use "_" to replace "."
        dirname2 = '-'.join(('-'.join(str(get_time(os.stat(file_path).st_mtime))[:19].split(':'))).split(' '))
        
        
        if os.path.exists(zipfilename + "_" + dirname2 + '.zip'):
            print("{} has already been zipped, so skip it.".format(zipfilename + "_" + dirname2 + '.zip'))
        
        else:
            print("{} will zip....".format(dirname))  
       
            zipfile_file = os.path.basename(file_path)
            print('Zipping {} ...'.format(dirname))
            os.chdir('\\'.join(file_path.split('\\')[:-1]))
            with zipfile.ZipFile(zipfilename + "_" + dirname2 + '.zip','w',zipfile.ZIP_DEFLATED) as f:
                f.write(zipfile_file)
                f.close()
            print('{} zipped successfully!'.format(zipfilename))
            
            if delete == "Y":
                print("Deleting {} ...".format(dirname))
                os.remove(dirname)
                print(dirname +" deleted")
            


#    zip all files under the directory
#    folders not included
#    zip file should be skipped
        
    else:        
        os.chdir('\\'.join(dirname.split('\\')))
        for file in os.listdir(dirname): # dirname is full location
            file_path = os.path.join(dirname, file) # file_path is full location + file name
            
            if os.path.isfile(file_path):
                if (file_path.split('.')[-1] == "zip"):
                    # print(file + " is already a zip file, will be skipped!!")
                    continue
                
                else:
                    zipfilename = '_'.join(os.path.basename(file_path).split('.'))# use "_" to replace "."
                    dirname2 = '-'.join(('-'.join(str(get_time(os.stat(file_path).st_mtime))[:19].split(':'))).split(' '))
                    zipfile_file = os.path.basename(file_path)
                    
                    if os.path.exists(zipfilename + "_" + dirname2 + '.zip'):
                        print("{} has already been zipped, so skip it.".format(zipfilename + "_" + dirname2 + '.zip'))
                    
                    else:
                        print('Zipping ' + zipfilename +' ...')
                        
                        with zipfile.ZipFile(zipfilename + "_" + dirname2 + '.zip','w',zipfile.ZIP_DEFLATED) as f:
                            f.write(zipfile_file)
                            f.close()
                        print('{} Zipped!'.format(zipfilename))
    
                        if delete == "Y":
                            print("Deleting " + file +" ...")
                            os.remove(file)
                            print(file +" deleted")
            else:
                continue
            
    print("All tasks fininshed!")
                 



def retrieve_input():
    input_text = zip_loc.get("1.0",END)
    input_title_cofirm.config(text=input_text.rstrip())
    print(repr(input_text.rstrip()))



root = tk.Tk()
ft = ('Calibri', 18, 'bold')
root.title('FileZipper')
input_title = Label(root, text="ZIP location", font = ft)
input_title_cofirm = Label(root, text="None", font = ft)
zip_loc= tk.Text(root, height=1, width=30)
zip_loc.insert(tk.END, "Please paste your adress here")
#adress = zip_loc.get("1.0",END)
confirm = Button(root, text="OK", command=retrieve_input, font = ft)

zip_in_folder = Label(root, text="Zip whole folder?", font = ft)
folder_zip = ttk.Combobox(root,values = ['N','Y'])

delete_after_zip = Label(root, text="Delete the file after zip?", font = ft)
folder_zip2 = ttk.Combobox(root,values = ['N','Y'])

folder_zip.current(0)
folder_zip2.current(0)
exec_zip = Button(root, text="GO!", font = ft, command=lambda : compress_dir(zip_loc.get("1.0",END).rstrip(),folder_zip.get(),folder_zip2.get()))



input_title.grid(row=0, column=0)
zip_loc.grid(row=0, column=1)
confirm.grid(row=0, column=4)
input_title_cofirm.grid(row=1, column=1)

zip_in_folder.grid(row=3, column=0)
folder_zip.grid(row=3, column=1)

delete_after_zip.grid(row=5, column=0)
folder_zip2.grid(row=5, column=1)

exec_zip.grid(row=3, column=4)
tk.mainloop()

