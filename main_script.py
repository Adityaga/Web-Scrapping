import re
import pymongo
from Database import TryDatabase
from Online_Search import SearchOnline
from typing import Mapping 
import sys
from flask import Flask
from flask.templating import render_template
from flask_pymongo import PyMongo, pymongo
from bson.json_util import CANONICAL_JSON_OPTIONS, dumps
from bson.objectid import ObjectId
from flask import jsonify
from flask import request

app=Flask(__name__)
app.config["MONGO_URI"]="mongodb://localhost:27017/MCA_data"
mongo = PyMongo(app)
data=""

@app.route("/")
def home_page():
    return "HomePage"




@app.route('/CIN',methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        cin_num=request.form.get("name")
        CIN=varifyCompanyId(cin_num)
        if CIN==None:
            return 'Entered ID is invalid'
        else :
            global data
            data=TryDatabase(CIN)
            if data==None:
                data=SearchOnline(CIN)
                print("hello ",data)
            if data==None:
                data="Company data is not available"
            # print(data['Company/LLP Master Data'])
            var1=data['Company/LLP Master Data']
          
            return render_template("Table1.html",rows=var1) 
            # return jsonify(data)
    return render_template("index.html")



def varifyCompanyId(CIN)  :
    #re stands for regular expression and number is denoting type of re
    re1=r"^[UL][0-9]{5}[A-Z]{2}[0-9]{4}[A-Z]{3}[0-9]{6}$" 
    # re2=r"^L[0-9]{5}[A-Z]{2}[0-9]{4}[A-Z]{3}[0-9]{6}$"
    re3=r"^[A-Z]{3}-[0-9]{4}$"
    re4=r"^F[0-9]{5}$"
    # CIN=sys.argv[1]
    result=re.match(re1,CIN) or re.match(re3,CIN) or re.match(re4,CIN)
    if result:
        print('Pls wait...fetching your data')
        return CIN
    else:
        return None



@app.route("/Table", methods=['GET','POST'])
def Table2():
    data2=data["Charges"]
    return render_template("Table2.html",headings=data2[0],rows=data2)

@app.route("/button", methods=['GET','POST'])    
def button():
    if request.method == 'POST':
        global data
        if request.form.get('action2'):
            data2=data["Directors/Signatory Details"]
            return render_template("Table2.html",headings=data2[0],rows=data2)
        elif request.form.get('action1'):
            var1=data['Company/LLP Master Data']
            return render_template("Table1.html",rows=var1) 
        
            
    
    



if __name__== '__main__':
    app.run(debug=True)
    

