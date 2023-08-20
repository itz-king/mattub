_doc_='''• `/install <reply to file>` - Install A Plugin

• `/uninstall <plugin name>` - Uninstall A Plugin'''

import asyncio
import re
import io
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

@ultroid_cmd(pattern='sysinfo$',owner_only=True)
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
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
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
        await event.reply(f'''<b>• Eval :-
<code>{cmd}</code></b>''',parse_mode='HTML',file='eval.txt')
        os.remove('eval.txt')
    else:
        await event.reply(f'''<b>• Eval :-
<code>{cmd.strip()}</code>

• Result :- 
<code>{evaluation.strip()}</code></b>''',parse_mode='HTML')