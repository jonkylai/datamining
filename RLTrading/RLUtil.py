from pandas import DataFrame
from os import path

import time


""" All constants are stored in utility """
# Number of posts to store per repeated item
MAX_ITEMS = 5
# Age to remove old posts
DAY_THRESHOLD = 3
# Maximum value of item
MAX_VALUE = 99999

# Index in item list
ITEM_NAME_IND = 0
ITEM_DESC_IND = 1
# Index in description list
DESC_POSTLINK_IND = 0
DESC_ITEMLINK_IND = 1
DESC_TIME_IND = 2
DESC_USERNAME_IND = 3
DESC_COMMENT_IND = 4
MAX_DESC_COUNT = 5

# Time format
TIME_FORMAT = "%Y%m%d%H%M%S"

# Name of blacklist file
BLACKLIST_FILE = path.abspath(path.join(path.dirname(__file__), '..', 'DetectSteamBot', 'blacklist.txt'))
# RL Trading url
BASE_URL = 'https://rocket-league.com'
# Watch list directory name
WATCH_DIR = 'watchlist'
# Name of save file
PICKLE_FILE = 'RLTrading.p'


class Query:
    """ Search parameters to get poster listings """
    def __init__(self):
        self.name = None
        self.action = None
        self.key = None
        self.max_search = 0
        self.params = {}


def print_time(string_in: str, time_in: float, benchmark_in: float) -> float:
    """ Benchmark run time of specified chunks of code
        Usage requires time.time() before and print_time() after
        Also removes this time from total program benchmark time """
    elapsed_time = time.time() - time_in
    print('--- %0.4f sec --- %s' % (elapsed_time, string_in))

    return benchmark_in + elapsed_time


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


