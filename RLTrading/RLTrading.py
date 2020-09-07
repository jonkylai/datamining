from RLDatabase import ItemDatabase
from RLParser import get_link, get_time, get_username, get_comment, get_item, get_container
from RLUtil import Query, get_df_index, WATCH_DIR, MAX_ITEMS
from RLExport import create_page
from RLSpamFilter import spam_filter
from SavedQueries import all_queries, single_query

import requests
import time
import re
import datetime

from pandas import DataFrame
from bs4 import BeautifulSoup


class RLTrades:
    """ Class that processes query using regex and BeautifulSoup
        If page layout changes, *_text variables must be changed
        If page layout changes, RLParser class must be changed """
    def __init__(self, user_query: Query):
        # Stores query as local variables
        user_action = user_query.action
        user_url = user_query.url
        user_key = user_query.key
        user_max = user_query.max_search

        # Initialize database of dictionaries
        database = ItemDatabase()

        # Begin data mining from user_max to page 1
        for i in range(user_max, 0, -1):

            # Benchmark requests.get() speed
            time_page = time.time()
            page = requests.get('%s&p=%i' % (user_url, i))
            print('--- %0.4f sec --- %s' % ( time.time() - time_page,
                                             page.url ) )

            page_soup = BeautifulSoup(page.content, 'html.parser')

            # Parse by individual post
            user_list = page_soup.find_all('div', {'class': 'rlg-trade'})

            # Loop over each item
            for user_soup in user_list:
                # Page keywords
                header_text = user_soup.find_all('header', {'class': 'rlg-trade__header'})
                post_link = get_link(header_text[0])
                post_time = get_time(header_text[0])
                #print(post_time)

                username_text = user_soup.find_all('a', {'class': 'rlg-trade__platform'})
                post_username = get_username(username_text[0])

                comment_text = user_soup.find_all('div', {'class': 'rlg-trade__note'})
                if len(comment_text) > 0:
                    post_comment = get_comment(comment_text[0])
                else:
                    post_comment = ''

                # Gets Container for has and wants from poster
                want_text = user_soup.find_all('div', {'class': 'rlg-trade__itemswants'})
                want_container = get_container(want_text[0], post_link, post_username, post_comment)

                has_text = user_soup.find_all('div', {'class': 'rlg-trade__itemshas'})
                has_container  = get_container(has_text[0], post_link, post_username, post_comment)

                # Use NLP to get poster's desired trades
                [cost_list, price_list] = get_item(want_container, has_container)

                # Store all data in dict
                for cost_item in cost_list:
                    database.add_cost( cost_item['name'],
                                       cost_item['value'],
                                       cost_item['description'] )
                for price_item in price_list:
                    database.add_price( price_item['name'],
                                        price_item['value'],
                                        price_item['description'] )

        # Create dataframe and organize
        self.df = database.create_df()

        # Remove all possible spam and recreate dataframe
        database = spam_filter(database, self.df)
        self.df = database.create_df()
        self.df = self.df.sort_values('Possible Gain', ascending=False)

        # Export to both page and csv
        self.df.to_csv('data.csv', index=False)

        # Execute user input action
        if user_action == 'Single':
            create_page(self.df, 'Single')
            # Use logic to determine item type from url
            user_key = database.get_highest_freq()
            self.print_single(user_key)

        elif user_action == 'Watch':
            create_page(self.df, 'General')
            # Print item from query
            self.print_single(user_key)
            self.item_watch(user_key)

        elif user_action == 'Optimize':
            create_page(self.df, 'General')

    def print_single(self, user_key: str) -> None:
        """ Print out information from a single query
            This is useful for investing new potential """
        print('\n')
        # Print item in question
        print('%s:' % user_key)

        # Get index of user_key
        user_index = get_df_index(user_key, self.df)

        # Print dataframe row
        print( self.df.loc[user_index] )

    def item_watch(self, user_key: str) -> None:
        # Get index of user_key
        user_index = get_df_index(user_key, self.df)

        row_df = self.df.loc[user_index]
        file_name = row_df['Item Name'].split('-')[0].lower()
        file_name = ''.join( re.split(r'\s|\(|\)', file_name ) ) + '.dat'

        fid = open('%s/%s' % (WATCH_DIR, file_name), 'a')
        now_date = datetime.datetime.now()
        fid.write('%s,%f,%f,%f,%f\n' % ( now_date,
                                         row_df['Cost 0'],
                                         row_df['Cost %i' % (MAX_ITEMS - 1)],
                                         row_df['Price 0'],
                                         row_df['Price %i' % (MAX_ITEMS - 1 )] ) )


def main():
    # Create list of query options
    query_list = all_queries
    query_length = len(query_list)

    # Print options
    print('Existing queries:')
    for i in range(query_length):
        print( '%i. %s' % (i + 1, query_list[i].key) )

    # Prompt user
    user_input = input('Enter query or url: ')

    # Preset input
    try:
        i = int(user_input)
        user_query = query_list[i - 1]
    # Manual input
    except:
        user_query = single_query
        user_query.url = user_input

    results = RLTrades(user_query)

    return 0


if __name__ == "__main__":
    main()

