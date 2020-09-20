from pandas import DataFrame
from os import path

import re
import time


""" All constants are stored in utility """
# Number of posts to store per repeated item
MAX_ITEMS = 6
# Age to remove old posts
DAY_THRESHOLD = 1
# Maximum value of item
MAX_VALUE = 99999

# Time format
TIME_FORMAT = "%Y%m%d%H%M%S"

# Name of blacklist file
BLACKLIST_FILE = path.abspath(path.join(path.dirname(__file__), '..', 'SBotDetection', 'blacklist.txt'))
# RL Trading url
BASE_URL = 'https://rocket-league.com'
# Watch list directory name
WATCH_DIR = 'watchlist'
# Name of save file
PICKLE_FILE = 'RLTrading.p'


class Query:
    """ Search parameters to get poster listings """
    def __init__(self):
        self.key = None
        self.action = None
        self.max_search = 0
        self.url = None


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


def string_clean(text_in: str) -> str:
    """ Clean strings to remove weird characters and extra spaces """
    text_out = re.sub('[^ A-Za-z0-9:/-]', '', text_in)
    # Remove duplicate spaces
    text_out = ' '.join(text_out.split())
    return text_out

