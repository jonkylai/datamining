import pandas as pd
import re
import copy
import time
import matplotlib
import datetime

import requests
from bs4 import BeautifulSoup


# Number of posts to store per repeated item
MAX_ITEMS = 3
# Watch list directory name
WATCH_DIR = 'watchData'


class Query:
    """ Search parameters to get poster listings """
    def __init__(self):
        self.name = None
        self.action = None
        self.key = None
        self.max_search = 0
        self.params = {}


def get_link(soup_text: BeautifulSoup) -> str:
    """ Grabs the link so items are traceable """
    for line in soup_text.prettify().split():
        if '/trade/' in line:
            return 'https://rocket-league.com%s' % line.split('"')[1]

    # Stop mining if bad format
    print('ERROR: Cannot find /trade/ in soup_text')
    exit()


def int_cast(user_in: str) -> int:
    """ Int cast with failure checking """
    try:
        return int( user_in.strip() )
    except ValueError:
        print('ERROR: Cannot cast int on %s' % user_in)
        exit()
    finally:
        pass


def get_item(want_containers: list, has_containers: list) -> (list, list):
    """ Processes the poster's intentions to get the inherent value of an item """
    cost_list = list()
    price_list = list()

    # Processing if user requests 1:1 trade
    if len(has_containers) == len(want_containers):

        for i in range( len(has_containers) ):
            # Create empty item
            poster_item = dict( name  = '',
                                link  = '',
                                value = -1 )
            poster_item['link'] = has_containers[i]['link']

            # If poster is selling
            if has_containers[i]['name'] != 'Credits' and want_containers[i]['name'] == 'Credits':
                poster_item['name'] = '%s %s %s' % ( has_containers[i]['name'],
                                                     has_containers[i]['color'],
                                                     has_containers[i]['rarity'] )
                # Remove extra white space
                poster_item['name'] = ' '.join( poster_item['name'].split() )
                # Divide if poster requests multiple items
                poster_item['value'] = want_containers[i]['count'] / has_containers[i]['count']
                cost_list.append(poster_item)

            # If poster buying
            if has_containers[i]['name'] == 'Credits' and want_containers[i]['name'] != 'Credits':
                poster_item['name'] = '%s %s %s' % ( want_containers[i]['name'],
                                                     want_containers[i]['color'],
                                                     want_containers[i]['rarity'] )
                # Remove extra white space
                poster_item['name'] = ' '.join( poster_item['name'].split() )
                # Divide if poster requests multiple items
                poster_item['value'] = has_containers[i]['count'] / want_containers[i]['count']
                price_list.append(poster_item)

            else:
                pass

    else:
        # Add NLP and others methods later
        pass

    return [cost_list, price_list]


def get_container(soup_text: BeautifulSoup, link_in: str) -> list:
    """ Grabs all necessary information from poster container """
    container_list = list()
    empty_container = dict(name  = '',
                           color = '',
                           rarity = '',
                           count = 1,
                           link  = '')
    name_flag = False
    cert_flag = False
    amount_flag = False

    for line in soup_text.prettify().split('\n'):

        # Image keyword
        if 'img alt' in line:
            container_list.append( copy.deepcopy(empty_container) )
            container_list[-1]['link'] = link_in

        # Rarity keyword
        if 'rlg-trade-item-gradient is' in line:
            container_list[-1]['rarity'] = line.split('is')[-1].split('\"')[0]

        # Name keyword
        elif '<h2>' in line:
            name_flag = True
        elif name_flag:
            container_list[-1]['name'] = line.strip()
            name_flag = False

        # Certification keyword
        elif '<span>' in line:
            cert_flag = True
        elif cert_flag:
            container_list[-1]['name'] += ' %s' % line.strip()
            cert_flag = False

        # Color keyword
        elif 'rlg-trade-display-item-paint' in line:
            container_list[-1]['color'] = line.split('data-name=\"')[-1].split('\"')[0]

        # Amount keyword
        elif amount_flag:
            container_list[-1]['count'] = int_cast(line)
            amount_flag = False
        elif 'rlg-trade-display-item__amount is' in line:
            amount_flag = True

    return container_list


def get_df_index(key_in, df_in) -> int:
    index_list = df_in.index[df_in['Item Name'] == key_in].tolist()
    if len(index_list) != 1:
        print('ERROR: Cannot find %s in dataframe' % key_in)
        exit()
    else:
        return index_list[0]


class ItemDatabase:
    def __init__(self):
        self.price_dict = {}
        self.cost_dict = {}

    def add_price(self, name: str, value: int, link: str):
        if self.price_dict.get(name) is None:
            self.price_dict[name] = list()
        self.price_dict[name].append( [value, link] )

    def add_cost(self, name: str, value: int, link: str):
        if self.cost_dict.get(name) is None:
            self.cost_dict[name] = list()
        self.cost_dict[name].append( [value, link] )

    def create_df(self):
        # Create dataframe columns
        header_names = list()
        header_names.append('Item Name')
        header_names.append('Possible Gain')
        for i in range(MAX_ITEMS):
            header_names.append('Cost %i' % i)
            header_names.append('Cost Link %i' % i)
        for i in range(MAX_ITEMS):
            header_names.append('Price %i' % i)
            header_names.append('Price Link %i' % i)
        df = pd.DataFrame(columns = header_names)

        # Loop over all unique keys
        unique_keys = set().union(self.cost_dict, self.price_dict)
        for key in unique_keys:
            # Initialize key if not declared
            if self.cost_dict.get(key) is None:
                self.cost_dict[key] = list()
            if self.price_dict.get(key) is None:
                self.price_dict[key] = list()

            # Add extra elements to ensure minimum
            for i in range(MAX_ITEMS):
                self.cost_dict[key].append( [99999, 'NULL'] )
                self.price_dict[key].append( [-1, 'NULL'] )

            # Sort for optimal gains
            sorted_cost = sorted( self.cost_dict[key] )
            sorted_price = sorted( self.price_dict[key] )
            sorted_price.reverse()

            row_list = list()
            row_list.append(key)
            possible_gain = sorted_price[0][0] - sorted_cost[0][0]
            row_list.append(possible_gain)
            for i in range(MAX_ITEMS):
                row_list.append(sorted_cost[i][0])
                row_list.append(sorted_cost[i][1])
            for i in range(MAX_ITEMS):
                row_list.append(sorted_price[i][0])
                row_list.append(sorted_price[i][1])

            single_df = pd.DataFrame( [row_list], columns=header_names )
            df = df.append(single_df, ignore_index=True)

        return df


# Mine queries and processes them
class RLTrades:
    def __init__(self, user_query: Query):
        user_action = user_query.action
        user_params = user_query.params
        user_key = user_query.key
        user_max = user_query.max_search

        database = ItemDatabase()

        # Begin data mining from user_max to page 1, where p is the page number
        user_params.update({'p': 0})
        for i in range(user_max, 0, -1):
            user_params['p'] = i

            # Times requests.get() speed
            time_page = time.time()
            page = requests.get('https://rocket-league.com/trading', params=user_params)
            print('--- %0.4f sec --- %s' % ( time.time() - time_page,
                                             page.url ) )

            page_soup = BeautifulSoup(page.content, 'html.parser')

            # Parse by individual post
            user_list = page_soup.find_all('div', {'class': 'rlg-trade-display-container is--user'})

            # Loop over each item
            for user_soup in user_list:
                # Page keywords
                url_text = user_soup.find_all('div', {'class': 'rlg-trade-link-container'})
                has_text = user_soup.find_all('div', {'id': 'rlg-youritems'})
                want_text = user_soup.find_all('div', {'id': 'rlg-theiritems'})

                post_link = get_link(url_text[0])

                # Gets Container for has and wants from poster
                want_containers = get_container(want_text[0], post_link)
                has_containers  = get_container(has_text[0],  post_link)

                # Use NLP to get poster's desired trades
                [cost_list, price_list] = get_item(want_containers, has_containers)

                # Store all data in dict
                for cost_item in cost_list:
                    database.add_cost( cost_item['name'],
                                       cost_item['value'],
                                       cost_item['link'] )
                for price_item in price_list:
                    database.add_price( price_item['name'],
                                        price_item['value'],
                                        price_item['link'] )

        # Create dataframe and organize
        self.df = database.create_df()
        self.df = self.df.sort_values('Possible Gain', ascending=False)
        self.df.to_csv('data.csv', index=False)

        # Execute user input action
        if user_action == 'Single':
            self.print_single(user_key)
        elif user_action == 'Watch':
            self.print_single(user_key)
            self.item_watch(user_key)

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
