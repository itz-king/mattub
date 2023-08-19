from telethon import events , Button

@ultroid.on(events.NewMessage(pattern="^/start$"))
async def h(event):
    await event.reply('hello')