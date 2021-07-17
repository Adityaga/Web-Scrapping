from typing import Mapping
from pymongo import collection
import requests
from bs4 import BeautifulSoup
import re
import pymongo


#  -(U/L) -----(5 digits) --(char A-Z) ----(4 digits) ---(3 char(A-Z)) ------(6 digits)      CIN
#2nd pattern     ---(char(A-Z)) -(hypen) ----(4 digits)        LLPIN 
#3rd pattern    F -----(5 digits)    FCRN
def getCompanyId()  :
    #re stands for regular expression and number is denoting type of re
    re1=r"^U[0-9]{5}[A-Z]{2}[0-9]{4}[A-Z]{3}[0-9]{6}$" 
    re2=r"^L[0-9]{5}[A-Z]{2}[0-9]{4}[A-Z]{3}[0-9]{6}$"
    re3=r"^[A-Z]{3}-[0-9]{4}$"
    re4=r"^F[0-9]{5}$"
    CIN=input('Enter company Id')
    result=re.match(re1,CIN) or re.match(re2,CIN) or re.match(re3,CIN) or re.match(re4,CIN)
    if result:
        print('Pls wait...fetching your data')
        return CIN
    else:
        return None
def findTable1(page):
    soup=BeautifulSoup( page,'lxml')
    table_html=soup.find('table',{'id':'resultTab1'})
    rows=table_html.find_all('tr')
    table={}
    for row_i in rows:
        col=row_i.find_all('td')
        key=col[0].text
        val=col[1].text
        table[key]=val
    # print(table)
    return table

def findTable2(page):
    soup=BeautifulSoup( page,'lxml')
    table_html=soup.find('table',{'id':'resultTab5'})
    rows=table_html.find_all('tr')
    list1=[]
    table={}

    for i in rows:  
    #     print(i.text)
        row=i.text
        k=row.split('\n')
        k=[x for x in k if x != '']
    #     print(type(k))
        length=len(k)
        if(length==4):
            k.insert(0,"-")
        list1.append(k)
    #     print(j)

    table=[]
    lines=len(list1)
    for j in range(1,lines):
        dct={}
        for i in range(0,length):
            # print(i)
            dct[list1[0][i]]=list1[1][i]
        table.append(dct)

    return table
    
def findTable3(page):
    soup=BeautifulSoup( page,'lxml')
    table_html=soup.find("table",{'id':'resultTab6'})
    rows=table_html.find_all('tr')
# print(txt)
    list1=[]
    dct={}
    
    # print(len(txt.text[]))
    for i in rows:  
    #     print(i.text)
        row=i.text
        k=row.split('\n')
        k=[x for x in k if x != '']
    #     print(type(k))
        length=len(k)
        list1.append(k)
    #     print(j)
    #     j+=1  
    for i in range(1,len(list1)):
        list1[i].append('-')
    
    lst1=[]
    for i in range(1,len(list1)):
        dct={}
        for j in range(0,len(list1[0])):
            dct[list1[0][j]]=list1[i][j]
#         print(lst[i][j],end='')
#     print()
    lst1.append(dct)
    # print(dct)
    # print(lst1)
    return lst1


def SearchOnline(CIN,collection):
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
    table1=findTable1(page)
    table2=findTable2(page)
    # print("Table 3 finding")
    table3=findTable3(page)
    # print(table1)
    # print(table2)
    # print(table3)
    #storing in database
    # table2=""
    data=StoreInDatabase(CIN,table1,table2,table3,collection)
    return data
   
def StoreInDatabase(CIN,table1,table2,table3,collection):
    dictionary={'cin':CIN, 'Company/LLP Master Data' : table1, "Charges" : table2, "Directors/Signatory Details" : table3 }
    collection.insert_one(dictionary)
    print("Sucessfully inserted in database")
    return dictionary

def TryDatabase(CIN,collection):
    # print("TryDatabase intiated")
    data=collection.find_one({'cin':CIN})
    # print("Try database end")
    return data

def CreateDatabase():
    # print("Create database initiated")
    client=pymongo.MongoClient("mongodb://localhost:27017/")
    # print("successful")
    # print(client)
    db=client['MCA_data']
    collection = db['Available_Data_of_MCA']
    # print("Create Databse end")
    return collection

if __name__== '__main__':
    collection=CreateDatabase()
    CIN=getCompanyId()
    if CIN==None:
        print('Entered ID is invalid')
    else :
        # print("Pls wait, while we are fetchimg your data")
        data=TryDatabase(CIN,collection)
        if data==None:
            # print("inside if")
            data=SearchOnline(CIN,collection)
        else:
            print("Available in Database")
        print(data)
    

