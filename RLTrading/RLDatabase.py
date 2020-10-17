from RLUtil import MAX_VALUE, MAX_ITEMS, DAY_THRESHOLD, TIME_FORMAT
from RLExport import get_color

from pandas import DataFrame
from datetime import datetime, timedelta

import time


class SingleItem:
    """ Class that holds information about a single item
        Having this pseudo-struct makes it easier to add more data """
    def __init__(self):
        self.item_name = 'NULL'
        self.item_value = -1
        self.item_link = 'NULL'
        self.post_link = 'NULL'
        self.post_time = 'NULL'
        self.username = 'NULL'
        self.comment = 'NULL'
        self.is_new = True
        self.is_multitrade = False


class ItemDatabase:
    """ Class that holds all items, which can be exported as a DataFrame
        Data is added using the add_price() and add_cost() functions """
    def __init__(self):
        self.cost_dict = dict()
        self.price_dict = dict()

        self.null_cost = SingleItem()
        self.null_cost.item_value = MAX_VALUE
        self.null_cost.is_new = False

        self.null_price = SingleItem()
        self.null_price.item_value = -MAX_VALUE
        self.null_price.is_new = False

    def add_cost(self, item_in: SingleItem) -> None:
        """ Stores cost information as dictionary """
        name = item_in.item_name
        if self.cost_dict.get(name) is None:
            self.cost_dict[name] = list()

        # Avoid duplicates
        if not self.is_duplicate(self.cost_dict, item_in.item_name, item_in.item_value, item_in.post_link):
            self.cost_dict[name].append(item_in)

    def add_price(self, item_in: SingleItem) -> None:
        """ Stores price information as dictionary """
        name = item_in.item_name
        if self.price_dict.get(name) is None:
            self.price_dict[name] = list()

        # Avoid duplicates
        if not self.is_duplicate(self.price_dict, item_in.item_name, item_in.item_value, item_in.post_link):
            self.price_dict[name].append(item_in)

    def is_duplicate(self, dict_in: dict, name_in: str, value_in: int, link_in: str) -> bool:
        """ Checks if an item already exists
            This function allows only the post link name to be compared since the time will always vary """
        # Compare only 2 fields rather than all of them
        for item in dict_in[name_in]:
            if value_in == item.item_value and link_in == item.post_link:
                return True
        return False

    def get_cost(self, name_in: str) -> float:
        """ Gets a feasible cost of a specified item
            This means getting the highest cost from MAX_ITEMS """
        if name_in in self.cost_dict:
            if len(self.cost_dict) >= MAX_ITEMS:
                sorted_cost = sorted(self.cost_dict[name_in], key=lambda x: x.item_value, reverse=True)
                print(sorted_cost)
                print('NEED TO TEST')
                exit()
                return sorted_cost[MAX_ITEMS - 1].item_value

        return -1

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
                    if user_dict[key][i].username == username_in:
                        # Save link and replace cost or price for printing
                        removed_link = user_dict[key][i].post_link

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

        # Loop over cost and price
        user_dict_list = [self.cost_dict, self.price_dict]
        for user_dict in user_dict_list:

            # Loop over dictionaries for cost and price
            for key in user_dict:

                # Loop over index of list
                for i in range(len(user_dict[key])):

                    # Get post time and convert it
                    post_time = user_dict[key][i].post_time
                    if post_time != 'NULL':
                        post_time = datetime.strptime(post_time, TIME_FORMAT)

                        # Nullify key if post is too old
                        if post_time + timedelta(days=DAY_THRESHOLD) < datetime.now():
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
        header_names.append('Item Link')
        header_names.append('Possible Gain')
        header_names.append('Possible Second')
        for i in range(MAX_ITEMS):
            header_names.append('Cost %i' % i)
            header_names.append('Cost Link %i' % i)
            header_names.append('Cost Steam %i' % i)
            header_names.append('Cost New %i' % i)
        for i in range(MAX_ITEMS):
            header_names.append('Price %i' % i)
            header_names.append('Price Link %i' % i)
            header_names.append('Price Steam %i' % i)
            header_names.append('Price New %i' % i)

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

            # Sort rows by item_value for optimal gains
            sorted_cost = sorted( self.cost_dict[key], key=lambda x: x.item_value, reverse=False)
            sorted_price = sorted( self.price_dict[key], key=lambda x: x.item_value, reverse=True)

            # Create row based on header definitions
            row_list = list()
            row_list.append( key )
            row_list.append( str(sorted_cost[0].item_link) )

            possible_gain = sorted_price[0].item_value - sorted_cost[0].item_value
            row_list.append( possible_gain )

            possible_second = sorted_price[2].item_value - sorted_cost[0].item_value
            row_list.append( possible_second )

            for i in range(MAX_ITEMS):
                row_list.append( sorted_cost[i].item_value )
                row_list.append( sorted_cost[i].post_link )
                row_list.append( sorted_cost[i].username )
                row_list.append( get_color(sorted_cost[i]) )
            for i in range(MAX_ITEMS):
                row_list.append( sorted_price[i].item_value )
                row_list.append( sorted_price[i].post_link )
                row_list.append( sorted_price[i].username )
                row_list.append( get_color(sorted_price[i]) )

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
            count = self.count_is_new(self.cost_dict[key]) + self.count_is_new(self.price_dict[key])
            if count > item_freq:
                item_freq = count
                key_out = key

        return key_out

    def count_is_new(self, list_in: list) -> int:
        """ Gets length of list for only items that are new """
        count_out = 0
        for item in list_in:
            if item.is_new == True:
                count_out += 1
        return count_out

    def change_is_new(self) -> None:
        """ Change all SingleItem.is_new to False """
        user_dict_list = [self.cost_dict, self.price_dict]
        # Loop over cost and price
        for user_dict in user_dict_list:

            # Loop over dictionaries for cost and price
            for key in user_dict:
                for item in user_dict[key]:
                    item.is_new = False
