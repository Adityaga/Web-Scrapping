from Database import StoreInDatabase
import Data_fetching_functions
from bs4 import BeautifulSoup
import requests
import re
import json

with open('config.json','r') as file_r:
    params=json.load(file_r)["params"]


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
    url=params["url"]
    headers={
    # 'Cookie': 'HttpOnly; alertPopup=true; JSESSIONID=0000cI8109c7VgkjvKerNbkZdy3:1aevggkab'
    'Host': params["Host"],
    'Origin': params["Origin"],
    'Referer': params["Referer"],
    'User-Agent': params["User-Agent"]
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
    soup=BeautifulSoup( page,'lxml')
    table1=Data_fetching_functions.findTable1(soup)
    if table1==None:
        return None
    table2=Data_fetching_functions.findTable2(soup)
    table3=Data_fetching_functions.findTable2(soup,'resultTab6')
    data=StoreInDatabase(CIN,table1,table2,table3)
    return data