import pymongo

    # print("Create database initiated")
client=pymongo.MongoClient("mongodb://localhost:27017/")
    # print("successful")
    # print(client)
db=client['MCA_data']
collection = db['Available_Data_of_MCA']
    # print("Create Databse end")

def StoreInDatabase(CIN,table1,table2,table3):
    # global collection
    dictionary={'cin':CIN, 'Company/LLP Master Data' : table1, "Charges" : table2, "Directors/Signatory Details" : table3 }
    collection.insert_one(dictionary)
    print("Sucessfully inserted in database")
    return dictionary

def TryDatabase(CIN):
    # print("TryDatabase intiated")
    # global collection
    data=collection.find_one({'cin':CIN})
    # print("Try database end")
    return data