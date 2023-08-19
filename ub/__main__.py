from . import *
from log import LOGGER
import os
import sys
from importlib import util
import udB
import config
from telethon import events , Button
from astroid import manager
import astroid
import asyncio
import re
import time

logger=LOGGER('initialising')

start_time=time.time()

LOADED_MODULES={}
ADDONS={}

ultroid.start()
logger.info("Connected To DB Successfully !!!")
logger.info("Connecting The Bot !!!")
me=ultroid.get_entity("me")
logger.info(f"Connected Successfully As - {me.first_name} ({me.username}) !!!")
logger.info("————————————————————————————————————————————————————————————————————————————————")
logger.info("Starting To Load Modules !!!")
def thumbnail():
    x=udB.get_key('THUMB')
    if x==False:
        return "https://telegra.ph/file/9bb02a1a7420241a61e88.jpg"
    elif x=='False':
        return False
    else:
        return x
def ultroid_cmd(pattern, owner_only=False):
    def decorator(func):
        async def wrapper(event):
            if owner_only and not event.sender_id == config.OWNER:
                return
            await func(event)
        ptrn = rf'^[{re.escape(config.HNDLR)}]{pattern}'
        ultroid.on(events.NewMessage(pattern=ptrn))(wrapper)
        return wrapper
    return decorator
def time_formatter(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    hmm = len(time_list)
    for x in range(hmm):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += f"{time_list.pop()}, "
    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time
def load_plugin(path,addon=False):
    base_name=os.path.basename(path).replace("/",'.').replace("\\",'.').replace('.py','')
    if not addon: LOADED_MODULES[base_name]=path
    else: ADDONS[base_name]=path
    spec = util.spec_from_file_location(base_name, path)
    mod = util.module_from_spec(spec)
    mod.udB = udB
    mod.asst = ultroid
    mod.bot = ultroid
    mod.ultroid = ultroid
    mod.logger = LOGGER(base_name)
    mod.config = config
    mod.events=events
    mod.Button=Button
    mod.asyncio=asyncio
    mod.os=os
    mod.sys=sys
    mod.thumbnail=thumbnail
    mod.ultroid_cmd=ultroid_cmd
    mod.time_formatter=time_formatter
    mod.start_time=start_time
    mod.LOADED_MODULES=LOADED_MODULES
    mod.ADDONS=ADDONS
    mod.load_plugin=load_plugin
    mod.unload_plugin=unload_plugin
    spec.loader.exec_module(mod)
    
def unload_plugin(short_name,addon=False):
    if not addon: path=LOADED_MODULES[short_name]
    else: path=ADDONS[short_name]
    all_func=[]
    with open(path, 'r') as file:
        code = file.read()
    node=astroid.parse(code)
    for n in node.body:
        if isinstance(n, astroid.FunctionDef):
            all_func.append(n.name)
    try:
        for x, _ in ultroid.list_event_handlers():
                if x.__name__ in all_func:
                    ultroid.remove_event_handler(x)
    except (ValueError, KeyError):
        name = f"addons.{shortname}"
        for i in reversed(range(len(ultroid._event_builders))):
            ev, cb = ultroid._event_builders[i]
            if cb.__module__ == name:
                del ultroid._event_builders[i]
    if not addon: del LOADED_MODULES[short_name]
    else: del ADDONS[short_name]

plugin_paths = [os.path.join('plugins', filename) for filename in os.listdir('plugins') if os.path.isfile(os.path.join('plugins', filename))]
logger.info("Loading From Plugins Path !!!")
for i in plugin_paths:
    load_plugin(i)
    base_name=os.path.basename(i).replace('.py','')
    logger.info(f'• Loaded Official Plugin - {base_name} !!!')
logger.info("————————————————————————————————————————————————————————————————————————————————")

def iter_messages(chat_id , search=False , reverse=False):
    messages=[]
    msgid=1
    wrong=1
    while (wrong<=5):
        try:
            x=ultroid.get_messages(chat_id,ids=msgid)
            if x: 
                if not search: messages.append(x)
                else: 
                    if search in x.raw_text: messages.append(x)
            else: wrong+=1
        except Exception as e:
            print(e)
        msgid+=1
    if reverse: return list(reversed(messages))
    else: return messages

if udB.get_key('PLUGIN_CHANNEL'):
    logger.info("Loading From PLUGIN CHANNEL !!!")
    messages=iter_messages(udB.get_key('PLUGIN_CHANNEL'))
    for i in messages:
        if i.document and i.file.name.endswith('.py'):
            d_path=ultroid.download_media(i.media ,  file=f"addons/{i.file.name}")
            load_plugin(d_path)
            base_name=os.path.basename(d_path).replace('.py','')
            logger.info(f'• Loaded Addon - {base_name} !!!')
logger.info("————————————————————————————————————————————————————————————————————————————————")
if udB.get_key('DEPLOY_MSG'): ultroid.send_message(config.OWNER,f'''<b>ProUb Deployed Successfully Enjoy !!!
——————————————————
Master - <a href="tg://user?id={config.OWNER}">{ultroid.get_entity(config.OWNER).first_name}</a>
Assistant - <a href="tg://user?id={me.id}">{me.first_name} </a>
——————————————————
Official Support - @Mattt_Murdock</b>''',parse_mode='HTML',buttons=[[Button.url('Support','https://t.me/Mattt_Murdock')]])
logger.info("ProUb Deployed Successfully Enjoy !!!")
rst=udB.get_key("RESTART_MSG")
if rst: 
    ultroid.edit_message(rst['chat_id'],rst['msg_id'],"**__Restarted Succesfully !!!__**")
    udB.del_key('RESTART_MSG')
ultroid.run_until_disconnected()
