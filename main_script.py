import requests
from bs4 import BeautifulSoup
import re
import pymongo
from Data_fetching_functions import *
from Database import TryDatabase
from Online_Search import *
from typing import Mapping 
import sys

collection=""
#  -(U/L) -----(5 digits) --(char A-Z) ----(4 digits) ---(3 char(A-Z)) ------(6 digits)      CIN
#2nd pattern     ---(char(A-Z)) -(hypen) ----(4 digits)        LLPIN 
#3rd pattern    F -----(5 digits)    FCRN
def getCompanyId()  :
    #re stands for regular expression and number is denoting type of re
    re1=r"^[UL][0-9]{5}[A-Z]{2}[0-9]{4}[A-Z]{3}[0-9]{6}$" 
    # re2=r"^L[0-9]{5}[A-Z]{2}[0-9]{4}[A-Z]{3}[0-9]{6}$"
    re3=r"^[A-Z]{3}-[0-9]{4}$"
    re4=r"^F[0-9]{5}$"
    CIN=sys.argv[1]
    result=re.match(re1,CIN) or re.match(re3,CIN) or re.match(re4,CIN)
    if result:
        print('Pls wait...fetching your data')
        return CIN
    else:
        return None
        

# if __name__== '__main__':
    # global collection
# CreateDatabase()
argumentList = sys.argv
CIN=getCompanyId()
if CIN==None:
    print('Entered ID is invalid')
else :
    data=TryDatabase(CIN)
    if data==None:
        data=SearchOnline(CIN)
    if data==None:
        data="Company data is not available"
    else:
        print("Available in Database")
        
    print(data)
    

