
@ultroid_cmd(pattern="install$",owner_only=True)
async def install(event):
    reply=await event.get_reply_message()
    if not reply and reply.document: return await event.reply("**Reply To Any Python File To Install !!!**")
    d_path=await ultroid.download_media(reply.media ,  file=f"addons/{reply.file.name}")
    try: load_plugin(d_path,addon=True)
    except Exception as e:
        os.remove(d_path)
        return await event.reply(e)
    base_name=os.path.basename(d_path).replace('.py','')
    logger.info(f'• Install Addon - {base_name} !!!')
    await event.reply(f'**Successfully Installed - `{base_name}`**')

@ultroid_cmd(pattern="uninstall ?(.*)",owner_only=True)
async def uninstall(event):
    matchs=event.pattern_match.group(1)
    if not matchs: return await event.reply('**Give Plugin Name Also !!!**')
    if matchs in LOADED_MODULES: return await event.reply('**Cant Uninstall Official Plugin !!!**')
    if matchs not in ADDONS: return await event.reply(f'**No Module Named - `{matchs}` !!!**')
    path=ADDONS[matchs]
    unload_plugin(matchs)
    os.remove(path)
    logger.info(f'• Uninstalled Addon - {matchs} !!!')
    await event.reply(f'**Successfully Uninstalled - `{matchs}`**')