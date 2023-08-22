from telethon import types , functions , errors
import asyncio
from datetime import datetime

_doc_='''• `/addapprove <id>` - Set Auto Approve Channel

• `/delappove <id>` - Delete Auto Approve Channel

• `/listapprove` - List All AutoApprove Channels'''

@ultroid.on(events.Raw(types.UpdateBotChatInviteRequester))
async def approver(event):
    app_lst=udB.get_key("APPROVE") if udB.get_key("APPROVE") else []
    chat=event.peer.channel_id
    chat=await ultroid.get_entity(chat)
    chatid= int('-100'+str(chat.id)) if chat.id>0 else chat.id
    if not chatid in app_lst: return
    who=await ultroid.get_entity(event.user_id)
    await ultroid(functions.messages.HideChatJoinRequestRequest(approved=True,peer=chat,user_id=event.user_id))
    await ultroid.send_message(event.user_id,f'''<b>Hey <a href="tg://user?id={who.id}">{who.first_name}</a> , Thanks For Join Our Channel {chat.title}.</b>''',
        parse_mode="HTML")

@ultroid_cmd(pattern="addapprove ?(.*)",sudo_also=True)
async def addapprove(event):
    matchs=event.pattern_match.group(1)
    if not matchs: return await event.reply(f"**Type Channel ID Also !!!**")
    app_lst=udB.get_key("APPROVE") if udB.get_key("APPROVE") else []
    matchs=int(matchs)
    app_lst.append(matchs)
    udB.set_key("APPROVE",app_lst)
    await event.reply(f"**Added Auto Approve Here - {matchs}**")

@ultroid_cmd(pattern="delapprove ?(.*)",sudo_also=True)
async def delapprove(event):
    matchs=event.pattern_match.group(1)
    if not matchs: return await event.reply(f"**Type Channel ID Also !!!**")
    app_lst=udB.get_key("APPROVE") if udB.get_key("APPROVE") else []
    matchs=int(matchs)
    if matchs not in app_lst: return await event.reply(f"**Not Auto Approved !!!**")
    app_lst.remove(matchs)
    udB.set_key("APPROVE",app_lst)
    await event.reply(f"**Deleted Auto Approve Here - {matchs}**")

@ultroid_cmd(pattern="listapprove ?(.*)",sudo_also=True)
async def listapprove(event):
    app_lst=udB.get_key("APPROVE") if udB.get_key("APPROVE") else []
    if not app_lst: return await event.reply(f"**No Auto Approve Channels !!!**")
    string=""
    for i in app_lst:
        string+=f"• <code>{i}</code>\n"
    await event.reply(f"""<b>List Of Auto Approved Channels -
{string}</b>""",parse_mode='HTML')