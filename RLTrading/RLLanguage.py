from RLDatabase import ItemDatabase, SingleItem
from RLUtil import string_clean, EXCLUDE_LIST, COLOR_LIST, NCC_LIST, NCU_LIST, NCR_LIST, NCVR_LIST, NCI_LIST, NCE_LIST, MAX_VALUE


""" Define dictionary for predefined NC classifications """
NC_TYPE = ['Common', 'Uncommon', 'Rare', 'Very-Rare', 'Import', 'Exotic']
NC_LIST = [NCC_LIST, NCU_LIST, NCR_LIST, NCVR_LIST, NCI_LIST, NCE_LIST]
NC_DICT = dict()
for i, nc_type in enumerate(NC_TYPE):
    for nc_item in NC_LIST[i]:
        # Generates the exact item_name after the string has been cleaned and titled
        key = 'Non-Crate %s Offer %s' % ( nc_type.replace('-',' '), nc_type )

        # Add key if not initialized
        if key not in NC_DICT.keys():
            NC_DICT[key] = list()

        # Add colored version to all NC items
        for color in COLOR_LIST:
            NC_DICT[key].append( '%s %s %s' % (nc_item, color, nc_type) )

""" Words to indicate the desire for an NC trade
    lower() already casted on comment """
NC_KEYWORDS = ['non crate', 'non-crate', 'ncr', 'ncvr', 'nci', 'nce']


def lexical_diversity(text_in: str) -> float:
    return len(set(text_in)) / len(text_in)


def container2item(container_in: dict) -> SingleItem:
    """" Copy basic information from container to item """
    item_out = SingleItem()
    item_out.post_link = container_in['post_link']
    item_out.item_link = container_in['item_link']
    item_out.post_time = container_in['post_time']
    item_out.username = container_in['username']
    item_out.comment = container_in['comment']
    item_out.is_multitrade = container_in['is_multitrade']
    item_out.item_name = '%s %s %s' % ( container_in['name'],
                                        container_in['color'],
                                        container_in['rarity'] )
    # Clean name
    item_out.item_name = string_clean( item_out.item_name ).title()
    return item_out


def add_list(list_in: list, item_in: SingleItem) -> None:
    """ Appends to list_in while double adding if NC """
    list_in.append(item_in)

    for key in NC_DICT.keys():
        if item_in.item_name in NC_DICT[key]:
            # Assigns NC traits before re-appending
            item_in.item_name = key
            item_in.is_multitrade = True
            list_in.append(item_in)


def get_item(database_in: ItemDatabase, want_container: list, has_container: list) -> (list, list):
    """ The main driver that does everything for this file
        Processes the poster's intentions to get the inherent value of an item """
    cost_list = list()
    price_list = list()

    # Processing if user requests 1:1 trade
    if len(has_container) == len(want_container):

        for i in range( len(has_container) ):
            # If poster is selling
            if has_container[i]['name'] != 'Credits' and want_container[i]['name'] == 'Credits':
                container = has_container
                value = want_container[i]['count'] / has_container[i]['count']

            # If poster buying
            elif has_container[i]['name'] == 'Credits' and want_container[i]['name'] != 'Credits':
                container = want_container
                value = has_container[i]['count'] / want_container[i]['count']

            # If pickle exists, use existing database to get potential value through multiple trades
            else:
                container = has_container
                container[i]['is_multitrade'] = True
                value = database_in.get_cost(want_container[i]['name'])
                if value == -1 or value == MAX_VALUE:
                    continue

            # Assign values to item
            poster_item = container2item(container[i])
            poster_item.item_value = round(value, 1)
            comment = poster_item.comment.lower()

            # Check if NC is desired, and change item_name to NC if it is
            if container is has_container:
                if 'not ' in comment:
                    break
                for nc_keyword in NC_KEYWORDS:
                    if nc_keyword in comment:
                        # Last word will always be type, so use this to associate to NC type
                        original_type = poster_item.item_name.split()[-1]
                        for key in NC_DICT.keys():
                            if original_type in key:
                                poster_item.item_name = key

            # Exclude certain types of items before appending
            if poster_item.item_name not in EXCLUDE_LIST and poster_item.item_value != 1:
                if container is has_container:
                    add_list(cost_list, poster_item)
                elif container is want_container:
                    price_list.append(poster_item)

    # Requests for single 1:N trade or one each trade
    elif len(has_container) == 1 and has_container[0]['name'] == 'Credits':
        comment = has_container[0]['comment'].lower()
        divide_amount = 1

        if 'all' in comment:
            divide_amount = len(want_container)

        for i in range( len(want_container) ):
            value = has_container[0]['count'] / want_container[i]['count'] / float(divide_amount)
            poster_item = container2item(want_container[i])
            poster_item.item_value = round(value, 1)

            # Check if NC is desired, and change item_name to NC if it is
            for nc_keyword in NC_KEYWORDS:
                if 'not ' in comment:
                    break
                if nc_keyword in comment:
                    # Last word will always be type, so use this to associate to NC type
                    original_type = poster_item.item_name.split()[-1]
                    for key in NC_DICT.keys():
                        if original_type in key:
                            poster_item.item_name = key

            # Exclude certain types of items before appending
            if poster_item.item_name not in EXCLUDE_LIST and poster_item.item_value != 1:
                price_list.append(poster_item)

    # Requests for single 1:N trade or one each trade
    elif len(want_container) == 1 and want_container[0]['name'] == 'Credits':
        comment = want_container[0]['comment'].lower()
        divide_amount = 1

        if 'all' in comment:
            divide_amount = len(want_container)

        for i in range( len(has_container) ):
            value = want_container[0]['count'] / has_container[i]['count'] / float(divide_amount)
            poster_item = container2item(has_container[i])
            poster_item.item_value = round(value, 1)

            # Exclude certain types of items before appending
            if poster_item.item_name not in EXCLUDE_LIST and poster_item.item_value != 1:
                add_list(cost_list, poster_item)

    else:
        # Add NLP and others methods later
        pass

    return [cost_list, price_list]
