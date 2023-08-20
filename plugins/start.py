fmt='''**MattUb Help

Total Plugins Installed - `{}`
Total Addons Installed - `{}`
Total Functions Currently Working - `{}`

Powered By** [MattUb](https://github.com/itz-king/mattub)'''

@ultroid_cmd(pattern="help ?(.*)",owner_only=True)
async def help_(event):
    args=event.pattern_match.group(1)
    if args:
        if args in HELP_STR: return await event.reply(HELP_STR[args],link_preview=False)
        else: return await event.reply(f'**No Module Named - `{args}` !!!**')
    await event.reply(fmt.format(len(LOADED_MODULES),len(ADDONS),len(FUNCTIONS)),
    buttons=[[
        Button.inline('Plugins','help plugins'),
        Button.inline('Addons','help addons')
    ]],link_preview=False)