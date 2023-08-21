_doc_='''• `/sysinfo` - Get Info About System

• `/eval <code>` - Run Python Codes

• `/bash <command>` - Run Terminal Commands'''

import asyncio
import re
from io import BytesIO, StringIO
import traceback

async def bash(cmd, run_code=0):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    err = stderr.decode().strip() or None
    out = stdout.decode().strip()
    if not run_code and err:
        if match := re.match("\/bin\/sh: (.*): ?(\w+): not found", err):
            return out, f"{match.group(2).upper()}_NOT_FOUND"
    return out, err

async def aexec(code, event):
    exec(
        (
            "async def __aexec(e, client): "
            + "\n message = event = e"
            + "\n reply = await event.get_reply_message()"
            + "\n chat = event.chat_id"
        )
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](event, event.client)

@ultroid_cmd(pattern='sysinfo$',sudo_also=True)
async def sysinfo(event):
    xx=await event.reply('**Processing...**')
    x, y = await bash("neofetch|sed 's/\x1B\\[[0-9;\\?]*[a-zA-Z]//g' >> neo.txt")
    if y and y.endswith("NOT_FOUND"):
        return await xx.edit(f"Error: `{y}`")
    with open("neo.txt", "r", encoding="utf-8") as neo:
        p = (neo.read()).replace("\n\n", "")
    await xx.edit(f'<code>{p}</code>',parse_mode='HTML')
    os.remove("neo.txt")

@ultroid_cmd(pattern='eval ?(.*)',owner_only=True)
async def eval(event):
    try:cmd=event.raw_text.split(maxsplit=1)[1]
    except: return await event.reply("**Give Eval Code !!!**")
    xx=await event.reply('**Processing...**')
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd,event)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    if len(evaluation)>4096:
        with open('eval.txt','w') as f:
            f.write(evaluation)
        await ultroid.send_file(event.chat_id,'eval.txt',force_document=True,thumb='thumb.jpg',allow_cache=False,caption=f'''<b>• Eval :-
<code>{cmd}</code></b>''',parse_mode='HTML',reply_to=event.id)
        os.remove('eval.txt')
        await xx.delete()
    else:
        await xx.edit(f'''<b>• Eval :-
<code>{cmd.strip()}</code>

• Result :- 
<code>{evaluation.strip()}</code></b>''',parse_mode='HTML')

@ultroid_cmd(pattern='bash ?(.*)',owner_only=True)
async def bash_(event):
    try:cmd=event.raw_text.split(maxsplit=1)[1]
    except: return await event.reply("**Give Bash Code !!!**")
    xx=await event.reply('**Processing...**')
    stdout, stderr = await bash(cmd, run_code=1)
    OUT = f"**☞ BASH\n\n• COMMAND:**\n`{cmd}` \n\n"
    err, out = "", ""
    if stderr:
        err = f"**• ERROR:** \n`{stderr}`\n\n"
    if stdout:
            stdout = f"`{stdout}`"
            out = f"**• OUTPUT:**\n{stdout}"
    if not stderr and not stdout:
        out = "**• OUTPUT:**\n`Success`"
    OUT += err + out
    if len(OUT) > 4096:
        ultd = err + out
        with BytesIO(str.encode(ultd)) as out_file:
            out_file.name = "bash.txt"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                thumb='thumb.jpg',
                allow_cache=False,
                caption=f"`{cmd}`" if len(cmd) < 998 else None,
                reply_to=event.id,
            )

            await xx.delete()
    else:
        await xx.edit(OUT, link_preview=False)