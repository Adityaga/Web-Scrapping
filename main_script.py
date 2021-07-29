from Database import TryDatabase
from Online_Search import SearchOnline, varifyCompanyId
from flask import Flask, request
from flask.templating import render_template
from flask_pymongo import PyMongo

app=Flask(__name__)
app.config["MONGO_URI"]="mongodb://localhost:27017/MCA_data"
mongo = PyMongo(app)

@app.route('/',methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        CIN=request.form.get("name")
        if varifyCompanyId(CIN)==False:
            data='Entered ID is invalid'
            return render_template("not_available.html",data=data)
        else :
            data=TryDatabase(CIN)
            if data==None:
                data=SearchOnline(CIN)
            if data==None:
                data="Company data is not available"
                return render_template("not_available.html",data=data)
            table1=data['Company/LLP Master Data']
            table2=data["Charges"]
            table3=data["Directors/Signatory Details"]
            return render_template("Table.html",table1=table1,headings2=table2[0],table2=table2,headings3=table3[0],table3=table3) 
    
    return render_template("index.html")



if __name__== '__main__':
    app.run(debug=True)
    

