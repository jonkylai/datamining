from RLDatabase import ItemDatabase
from RLParser import get_text_between
from RLUtil import print_time

from os import path

import requests
import time


SAVE_DIR = 'savedata'
REPLACE_LIST = [':', '*', '/', '|', '?']


def get_title(page_in: str) -> str:
    for line in page_in.split('\n'):
        if 'title' in line:
            string_out = get_text_between(line, '<title>', '</title>')
            for character in REPLACE_LIST:
                string_out = string_out.replace(character, '_')
            return string_out


def mine_steam(database_in: ItemDatabase) -> None:
    """ Save account data from items """
    benchmark_time = time.time()
    requests_time = 0

    # Make list by looping over every item in cost_dict and price_dict
    username_list = list()
    user_dict_list = [database_in.cost_dict, database_in.price_dict]
    for user_dict in user_dict_list:
        for key in user_dict:
            for item in user_dict[key]:
                if item.username != 'NULL':
                    username_list.append(item.username)

    # Loop over unique items
    for username in list( set(username_list) ):
        # Load page
        benchmark_time = time.time()
        page = requests.get(username)
        title = get_title(page.text)
        save_path = '%s/%s.html' % (SAVE_DIR, title)
        requests_time = print_time(username, benchmark_time, requests_time)

        # Save if file does not exist
        if not path.exists(save_path):
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(page.text)
            print('Wrote to \"%s\"' % save_path)

    minutes, seconds = divmod(requests_time, 60)
    print('Requests time: %0.0f m %0.0f s' % (minutes, seconds))
    minutes, seconds = divmod(time.time() - benchmark_time, 60)
    print('Other time: %0.0f m %0.0f s' % (minutes, seconds))

