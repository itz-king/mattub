from pymongo import MongoClient
from config import DATABASE_URL

client=MongoClient(DATABASE_URL)
db=client['ub']
col=db['ub']

config_dict={}
record=col.find_one({'_id':'ub'})

async def sync_changes():
    col.update_one({'_id':'ub'},{'$set':config_dict},upsert=True)
    
if not record:
    config_dict['_id']="ub"
    sync_changes()
else:
    for i in record:
        if not i == '_id': config_dict[i]=record[i]

async def set_key(key , value):
    config_dict[key]=value
    await sync_changes()

async def get_key(key):
    value=config_dict[key]
    await sync_changes()
    return value

async def del_key(key):
    return del config_dict[key]

async def list_keys():
    keys=[]
    for i in config_dict:
        if i != '_id': keys.append(i)
    return keys