from RLDatabase import SingleItem
from RLUtil import string_clean


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
    item_out.item_name = '%s %s %s' % ( container_in['name'],
                                        container_in['color'],
                                        container_in['rarity'] )
    # Clean name
    item_out.item_name = string_clean( item_out.item_name ).title()
    return item_out


def get_item(want_container: list, has_container: list) -> (list, list):
    """ Processes the poster's intentions to get the inherent value of an item """
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

            # Do not append if criteria not met
            else:
                continue

            # Assign values to item
            poster_item = container2item(container[i])
            poster_item.item_value = round(value, 1)

            # Exclude certain types of items before appending
            if 'Offer' not in poster_item.item_name:
                if container is has_container:
                    cost_list.append(poster_item)
                elif container is want_container:
                    price_list.append(poster_item)

    # Requests for single 1:N trade or one each trade
    elif len(has_container) == 1 and has_container[0]['name'] == 'Credits':
        comment = has_container[0]['comment']
        divide_amount = 1

        if 'all' in comment:
            divide_amount = len(want_container)

        for i in range( len(want_container) ):
            value = has_container[0]['count'] / want_container[i]['count'] / float(divide_amount)
            poster_item = container2item(want_container[i])
            poster_item.item_value = round(value, 1)

            # Exclude certain types of items before appending
            if 'Offer' not in poster_item.item_name:
                price_list.append(poster_item)

    # Requests for single 1:N trade or one each trade
    elif len(want_container) == 1 and want_container[0]['name'] == 'Credits':
        comment = want_container[0]['comment']
        divide_amount = 1

        if 'all' in comment:
            divide_amount = len(want_container)

        for i in range( len(has_container) ):
            value = want_container[0]['count'] / has_container[i]['count'] / float(divide_amount)
            poster_item = container2item(has_container[i])
            poster_item.item_value = round(value, 1)

            # Exclude certain types of items before appending
            if 'Offer' not in poster_item.item_name:
                cost_list.append(poster_item)

    else:
        # Add NLP and others methods later
        pass

    return [cost_list, price_list]
