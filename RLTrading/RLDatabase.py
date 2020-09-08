from RLUtil import MAX_VALUE, MAX_ITEMS, ITEM_DESC_IND, DESC_POSTLINK_IND, DESC_TIME_IND, DESC_USERNAME_IND, MAX_DESC_COUNT, DAY_THRESHOLD, TIME_FORMAT
from pandas import DataFrame

from datetime import datetime, timedelta

import time


class ItemDatabase:
    """ Class that holds all items, which can be exported as a DataFrame
        Data is added using the add_price() and add_cost() functions """
    def __init__(self):
        self.cost_dict = dict()
        self.price_dict = dict()
        self.null_cost = [ MAX_VALUE, ['NULL']*MAX_DESC_COUNT ]
        self.null_price = [-MAX_VALUE, ['NULL']*MAX_DESC_COUNT ]

    def add_cost(self, name: str, value: int, description: list) -> None:
        """ Stores cost information as dictionary
            cost_dict is equal to { item name: [cost, list] }
            where list holds link, username, comment, and etc """
        if self.cost_dict.get(name) is None:
            self.cost_dict[name] = list()
        # Avoid duplicates
        if self.cost_dict[name].count( [value, description] ) == 0:
            self.cost_dict[name].append( [value, description] )

    def add_price(self, name: str, value: int, description: list) -> None:
        """ Stores price information as dictionary
            price_dict is equal to { item name: [price, list] }
            where list holds link, username, comment, and etc """
        if self.price_dict.get(name) is None:
            self.price_dict[name] = list()
        # Avoid duplicates
        if self.price_dict[name].count( [value, description] ) == 0:
            self.price_dict[name].append( [value, description] )

    def remove_username(self, username_in: str) -> None:
        """ Removes any cost or price that contains username_in """
        removed_link = False
        user_dict_list = [self.cost_dict, self.price_dict]

        for user_dict in user_dict_list:
            # Loop over dictionaries for cost and price
            for key in user_dict:
                # Loop over lists in dictionary
                for i in range(len(user_dict[key])):

                    # Store description list and check username
                    description = user_dict[key][i][ITEM_DESC_IND]
                    if description[DESC_USERNAME_IND] == username_in:
                        # Save link and replace cost or price for printing
                        removed_link = description[DESC_POSTLINK_IND]

                        # Nullify key
                        if user_dict is self.cost_dict:
                            user_dict[key][i] = self.null_cost
                        else:
                            user_dict[key][i] = self.null_price

        # Only print if username found
        if removed_link is not False:
            print('SPAM BOT: %s flagged as a bot %s' % (username_in, removed_link))

    def remove_old(self) -> None:
        """ Removes any posts that are DAY_THRESHOLD days old
            Old posters are not likely to respond and """
        remove_count = 0
        user_dict_list = [self.cost_dict, self.price_dict]

        for user_dict in user_dict_list:
            # Loop over dictionaries for cost and price
            for key in user_dict:
                for i in range(len(user_dict[key])):

                    # Get post time and convert it
                    time_post = user_dict[key][i][ITEM_DESC_IND][DESC_TIME_IND]
                    time_post = datetime.strptime(time_post, TIME_FORMAT)

                    # Nullify key if post is too old
                    if time_post + timedelta(days=DAY_THRESHOLD) < datetime.now():
                        remove_count += 1
                        if user_dict is self.cost_dict:
                            user_dict[key][i] = self.null_cost
                        else:
                            user_dict[key][i] = self.null_price

        if remove_count > 0:
            print('%i items older than %i days have been deleted' % (remove_count, DAY_THRESHOLD))

    def create_df(self) -> DataFrame:
        """ Creates DataFrame by combining dictionaries
            and sorting back optimal prices and costs """
        # Header are generated based on MAX_ITEMS
        header_names = list()
        header_names.append('Item Name')
        header_names.append('Possible Gain')
        for i in range(MAX_ITEMS):
            header_names.append('Cost %i' % i)
            header_names.append('Cost Info %i' % i)
        for i in range(MAX_ITEMS):
            header_names.append('Price %i' % i)
            header_names.append('Price Info %i' % i)

        # Create list to be converted into dataframe
        table_out = list()

        # Loop over all unique keys
        unique_keys = set().union(self.cost_dict, self.price_dict)
        for key in unique_keys:
            # Initialize key if not declared
            if self.cost_dict.get(key) is None:
                self.cost_dict[key] = list()
            if self.price_dict.get(key) is None:
                self.price_dict[key] = list()

            # Add extra elements to ensure minimum items exist
            for i in range(MAX_ITEMS):
                self.cost_dict[key].append( self.null_cost )
                self.price_dict[key].append( self.null_price )

            # Sort rows for optimal gains
            sorted_cost = sorted( self.cost_dict[key] )
            sorted_price = sorted( self.price_dict[key] )
            sorted_price.reverse()

            # Create row based on header definitions
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

            # Append to DataFrame
            table_out.append(row_list)

        # Create dataframe and sort column by best prices
        df_out = DataFrame(data=table_out, columns=header_names)
        return df_out.sort_values('Possible Gain', ascending=False)

    def get_highest_freq(self) -> str:
        """ Get the key for single type queries
            Highest frequency item is used to check """
        item_freq = 0
        key_out = None

        # Loop over all unique keys
        unique_keys = set().union(self.cost_dict, self.price_dict)
        for key in unique_keys:
            count = len(self.cost_dict[key]) + len(self.price_dict[key])
            if count > item_freq:
                item_freq = count
                key_out = key

        return key_out
