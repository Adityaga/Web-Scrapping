import pymongo
from pymongo import collection
def fun():
    client=pymongo.MongoClient("mongodb://localhost:27017/")
    print("successful")
    print(client)
    db=client['MCA_data']
    collection = db['Available_Data_of_MCA']
    return collection

if __name__=="__main__":
    collection=fun()
    item=collection.find_one({'cid':'1234'})
    # print(item)
    if item==None:
        print('Not Available')
