from typing import Mapping
import requests
from bs4 import BeautifulSoup
import re
session=requests.session()

url='https://www.mca.gov.in/mcafoportal/companyLLPMasterData.do'
headers={
# 'Cookie': 'HttpOnly; alertPopup=true; JSESSIONID=0000cI8109c7VgkjvKerNbkZdy3:1aevggkab'
'Host': 'www.mca.gov.in',
'Origin': 'https://www.mca.gov.in',
'Referer': 'https://www.mca.gov.in/mcafoportal/viewCompanyMasterData.do',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'
}

#  -(U/L) -----(5 digits) --(char A-Z) ----(4 digits) ---(3 char(A-Z)) ------(6 digits)      CIN
#2nd pattern     ---(char(A-Z)) -(hypen) ----(4 digits)        LLPIN 
#3rd pattern    F -----(5 digits)    FCRN
def getCompanyId()  :
    #  -(U/L) -----(5 digits) --(char A-Z) ----(4 digits) ---(3 char(A-Z)) ------(6 digits)      CIN
#2nd pattern     ---(char(A-Z)) -(hypen) ----(4 digits)        LLPIN 
#3rd pattern    F -----(5 digits)    FCRN
    re1=r"^U[0-9]{5}[A-Z]{2}[0-9]{4}[A-Z]{3}[0-9]{6}$" 
    re2=r"^L[0-9]{5}[A-Z]{2}[0-9]{4}[A-Z]{3}[0-9]{6}$"
    re3=r"^[A-Z]{3}-[0-9]{4}$"
    re4=r"^F[0-9]{5}$"
    r=input('Enter company Id')
    result=re.match(re1,r) or re.match(re2,r) or re.match(re3,r) or re.match(re4,r)
    if result:
        print('Pls wait...fetching your data')
    else:
        print('Company Id invalid')
        return 

    
    data={
    'companyName':None ,
    'companyID': 'U74120MH2015PTC265316',
    'displayCaptcha': False,
    'userEnteredCaptcha': None
    }
    
    y=session.post(url=url,data=data,headers=headers)
    page=y.content
    # print(page)
    soup=BeautifulSoup( page,'lxml')
    var1=soup.find('table',{'id':'resultTab1'})
    var2=soup.find('table',{'id':'resultTab5'})
    var3=soup.find("table",{'id':'resultTab6'})
    rows1=var1.find_all('tr')
    rows2=var2.find_all('tr')
    rows3=var3.find_all('tr')
    dt1={}
    for row_i in rows1:
    #     print(row_i)
        col=row_i.find_all('td')
        key=col[0].text
        val=col[1].text
        dt1[key]=val
    print(dt1)

    list1=[]
    dt2={}

    # print(len(txt.text[]))
    for i in rows2:  
    #     print(i.text)
        row=i.text
        k=row.split('\n')
        k=[x for x in k if x != '']
    #     print(type(k))
        length=len(k)
        list1.append(k)
    #     print(j)
    #     j+=1
    for i in range(0,length):
        dt2[list1[0][i]]=list1[1][i]
        
    # print(list1)
    print(dt2)

    lst=[]
    dct=[]
    for i in rows3:
        row=i.text
    #     print(type(row)
        row=row.split('\n')
        list1=[x for x in row if x!='']
        lst.append(list1)
    #     print(row)
    # print(lst)
    # print(len(lst[0]))
    for i in range(1,len(lst)):
        lst[i].append('-')
    lst1=[]
    for i in range(1,len(lst)):
        dct={}
        for j in range(0,len(lst[0])):
            dct[lst[0][j]]=lst[i][j]
    #         print(lst[i][j],end='')
    #     print()
        lst1.append(dct)
    print(lst1) #data of table 3



if __name__== '__main__':
    getCompanyId()