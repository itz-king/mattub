import math

_doc_='''• `/help <optional plugin name>` - Get Help Of Different Modules'''

fmt='''**MattUb Help

Total Plugins Installed - `{}`
Total Addons Installed - `{}`
Total Functions Currently Working - `{}`

Powered By** [MattUb](https://github.com/itz-king/mattub)'''

@ultroid_cmd(pattern="help ?(.*)",sudo_also=True)
async def help_(event):
    args=event.pattern_match.group(1)
    if args:
        if args in HELP_STR: return await event.reply(HELP_STR[args],link_preview=False)
        else: return await event.reply(f'**No Module Named - `{args}` !!!**')
    f_count=ultroid.list_event_handlers()
    if udB.get_key('HELP_PIC'): file_=udB.get_key('HELP_PIC')
    else: file_=None
    await event.reply(fmt.format(len(LOADED_MODULES),len(ADDONS),len(f_count)),
        buttons=[[
            Button.inline('Plugins','help plugins 1'),
            Button.inline('Addons','help addons 1')
        ]],link_preview=False,file=file_)

def get_help_buttons(list_ , page):
    sublist=[list_[i:i+8] for i in range(0, len(list_), 8)][page-1]
    sublist=[sublist[i:i+2] for i in range(0, len(sublist), 2)]
    return sublist

@ultroid.on(events.CallbackQuery(pattern="^help ?(.*)"))
async def helpcb(event):
    args=event.data_match.group(1).decode('utf-8').split()
    f_count=ultroid.list_event_handlers()
    if not args:
        return await event.edit(fmt.format(len(LOADED_MODULES),len(ADDONS),len(f_count)),
            buttons=[[
            Button.inline('Plugins','help plugins 1'),
            Button.inline('Addons','help addons 1')
        ]],link_preview=False)
    if args[0] == 'plugins':
        page=int(args[-1])
        x=[i for i in LOADED_MODULES]
        sorted(x)
        xx=get_help_buttons(x,page)
        button=[[]]
        for i in xx:
            for j in i:
                button[-1].append(Button.inline(f'✘ {j.capitalize()} ✘',f'help {j}'))
            button.append([])
        if (page-1)<1: 
            prev=math.ceil(len(x)/8)
            if (page+1)>math.ceil(len(x)/8): next_=1
            else:next_=page+1
        elif (page+1)>math.ceil(len(x)/8):
            prev=page-1
            next_=1
        else:
            prev=page-1
            next_=page+1
        button.append([
            Button.inline(' « ',f'help plugins {prev}'),
            Button.inline(' Back ',f'help'),
            Button.inline(' » ',f'help plugins {next_}'),
        ])
        try:await event.edit(fmt.format(len(LOADED_MODULES),len(ADDONS),len(f_count)) , buttons=button,link_preview=False)
        except: await event.answer()
    elif args[0] == "addons":
        page=int(args[-1])
        x=[i for i in ADDONS]
        if len(x)==0: return await event.answer("No Addons Installed",alert=True)
        sorted(x)
        xx=get_help_buttons(x,page)
        button=[[]]
        for i in xx:
            for j in i:
                button[-1].append(Button.inline(f'✘ {j.capitalize()} ✘',f'help {j}'))
            button.append([])
        if (page-1)<1: 
            prev=math.ceil(len(x)/8)
            if (page+1)>math.ceil(len(x)/8): next_=1
            else:next_=page+1
        elif (page+1)>math.ceil(len(x)/8):
            prev=page-1
            next_=1
        else:
            prev=page-1
            next_=page+1
        button.append([
            Button.inline(' « ',f'help addons {prev}'),
            Button.inline(' Back ',f'help'),
            Button.inline(' » ',f'help addons {next_}'),
        ])
        try:await event.edit(fmt.format(len(LOADED_MODULES),len(ADDONS),len(f_count)) , buttons=button,link_preview=False)
        except: await event.answer()