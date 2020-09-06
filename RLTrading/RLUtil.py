from pandas import DataFrame
from os import path
import pandas as pd
import matplotlib


""" All constants are stored in this utility file """
# Number of posts to store per repeated item
MAX_ITEMS = 4
# Maximum value of item
MAX_VALUE = 99999

# Index in item list
NAME_INDEX = 0
DESCRIPTION_INDEX = 1
# Index in description list
POST_LINK_INDEX = 0
ITEM_LINK_INDEX = 1
USERNAME_INDEX = 2
COMMENT_INDEX = 3
# Name of blacklist file
BLACKLIST_FILE = path.abspath(path.join(path.dirname(__file__), '..', 'DetectSteamBot', 'blacklist.txt'))
# RL Trading url
BASE_URL = 'https://rocket-league.com'
# Watch list directory name
WATCH_DIR = 'watchlist'


class Query:
    """ Search parameters to get poster listings """
    def __init__(self):
        self.name = None
        self.action = None
        self.key = None
        self.max_search = 0
        self.params = {}


def get_df_index(key_in: str, df_in: DataFrame) -> int:
    """ Returns index of a key with error checking """
    index_list = df_in.index[df_in['Item Name'] == key_in].tolist()
    if len(index_list) != 1:
        print('ERROR: Cannot find %s in dataframe' % key_in)
        exit()
    else:
        return index_list[0]


def int_cast(user_in: str) -> int:
    """ Int cast with failure checking """
    try:
        return int( user_in.strip() )
    except ValueError:
        print('ERROR: Cannot cast int on %s' % user_in)
        exit()
    finally:
        pass


