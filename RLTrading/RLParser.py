from RLUtil import int_cast, MAX_VALUE
from bs4 import BeautifulSoup

import copy


def get_link(soup_text: BeautifulSoup) -> str:
    """ Grabs the link so items are traceable """
    search_text = '/trade/'
    for line in soup_text.prettify().split():
        if search_text in line:
            return 'https://rocket-league.com%s' % line.split('\"')[1]

    print('ERROR: Cannot find "%s" in soup_text' % search_text)
    exit()


def get_username(soup_text: BeautifulSoup) -> str:
    """ Grabs username for spam filtering """
    return soup_text.text.strip()


def get_comment(soup_text: BeautifulSoup) -> str:
    """ Grabs poster note for NLP """
    return soup_text.text.strip()


def get_item(want_containers: list, has_containers: list) -> (list, list):
    """ Processes the poster's intentions to get the inherent value of an item """
    cost_list = list()
    price_list = list()

    # Processing if user requests 1:1 trade
    if len(has_containers) == len(want_containers):

        for i in range( len(has_containers) ):
            # Create empty item
            poster_item = dict( name        = '',
                                description = '',
                                value       = -MAX_VALUE )
            poster_item['link'] = has_containers[i]['link']

            # If poster is selling
            if has_containers[i]['name'] != 'Credits' and want_containers[i]['name'] == 'Credits':
                poster_item['name'] = '%s %s %s' % ( has_containers[i]['name'],
                                                     has_containers[i]['color'],
                                                     has_containers[i]['rarity'] )

                poster_item['description'] = [ has_containers[i]['link'],
                                               has_containers[i]['username'],
                                               has_containers[i]['comment'] ]

                # Remove extra white space
                poster_item['name'] = ' '.join( poster_item['name'].split() )
                # Divide if poster requests multiple items
                poster_item['value'] = round(want_containers[i]['count'] / has_containers[i]['count'], 1)

                cost_list.append(poster_item)

            # If poster buying
            if has_containers[i]['name'] == 'Credits' and want_containers[i]['name'] != 'Credits':
                poster_item['name'] = '%s %s %s' % ( want_containers[i]['name'],
                                                     want_containers[i]['color'],
                                                     want_containers[i]['rarity'] )

                poster_item['description'] = [ want_containers[i]['link'],
                                               want_containers[i]['username'],
                                               want_containers[i]['comment'] ]

                # Remove extra white space
                poster_item['name'] = ' '.join( poster_item['name'].split() )
                # Divide if poster requests multiple items
                poster_item['value'] = round(has_containers[i]['count'] / want_containers[i]['count'], 1)

                price_list.append(poster_item)

            else:
                pass

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
                            link  = '',
                            username = '',
                            comment = '' )
    name_flag = False
    cert_flag = False
    amount_flag = False

    for line in soup_text.prettify().split('\n'):

        # Rarity keyword
        if 'rlg-item__gradient' in line:
            # Initialize because this is the first keyword for each item
            container_list.append( copy.deepcopy(empty_container) )
            container_list[-1]['link'] = link_in
            container_list[-1]['username'] = username_in
            container_list[-1]['comment'] = comment_in
            # Assign rarity
            container_list[-1]['rarity'] = line.split('--')[-1].split('\"')[0]

        # Color keyword
        elif 'rlg-item__paint' in line:
            container_list[-1]['color'] = line.split('data-name=\"')[-1].split('\"')[0]

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

