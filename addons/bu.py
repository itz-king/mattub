from telethon import events , Button

@ultroid.on(events.NewMessage(pattern="^/help$"))
async def he(event):
    await event.reply('hello')