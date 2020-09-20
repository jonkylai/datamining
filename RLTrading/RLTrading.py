from RLDatabase import ItemDatabase
from RLParser import get_link, get_time, get_username, get_comment, get_container
from RLLanguage import get_item
from RLUtil import Query, get_df_index, print_time, TIME_FORMAT, WATCH_DIR, MAX_ITEMS, PICKLE_FILE
from RLExport import create_page
from RLSpamFilter import spam_filter
from RLMine import mine_steam
from SavedQueries import all_queries, single_query

import requests
import time
import re
import os
import pickle

from datetime import datetime
from pandas import DataFrame
from bs4 import BeautifulSoup
from os import path, remove


class RLTrades:
    """ Class that processes query using regex and BeautifulSoup
        If page layout changes, RLParser functions must be changed """
    def __init__(self, user_query: Query) -> None:
        global benchmark_recorded

        # Stores query as local variables
        user_action = user_query.action
        user_url = user_query.url
        user_key = user_query.key
        user_max = user_query.max_search

        # Initialize data
        benchmark_time = time.time()
        if user_action == 'Delete Pickle' and path.exists(PICKLE_FILE):
            remove(PICKLE_FILE)
            print('Removed pickled database')
            exit()
        if user_action == 'Data Mine':
            if path.exists(PICKLE_FILE):
                database = pickle.load(open(PICKLE_FILE, 'rb'))
                mine_steam(database)
            else:
                print('ERROR: %s does not exist' % PICKLE_FILE)
            exit()
        elif path.exists(PICKLE_FILE):
            database = pickle.load(open(PICKLE_FILE, 'rb'))
            database.change_is_new()
            benchmark_recorded = print_time('Loaded pickled database', benchmark_time, benchmark_recorded)
        else:
            database = ItemDatabase()
            benchmark_recorded = print_time('Created new database', benchmark_time, benchmark_recorded)

        # Begin data mining from user_max to page 1
        for i in range(user_max, 0, -1):

            # Get site data
            benchmark_time = time.time()
            page = requests.get('%s&p=%i' % (user_url, i))
            benchmark_recorded = print_time(page.url, benchmark_time, benchmark_recorded)

            page_soup = BeautifulSoup(page.content, 'html.parser')

            # Parse by individual post
            user_list = page_soup.find_all('div', {'class': 'rlg-trade'})

            # Loop over each item
            for user_soup in user_list:
                # Page keywords
                post_link = get_link(user_soup)
                post_time = get_time(user_soup)
                post_username = get_username(user_soup)
                post_comment = get_comment(user_soup)

                # Gets Container for has and wants from poster
                want_container = get_container('want', user_soup, post_link, post_time, post_username, post_comment)
                has_container  = get_container('has', user_soup, post_link, post_time, post_username, post_comment)

                # Use NLP to get poster's desired trades
                [cost_list, price_list] = get_item(want_container, has_container)

                # Store all data in dict
                for cost_item in cost_list:
                    database.add_cost(cost_item)
                for price_item in price_list:
                    database.add_price(price_item)

        # Remove old data
        benchmark_time = time.time()
        database.remove_old()
        benchmark_recorded = print_time('remove_old()', benchmark_time, benchmark_recorded)

        # Save data
        pickle.dump(database, open(PICKLE_FILE, 'wb'))

        # Create dataframe and organize
        benchmark_time = time.time()
        self.df = database.create_df()

        # Remove all possible spam and recreate dataframe
        database = spam_filter(database, self.df)
        self.df = database.create_df()
        benchmark_recorded = print_time('spam_filter()', benchmark_time, benchmark_recorded)

        # Export to both page and csv
        self.df.to_csv('data.csv', index=False)

        # Execute user input action
        if user_action == 'Single':
            create_page(self.df, 'General')
            # Print item using logic from get_highest_freq()
            user_key = database.get_highest_freq()
            self.print_single(user_key)

        elif user_action == 'Watch':
            create_page(self.df, 'General')
            # Print item from query
            self.print_single(user_key)
            # Store data to external file
            self.item_watch(user_key)

        elif user_action == 'Optimize':
            create_page(self.df, 'General')

    def print_single(self, user_key: str) -> None:
        """ Print out information from a single query
            This is useful for investing new potential items """
        print('\n')
        # Print item in question
        print('%s:' % user_key)

        # Get index of user_key
        user_index = get_df_index(user_key, self.df)

        # Print dataframe row
        print( self.df.loc[user_index] )
        print( 'Possible Gain = %0.1f' % self.df.loc[user_index]['Possible Gain'] )
        print( 'Possible Second = %0.1f' % self.df.loc[user_index]['Possible Second'] )

    def item_watch(self, user_key: str) -> None:
        # Get index of user_key
        user_index = get_df_index(user_key, self.df)

        row_df = self.df.loc[user_index]
        file_name = row_df['Item Name'].split('-')[0].lower()
        file_name = ''.join( re.split(r'\s|\(|\)', file_name ) ) + '.dat'

        fid = open('%s/%s' % (WATCH_DIR, file_name), 'a')
        now_date = datetime.now().strftime(TIME_FORMAT)
        fid.write('%s,%f,%f,%f,%f\n' % ( now_date,
                                         row_df['Cost 0'],
                                         row_df['Cost %i' % (MAX_ITEMS - 1)],
                                         row_df['Price 0'],
                                         row_df['Price %i' % (MAX_ITEMS - 1 )] ) )


def main():
    """ Basic logic for user input
        Made simple because I run this tens of times a day """
    # Create list of query options
    query_list = all_queries
    query_length = len(query_list)

    # Print options
    print('Existing queries:')
    for i in range(query_length):
        print( '%i. %s' % (i + 1, query_list[i].key) )

    # Prompt user
    user_input = input('Enter query or url: ')

    # Time total benchmark time except those documented by print_time()
    global benchmark_recorded
    benchmark_recorded = 0
    benchmark_all = time.time()

    try:
        # Preset input
        i = int(user_input)
        user_query = query_list[i - 1]
    except:
        # Manual input
        user_query = single_query
        user_query.url = user_input
        if 'filterPlatform=1' not in user_query.url:
            print('ERROR: Manual input requires steam platform string filterPlatform=1')
            exit()

    # Do everything else
    RLTrades(user_query)

    print('Time spent on recorded activities: %0.4f' % benchmark_recorded)
    print('Time spent on everything else:     %0.4f' % (time.time() - benchmark_all - benchmark_recorded))

    return 0


if __name__ == "__main__":
    main()

