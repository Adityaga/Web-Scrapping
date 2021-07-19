from main_script import *
from Database import *
from Online_Search import *


def findTable1(soup):
    # soup=BeautifulSoup( page,'lxml')
    table_html=soup.find('table',{'id':'resultTab1'})
    if table_html==None:
        return None
    rows=table_html.find_all('tr')
    table={}
    for row_i in rows:
        col=row_i.find_all('td')
        key=col[0].text
        val=col[1].text
        table[key]=val
    # print(table)
    return table

def findTable2(soup,id='resultTab5'):
    results=soup.find('table',{'id':id})
    table={} 
    txt=results.find_all('tr')
    tags=results.find_all('th')
    row_data_html=[]
    table=[]

    # print(txt)
    flag=0
    for i in txt:
        lst=i.find_all('td')
        dct={}
        if flag==0:   # for avoiding first row which contains nothing
            flag=1
            continue
        if len(lst)==1:
            dct['Charges']="No Charges Exists for Company/LLP"
            table.append(dct)
            break
        for i in range(0,len(tags)):
            dct[tags[i].text]=lst[i].text
        table.append(dct)

    # print(table)
    return table
    
def findTable3(soup):
    return findTable2(soup,'resultTab6')