import ast

_doc_='''• `/getdb <var>` - Get Var From DB

• `/setdb <var> <value>` - Set Var In DB

• `/deldb <var>` - Delete Var From DB

• `/listdb` - List All Vars From DB'''

@ultroid_cmd(pattern="getdb ?(.*)",owner_only=True)
async def getdb(event):
    matchs=event.pattern_match.group(1)
    if not matchs: return await event.reply(f"**Type Var Name Too !!!**")
    x=udB.get_key(matchs)
    if isinstance(x, int):
        tp= "Integer"
    elif isinstance(x, float):
        tp= "Float"
    elif isinstance(x, str):
        tp= "String"
    elif isinstance(x, list):
        tp= "List"
    elif isinstance(x, tuple):
        tp= "Tuple"
    elif isinstance(x, dict):
        tp= "Dictionary"
    elif isinstance(x, set):
        tp= "Set"
    elif isinstance(x, bool):
        tp= "Boolean"
    else:
        tp= "Unknown"
    if not x: return await event.reply(f"**No Var Named - `{matchs}` !!!**")
    await event.reply(f'''<b>Var Name - <code>{matchs}</code>
Value - <code>{x}</code>

Type - <code>{tp}</code></b>''',parse_mode='HTML')

@ultroid_cmd(pattern="setdb ?(.*)",owner_only=True)
async def setdb(event):
    matchs=event.pattern_match.group(1)
    if not matchs: return await event.reply(f"**Type Var Name Too !!!**")
    try: key , x=matchs.split()
    except: return await event.reply(f"**Type Key & Value Seperated By Space !!!**")
    try:
        x=ast.literal_eval(x)
    except (ValueError, SyntaxError):
        x=x
    udB.set_key(key,x)
    if isinstance(x, int):
        tp= "Integer"
    elif isinstance(x, float):
        tp= "Float"
    elif isinstance(x, str):
        tp= "String"
    elif isinstance(x, list):
        tp= "List"
    elif isinstance(x, tuple):
        tp= "Tuple"
    elif isinstance(x, dict):
        tp= "Dictionary"
    elif isinstance(x, set):
        tp= "Set"
    elif isinstance(x, bool):
        tp= "Boolean"
    else:
        tp= "Unknown"
    await event.reply(f'''<b>Setted - <code>{matchs}</code>
Value - <code>{x}</code>

Type - <code>{tp}</code></b>''',parse_mode='HTML')

@ultroid_cmd(pattern="deldb ?(.*)",owner_only=True)
async def deldb(event):
    matchs=event.pattern_match.group(1)
    if not matchs: return await event.reply(f"**Type Var Name Too !!!**")
    x=udB.del_key(matchs)
    if x:
        return await event.reply(f"**Deleted Var - `{matchs}`**")
    else: return await event.reply(f"**No Var Named -   `{matchs}`**")

@ultroid_cmd(pattern="listdb",sudo_also=True)
async def listdb(event):
    x=udB.list_keys()
    string='</code>\n• <code>'.join(x)
    await event.reply(f"""<b>List Of Var -
• <code>{string}</code></b>""",parse_mode='HTML')