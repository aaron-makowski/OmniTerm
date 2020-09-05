import json

with open('omni_db.json', encoding='utf-8', mode="r") as f:
	data = json.load(f)

total_apps = len([z for x, y in data.items() for z in y])

print(""""
  ______                          _               
    /                            //               
 --/_  __  ______  o ____  __.  //                
(_/</_/ (_/ / / <_<_/ / <_(_/|_</_                
                                                  
                                                  
   __             __                              
  /  )           /  )    _/_                      
 /--/ _   _     /   __.  /  _  _,  __ __  o _  _  
/  (_/_)_/_)_  (__/(_/|_<__</_(_)_(_)/ (_<_</_/_)_
    /   /                      /|                 
   '   '                      |/                  
""")

from random import choice
from rich.console import Console
from rich.table import Table

console = Console()
print = console.print #override/replace print!

def print_with_border(
    dictionary, headers, 
    colors=['magenta', 'white','navajo_white1','orange1','orchid1',
            'orchid2','salmon1','tan','yellow3','light_cyan3','navajo_white3',
            'light_salmon3','chartreuse1','light_slate_grey','light_pink4', 'cornflower_blue',
            'aquamarine1','sea_green3','aquamarine3','sky_blue3', 'chartreuse4',
            'orange4','cyan1','cyan2','cyan3','turquoise2','spring_green3', 'bright_green',
            'turquoise4','bright_white','bright_cyan','bright_yellow'
            ],
    emojis=[':avocado:','::',':sparkles:',':purple_circle:',':large_blue_diamond:',
            ':laptop_computer:',':gem_stone:',':droplet:',':diamond_with_a_dot:',
            ':crown:',':cityscape_at_dusk:',':bank:',':ballot_box_with_check:',':balloon:'
            ]):
    for app, data in dictionary.items():
        app_color, info_color = choice(colors), choice(colors)
        table = Table(show_header=True, header_style=f'bold {app_color}')
        table.add_column(app)
        table.add_row(f'[bold {info_color}]{data[0]}[/bold {info_color}]')
        table.add_row(f'\n[bold cyan]{data[1]}[/bold cyan]')
        
        # url = data[1]
        # if 'github.com/' in url:
        #     import github3
        #     _, useful = url.split('github.com/')
        #     github_user, repo_name = useful.split('/')
        #     #print(github_user, repo_name)
        #     repo = github3.repository(github_user, repo_name)
        #     import base64
        #     if f'pip install {app}' in base64.decodestring(repo.file_contents('README.md').content):
        #         print('pip installable')
        #     # table.add_column('Info')
        #     # table.add_row(f'{repo.open_issues_count} Open Issues')
        print(table)

#from bullet import colors
#colors.bright(colors.foreground["cyan"]),

from bullet import Check, keyhandler, styles
from bullet.charDef import NEWLINE_KEY

class MinMaxCheck(Check):
    def __init__(self, min_selections=0, max_selections=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_selections = min_selections
        self.max_selections = max_selections if max_selections else len(self.choices)

    @keyhandler.register(NEWLINE_KEY)
    def accept(self):
        if self.valid():
            return super().accept()

    def valid(self):
        return self.min_selections <= sum(1 for c in self.checked if c) <= self.max_selections


all_choices = [x for x in data.keys()]

max_items = 20
starting_index = 0

while True:
    ending_index = starting_index + max_items
    choices = [f'Print All {total_apps} Apps...' if not starting_index else '<= Prev Page'] \
            + all_choices[starting_index : ending_index] \
            + ['Next Page =>' if starting_index < len(all_choices) - 1 else '<= Page 1']

    client = MinMaxCheck(
        prompt = "Use Space Bar to select categories...\n",
        min_selections = 1,
        return_index = False,
        choices = choices,
        **styles.Exam
    )
    #print(end = '')
    result = client.launch()

    if 'Next Page =>' in result:
        starting_index += max_items
        starting_index = min(len(all_choices), starting_index)
    elif '<= Prev Page' in result:
        starting_index -= max_items
        starting_index = max(0, starting_index)
    elif '<= Page 1' in result:
        starting_index = 0
    elif f'Print All {total_apps} Apps...' in result:
        for x in all_choices:
            for app, app_info in data[x].items():
                try:
                    new_desc = app_info['description']
                    length = len(new_desc)
                    max_length = len(app_info['url'])
                    max_length = max_length if max_length > 50 else 50

                    if length > max_length:
                        chops = int(length / max_length) # 1 chop per length over multiple of 50
                        segment_len = length / (chops + 1)
                        #print(length, chops, segment_len)
                        for chop in range(0, int(chops)):
                            idx = new_desc[:int(segment_len * (chop + 1))].rfind(' ')#; print(idx)
                            #idx = idx if len(new_desc[idx+1:]) > idx else new_desc.find(' ', int((segment_len) * (chop + 1))); print(idx)
                            new_desc = new_desc[:idx] + '\n' + new_desc[idx+1:] # idx+1 to replace space
                    print_with_border({app: [new_desc, 
                                              app_info['url']]}, headers='keys')
                except:
                    pass
        break
    else:
        for category in result:
            for app, app_info in data[category].items():
                new_desc = app_info['description']
                length = len(new_desc)
                max_length = len(app_info['url'])
                max_length = max_length if max_length > 50 else 50

                if length > max_length:
                    chops = int(length / max_length) # 1 chop per length over multiple of 50
                    segment_len = length / (chops + 1)
                    #print(length, chops, segment_len)
                    for chop in range(0, int(chops)):
                        idx = new_desc[:int(segment_len * (chop + 1))].rfind(' ')#; print(idx)
                        #idx = idx if len(new_desc[idx+1:]) > idx else new_desc.find(' ', int((segment_len) * (chop + 1))); print(idx)
                        new_desc = new_desc[:idx] + '\n' + new_desc[idx+1:] # idx+1 to replace space
                print_with_border({app: [new_desc, app_info['url']]}, headers='keys')
        break

# import github3
# for category in all_choices:
#     for app, app_info in data[category].items():
#         url = app_info['url']
#         if 'github.com/' in url:
#             _, useful = url.split('github.com/')
#             github_user, repo_name = useful.split('/')
#             #print(github_user, repo_name)
#             repo = github3.repository(github_user, repo_name)

#             #Get issues amount
#             for issue in repo.issues(state='open'):
#                 print(f':cross_mark: {repo.open_issues_count} Open Issues: ')
#                 #print(f'{repo}#{issue.number}: "{issue.title}"\n\t{issue.html_url}')
#                 print('Last Commit: ' + str(repo.pushed_at))
#                 print('Last Update: ' + str(repo.updated_at))
#                 print('Has a Wiki: ' + str(repo.has_wiki))
#                 print('Languages: ' + str([x for x in repo.languages]))

#check if app is pip installable
# [![PyPI badge](https://badge.fury.io/py/huge.svg)](https://badge.fury.io/py/huge)
# ```
# f'pip install {app}''
# ```