import re
import pymongo
from Database import TryDatabase
from Online_Search import SearchOnline
from typing import Mapping 
import sys
from flask import Flask
from flask.templating import render_template
from flask_pymongo import PyMongo, pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify
from flask import request

app=Flask(__name__)
app.config["MONGO_URI"]="mongodb://localhost:27017/MCA_data"
mongo = PyMongo(app)
# CIN=""

@app.route("/")
def home_page():
    return "<p>Hello!</p>"

@app.route('/CIN/<id>')
def user(id):
    #id="U65999DL2016PLC304713"
    print(type(id))
    CIN=id
    CIN=getCompanyId(id)
    flag=1
    if CIN==None:
        print('Entered ID is invalid')
    else :
        data=TryDatabase(CIN)
        if data==None:
            data=SearchOnline(CIN)
            print("hello ",data)
        if data==None:
            data="Company data is not available"
        else:
            print("Available in Database")
            # flag=0
        print(data)

    # id="U74899DL1994PTC061340"
    print(CIN)
    print(type(CIN))
    user=mongo.db.Available_Data_of_MCA.find_one({'cin':id})
    response=dumps(user)
    return response
#collection=""
#  -(U/L) -----(5 digits) --(char A-Z) ----(4 digits) ---(3 char(A-Z)) ------(6 digits)      CIN
#2nd pattern     ---(char(A-Z)) -(hypen) ----(4 digits)        LLPIN 
#3rd pattern    F -----(5 digits)    FCRN


def getCompanyId(CIN)  :
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


if __name__== '__main__':
    app.run(debug=True)
    

