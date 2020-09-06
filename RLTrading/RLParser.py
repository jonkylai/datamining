from RLUtil import int_cast, BASE_URL, MAX_VALUE
from bs4 import BeautifulSoup

import copy


def get_text_between(string_in: str, begin_in: str, end_in: str) -> str:
    """ Parses text by stripping text before and after
        Error checking included """
    try:
        string_out = string_in.split(begin_in)[-1]
        string_out = string_out.split(end_in)[0]
        return string_out
    except:
        print('ERROR: Cannot find %s or %s from input text below' % (begin_in, end_in))
        print('       %s' % string_in)


def get_link(soup_text: BeautifulSoup) -> str:
    """ Grabs the post link so items are traceable """
    search_text = '/trade/'
    for line in soup_text.prettify().split():
        if search_text in line:
            return 'https://rocket-league.com%s' % line.split('\"')[1]

    print('ERROR: Cannot find "%s" in soup_text' % search_text)
    exit()


def get_username(soup_text: BeautifulSoup) -> str:
    """ Grabs username for spam filtering """
    return get_text_between(soup_text.prettify(), 'phishingAware(\'', '\');')


def get_comment(soup_text: BeautifulSoup) -> str:
    """ Grabs poster note for NLP """
    return soup_text.text.strip()


def get_item(want_container: list, has_container: list) -> (list, list):
    """ Processes the poster's intentions to get the inherent value of an item """
    cost_list = list()
    price_list = list()

    # Processing if user requests 1:1 trade
    if len(has_container) == len(want_container):

        for i in range( len(has_container) ):
            # Create empty item
            poster_item = dict( name        = '',
                                description = '',
                                value       = 0 )

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
            poster_item['description'] = [ container[i]['post_link'],
                                           container[i]['item_link'],
                                           container[i]['username'],
                                           container[i]['comment'] ]

            poster_item['value'] = round(value, 1)

            poster_item['name'] = '%s %s %s' % ( container[i]['name'],
                                                 container[i]['color'],
                                                 container[i]['rarity'] )
            # Remove extra white space
            poster_item['name'] = ' '.join( poster_item['name'].split() )

            # Append
            if container is has_container:
                cost_list.append(poster_item)
            elif container is want_container:
                price_list.append(poster_item)

    else:
        # Add NLP and others methods later
        pass

    return [cost_list, price_list]


def get_container(soup_text: BeautifulSoup, link_in: str, username_in: str, comment_in: str) -> list:
    """ Grabs all necessary information from poster container """
    container_list = list()
    # Amount keyword does not exist unless count is not one
    empty_container = dict( name  = '',
                            color = '',
                            rarity = '',
                            count = 1,
                            post_link  = '',
                            username = '',
                            item_link = '',
                            comment = '' )
    name_flag = False
    cert_flag = False
    amount_flag = False

    for line in soup_text.prettify().split('\n'):

        # Item link keyword
        if 'rlg-item --' in line:
            # Initialize because this is the first keyword for each item
            container_list.append( copy.deepcopy(empty_container) )
            container_list[-1]['post_link'] = link_in
            container_list[-1]['username'] = username_in
            container_list[-1]['comment'] = comment_in

            # Assign item link with filter search of zero
            container_list[-1]['item_link'] = '%s%s%s' % ( BASE_URL,
                                                           get_text_between(line, 'href=\"', '\">'),
                                                           '&filterSearchType=0' )

        # Rarity keyword
        if 'rlg-item__gradient' in line:
            container_list[-1]['rarity'] = get_text_between(line, '--', '\"')

        # Color keyword
        elif 'rlg-item__paint' in line:
            container_list[-1]['color'] = get_text_between(line, 'data-name=\"', '\"')

        # Name keyword
        elif 'rlg-item__name' in line:
            name_flag = True
        elif name_flag:
            container_list[-1]['name'] = line.strip()
            name_flag = False

        # Certification keyword
        elif 'rlg-item__cert' in line:
            cert_flag = True
        elif cert_flag:
            # Append certification to name
            container_list[-1]['name'] += ' %s' % line.strip()
            cert_flag = False

        # Amount keyword
        elif 'rlg-item__quantity' in line:
            amount_flag = True
        elif amount_flag:
            container_list[-1]['count'] = int_cast(line)
            amount_flag = False

    return container_list

