from pymongo import MongoClient

def connect(tb):
    try:
        client = MongoClient('localhost:27017')
        db = client['Tool_Check']
        tb = db[tb]
        return tb
    except Exception as e:
        print(e)
    finally:
        client.close()

def serviceByid(id):
    m_id = {'_id': id}
    tb = connect('Script')
    show_tb = tb.find_one(m_id)
    return show_tb

def serviceDelete(id):
    d_id = {'_id': id}
    tb = connect('Script')
    tb.delete_one(d_id)
def serviceUpdate(id,dt):
    d_id = {'_id': id}
    tb = connect('Script')
    tb.update_one(d_id,{'$set': dt},upsert=True)


def serviceAll():
    tb = connect('Script')
    show_tb = tb.find({})
    return show_tb


def serviceinsert(data):
    show = serviceByid(data['_id'])
    if(show == None):
        tb_demo2 = connect('Script')
        tb_demo2.insert_one(data)
        print("ok")

def findUser(user, pasword):
    u_id = {"_id": user,
            "password": pasword,
            "Status": "on"}
    tb = connect('user_login')
    show_tb = tb.find_one(u_id)
    return show_tb

def findUserAll():
    tb = connect('user_login')
    show_tb = tb.find({})
    return show_tb

def insertUser(data):
    u_id = {"_id": data["_id"]}
    tb = connect('user_login')
    show = tb.find_one(u_id)
    if(show == None):
        tb.insert_one(data)
        print("ok")

def UpdateUser(id,dt):
    myquery = id
    newvalues = { "$set": dt }
    tb = connect('user_login')
    tb.update_one(myquery, newvalues)

def deleteUser(id):
    tb = connect('user_login')
    u_id = {"_id": id}
    show = tb.find_one(u_id)
    if show["partition"] != "1":
        tb.delete_one(u_id)