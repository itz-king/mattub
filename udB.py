from pymongo import MongoClient
from config import DATABASE_URL

client=MongoClient(DATABASE_URL)
db=client['ub']
col=db['ub']

config_dict={}
record=col.find_one({'_id':'ub'})

def sync_changes():
    col.update_one({'_id':'ub'},{'$set':config_dict},upsert=True)
    
if not record:
    config_dict['_id']="ub"
    sync_changes()
else:
    for i in record:
        if not i == '_id': config_dict[i]=record[i]

def set_key(key, value):
        try:
            config_dict[key] = value
            sync_changes()
            return True
        except:
            return False

def get_key( key):
        try:
            value = config_dict[key]
            return value
        except:
            return False
    
def del_key( key):
        try:
            del config_dict[key]
            sync_changes()
            return True
        except:
            return False
    
def list_keys():
        try:
            keys = []
            for i in config_dict:
                if i != '_id':
                    keys.append(i)
            return keys
        except:
            return False