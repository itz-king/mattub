_doc_='''• `/addsudo <reply or id or name>` - Add Sudo To A Person

• `/delsudo <reply or id or name>` - Remove Sudo Of A Person

• `/listsudo` - List All Sudo Users'''

@ultroid_cmd(pattern="addsudo ?(.*)",owner_only=True)
async def addsudo(event):
    matchs=event.pattern_match.group(1)
    if not matchs and event.reply: return await event.reply(f"**Reply/Username/Id With Command !!!**")
    if matchs:
        try: chat=int(matchs)
        except: chat=(await ultroid.get_entity(matchs)).id
    elif event.reply:
        chat=(await event.get_reply_message()).sender_id
    chat_=await ultroid.get_entity(chat)
    x=udB.get_key('SUDO_LIST')
    if not x: udB.set_key('SUDO_LIST',[chat])
    if chat in x: return await event.reply(f"**Already A Sudo User !!!**")
    else: 
        x.append(chat)
        udB.set_key('SUDO_LIST',x)
    return await event.reply(f"<b>Added <a href='tg://user?id={chat_.id}'>{chat_.first_name}</a> As Sudo !!!</b>",parse_mode='HTML')

@ultroid_cmd(pattern="delsudo ?(.*)",owner_only=True)
async def delsudo(event):
    matchs=event.pattern_match.group(1)
    if not matchs and event.reply: return await event.reply(f"**Reply/Username/Id With Command !!!**")
    if matchs:
        try: chat=int(matchs)
        except: chat=(await ultroid.get_entity(matchs)).id
    elif event.reply:
        chat=(await event.get_reply_message()).sender_id
    chat_=await ultroid.get_entity(chat)
    x=udB.get_key('SUDO_LIST')
    if not chat in x: return await event.reply(f"**Not A Sudo User !!!**")
    x.remove(chat)
    udB.set_key('SUDO_LIST',x)
    return await event.reply(f"<b>Removed <a href='tg://user?id={chat_.id}'>{chat_.first_name}</a> As Sudo !!!</b>",parse_mode='HTML')

@ultroid_cmd(pattern="listsudo",sudo_also=True)
async def listsudo(event):
    x=udB.get_key('SUDO_LIST')
    if not x: return await event.reply(f"**No Sudo Users !!!**")
    string=""
    for i in x:
        chat=await ultroid.get_entity(i)
        string+=f"• <a href='tg://user?id={chat.id}'>{chat.first_name}</a>\n"
    await event.reply(f"<b>List Of Sudo Users - \n{string.strip()}</b>",parse_mode='HTML')