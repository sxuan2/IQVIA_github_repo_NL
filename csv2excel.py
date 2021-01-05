# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 02:09:41 2020

@author: sijian.xuan
"""


import pandas as pd
import os

mainDir = r"C:\Users\sijian.xuan\Desktop\local projects\Otezla\202003"


itemList = os.listdir(mainDir)
itemListLen = len(itemList)


fullLocationList=[]

for i in range(itemListLen):
    fullLocationList.append(os.path.join(mainDir, itemList[i]))


fullOutputList = fullLocationList.copy()

for i in range(itemListLen):
    fullOutputList[i] = fullOutputList[i].replace("csv","xlsx")


def csv2excel(file,outFile):
    
    data = pd.read_csv(file, encoding = "ISO-8859-1") 
    data.to_excel(outFile, index = False)
    

for i in range(itemListLen):
    csv2excel(fullLocationList[i],fullOutputList[i])
    

print("finished!")
    
    
    
#mainDir = r"X:\Data\Celgene\PLS\AIB_OTEZELA_adhoc_19_201912\Report"
    
#    
#    
#csv2excel(r"C:\Users\sijian.xuan\Desktop\otezlaOutput\1912\hospital_pack_info_share.csv",\
#          r"C:\Users\sijian.xuan\Desktop\otezlaOutput\1912\hospital_pack_info_share.xlsx")
