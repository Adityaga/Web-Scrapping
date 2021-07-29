from Database import StoreInDatabase
import Data_fetching_functions
from bs4 import BeautifulSoup
import requests
import re

def varifyCompanyId(CIN)  :
    #re stands for regular expression and number is denoting type of re
    re1=r"^[UL][0-9]{5}[A-Z]{2}[0-9]{4}[A-Z]{3}[0-9]{6}$"
    re3=r"^[A-Z]{3}-[0-9]{4}$"
    re4=r"^F[0-9]{5}$"
    result=re.match(re1,CIN) or re.match(re3,CIN) or re.match(re4,CIN)
    if result:
        return CIN
    else:
        return None

def SearchOnline(CIN):
    url='https://www.mca.gov.in/mcafoportal/companyLLPMasterData.do'
    headers={
    # 'Cookie': 'HttpOnly; alertPopup=true; JSESSIONID=0000cI8109c7VgkjvKerNbkZdy3:1aevggkab'
    'Host': 'www.mca.gov.in',
    'Origin': 'https://www.mca.gov.in',
    'Referer': 'https://www.mca.gov.in/mcafoportal/viewCompanyMasterData.do',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'
    }
    data={
    'companyName':None ,
    'companyID': CIN,
    'displayCaptcha': False,
    'userEnteredCaptcha': None
    }
    session=requests.session()
    y=session.post(url=url,data=data,headers=headers)
    page=y.content
    # print(page)
    # print("before online search")
    soup=BeautifulSoup( page,'lxml')
    table1=Data_fetching_functions.findTable1(soup)
    if table1==None:
        return None
    table2=Data_fetching_functions.findTable2(soup)
    # print("Table 3 finding")
    table3=Data_fetching_functions.findTable2(soup,'resultTab6')
    # print(table1)
    # print(table2)
    # print(table3)
    #storing in database
    # table2=""
    data=StoreInDatabase(CIN,table1,table2,table3)
    return data