# import os
# import sys

# sys.path.insert(1, os.path.join(sys.path[0], 'classes'))
# from languages import Languages
# from battleship import Battleship
# from tic_tac_toe import TicTacToe
# import global_variables as gv

# counter = 1
# interface = None

# def start():
#     global counter
#     # gv.interface
#     dict_of_languages = {}.items 
#     for lang in Languages.get_dict_of_access_languages().items():
#         list_of_full_name = []
#         full_name_on_main_lang = lang[1]["full_name"][lang[1]["main_lang"]]
#         for full_name_of_lang in lang[1]["full_name"].values():
#             if full_name_on_main_lang != full_name_of_lang:
#                 list_of_full_name.append(full_name_of_lang)
#         dict_of_languages.update(get_dict_of_settings(lang[0], {lang[0]: lang[1]}, f'{full_name_on_main_lang} ({", ".join(list_of_full_name)})', ['-' + lang[0], lang[0], full_name_on_main_lang]))
    
#     counter = 1
#     dict_of_games = {}
#     dict_of_games.update(Battleship)
#     dict_of_games.update(TicTacToe)
#     game = Games()
#     game.Start()

# def get_dict_of_settings(name, value_class_of_setting, title, list_of_commands, add_counter_to_list_of_commands = True) -> dict:
#     global counter
#     if add_counter_to_list_of_commands:
#         list_of_commands.append(str(counter))
#     dict_of_settings = {
#         name: {
#             'name': name,
#             'number': counter,
#             'value': value_class_of_setting,
#             'title': title,
#             'commands': list_of_commands,
#         },
#     }
#     counter += 1
#     return dict_of_settings

class Test:
    pass

def show():
    # print('Numer {axis} from {min} to {max}'.format(**{
    #     'axis': 'Of row', 
    #     'min': 1, 
    #     'max': 6,
    # }))

    # vowels list 
    vowels = ['a', 'e', 'i', 'o', 'i', 'u'] 
    # count element 'i' index
    # count = vowels.count('i') 
    # # print count 
    # print('The count of i is:', count) 
    # # count element 'p' 
    # count = vowels.count('p') 
    # # print count 
    # print('The count of p is:', count)
    # count = vowels.count('a') 
    # # print count 
    # print('The count of a is:', count)
    # count = vowels.count('u') 
    # # print count 
    # print('The count of u is:', count)

    count = vowels.index('i') 
    # print count 
    print('The index of i is:', count) 
    # count element 'p' 
    # count = vowels.index('p') 
    # # print count 
    # print('The index of p is:', count)
    count = vowels.index('a') 
    # print count 
    print('The index of a is:', count)
    count = vowels.index('u') 
    # print count 
    print('The index of u is:', count)

show()

# def show_and_processing_settings():
