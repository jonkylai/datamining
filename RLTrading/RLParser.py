from RLUtil import int_cast, TIME_FORMAT, BASE_URL, MAX_VALUE
from RLUtil import string_clean
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

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


def get_link(soup_in: BeautifulSoup) -> str:
    """ Grabs the post link so items are traceable """
    text = soup_in.find_all('header', {'class': 'rlg-trade__header'})
    search_text = '/trade/'

    if len(text) > 0:
        for line in text[0].prettify().split():
            if search_text in line:
                return 'https://rocket-league.com%s' % line.split('\"')[1]

    print('ERROR: Cannot find "%s" in soup_text' % search_text)
    exit()


def get_time(soup_in: BeautifulSoup) -> str:
    """ Grabs the post time so old posts can be removed """
    text = soup_in.find_all('header', {'class': 'rlg-trade__header'})
    search_text = 'rlg-trade__time'

    if len(text) > 0:
        line_list = text[0].prettify().split('\n')
        for i, line in enumerate(line_list):
            if search_text in line:
                # Where the time ago string is the 3rd item after searched text
                time_text = line_list[i+2]

                # Convert time ago string to delta time
                time_num = int(time_text.split()[0])
                if 'second' in time_text:
                    delta_time = timedelta(seconds=time_num)
                elif 'minute' in time_text:
                    delta_time = timedelta(minutes=time_num)
                elif 'hour' in time_text:
                    delta_time = timedelta(hours=time_num)
                elif 'day' in time_text:
                    delta_time = timedelta(days=time_num)
                else:
                    print('ERROR: Cannot recognize time from %s' % time_text)
                    exit()

                # Calculate when the post was made
                time_post = datetime.now() - delta_time
                return time_post.strftime(TIME_FORMAT)

    print('ERROR: Cannot find "%s" in soup_text' % search_text)
    exit()


def get_username(soup_in: BeautifulSoup) -> str:
    """ Grabs username for spam filtering """
    text = soup_in.find_all('a', {'class': 'rlg-trade__platform'})
    if len(text) > 0:
        return get_text_between(text[0].prettify(), 'phishingAware(\'', '\');')
    else:
        print('ERROR: Could not find username')
        exit()


def get_comment(soup_in: BeautifulSoup) -> str:
    """ Grabs poster note for NLP """
    text = soup_in.find_all('div', {'class': 'rlg-trade__note'})
    if len(text) > 0:
        return text[0].text.strip()
    else:
        return ''


def get_container(type_in: str, soup_in: BeautifulSoup, link_in: str, time_in: str, username_in: str, comment_in: str) -> list:
    """ Grabs all necessary information from poster container """
    container_list = list()

    # Amount keyword does not exist unless count is not one
    empty_container = dict( name  = '',
                            color = '',
                            rarity = '',
                            count = 1,
                            post_link  = '',
                            post_time  = '',
                            username = '',
                            item_link = '',
                            comment = '' )

    # Parse depending on type input
    if type_in == 'want':
        text = soup_in.find_all('div', {'class': 'rlg-trade__itemswants'})
    elif type_in == 'has':
        text = soup_in.find_all('div', {'class': 'rlg-trade__itemshas'})

    name_flag = False
    cert_flag = False
    amount_flag = False

    for line in text[0].prettify().split('\n'):

        # Item link keyword
        if 'rlg-item --' in line:
            # Initialize because this is the first keyword for each item
            container_list.append( copy.deepcopy(empty_container) )
            container_list[-1]['post_link'] = link_in
            container_list[-1]['post_time'] = time_in
            container_list[-1]['username'] = username_in
            container_list[-1]['comment'] = string_clean(comment_in).lower()

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

