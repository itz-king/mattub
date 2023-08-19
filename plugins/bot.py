from telethon import __version__
from datetime import datetime
import time
import shutil

async def alive_def():
    owner=await ultroid.get_entity(config.OWNER)
    me=await ultroid.get_entity("me")
    pic=udB.get_key('ALIVE_PIC')
    uptime=time_formatter(int(time.time() - start_time))
    fmt=f'''<b>「 <a href="tg://user?id={me.id}">Pro Userbot</a> 」
My Master : <a href='tg://user?id={owner.id}'>{owner.first_name}</a>
Date : {datetime.now().strftime("%B %d, %Y")}
Telethon Version : {__version__}
Uptime : {uptime}</b>'''
    return "https://telegra.ph/file/651eef7ff3c0209dca8da.jpg" if not pic else pic , fmt

@ultroid_cmd(pattern="alive$",owner_only=True)
async def alive(event):
    pic , text = await alive_def()
    await event.reply(text , file=pic , parse_mode='HTML')

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
    os.execl(sys.executable, sys.executable, "-m ub")
