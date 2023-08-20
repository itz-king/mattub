from telethon import __version__
from datetime import datetime
import time
import shutil
from subprocess import run as srun
from asyncio import create_subprocess_exec, gather

_doc_='''• `/alive` - Check Alive

• `/ping` - Ping The Bot

• `/restart` - Restart The Bot

• `/update` - Update The Bot'''

@ultroid_cmd(pattern="alive$",owner_only=True)
async def alive(event):
    owner=await ultroid.get_entity(config.OWNER)
    me=await ultroid.get_entity("me")
    pic=udB.get_key('ALIVE_PIC')
    uptime=time_formatter(int(time.time() - start_time))
    fmt=f'''<b>「 <a href="tg://user?id={me.id}">Matt Userbot</a> 」
My Master : <a href='tg://user?id={owner.id}'>{owner.first_name}</a>
Date : {datetime.now().strftime("%B %d, %Y")}
Telethon Version : {__version__}
Uptime : {uptime}</b>'''
    pic="https://telegra.ph/file/651eef7ff3c0209dca8da.jpg" if not pic else pic
    await event.reply(fmt , file=pic , parse_mode='HTML')

@ultroid_cmd(pattern="ping$",owner_only=True)
async def ping(event):
    x=await event.reply("**Ping !**")
    start = time.time()
    x = await x.edit("**Pong !**")
    end = round((time.time() - start) * 1000)
    uptime=time_formatter(int(time.time() - start_time))
    await x.edit("**Pingtime : {}ms\nUptime : {}**".format(end, uptime))

@ultroid_cmd(pattern="restart$",owner_only=True)
async def restart(event):
    x=await event.reply("**__Restarting !!!__**")
    udB.set_key('RESTART_MSG',{'chat_id':event.chat_id,'msg_id':x.id})
    for i in ADDONS:
        unload_plugin(i)
    try: shutil.rmtree('addons')
    except: pass
    os.execl(sys.executable,sys.executable,'-B', "ub.py")

@ultroid_cmd(pattern="logs$",owner_only=True)
async def logs(event):
    await ultroid.send_file(event.chat_id,'ub.log',force_document=True,thumb='thumb.jpg',allow_cache=False,
    caption="**LOG File**",reply_to=event.id)

@ultroid_cmd(pattern="update$",owner_only=True)
async def update(event):
    x=await event.reply("**__Updating !!!__**")
    udB.set_key('RESTART_MSG',{'chat_id':event.chat_id,'msg_id':x.id})
    for i in ADDONS:
        unload_plugin(i)
    try: shutil.rmtree('addons')
    except: pass
    proc = await create_subprocess_exec("python3", "update.py")
    await gather(proc.wait())
    os.execl(sys.executable,sys.executable,'-B',"ub.py")