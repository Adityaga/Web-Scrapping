from main_script import *
from Database import *
import Data_fetching_functions

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
    table3=Data_fetching_functions.findTable3(soup)
    # print(table1)
    # print(table2)
    # print(table3)
    #storing in database
    # table2=""
    data=StoreInDatabase(CIN,table1,table2,table3)
    return data