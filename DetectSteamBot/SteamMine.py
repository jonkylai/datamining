import pickle
import os
import time
import requests

from bs4 import BeautifulSoup


HUMAN_FILE = 'truthlist.txt'
BOT_FILE = 'blacklist.txt'
HUMAN_PICKLE = 'steam_human.p'
BOT_PICKLE = 'steam_bot.p'


def get_accounts(file_in: str) -> list:
    """ Return list of accounts to mine """
    accounts_out = list()

    with open(file_in, 'r') as f:
        for line in f.readlines():
            # Get first character except when line is empty
            try:
                first_char = line[0]
            except IndexError:
                first_char = '#'

            # Stop reading once ignore list is reached
            if '# Ignore list' in line:
                break

            # Ignore comments and non account format
            if first_char == 'h':
                accounts_out.append(line.strip())

    return accounts_out


def get_summary(soup_in: BeautifulSoup, class_in: str) -> str:
    """ Get account summary from class name in soup """
    text = soup_in.find_all(class_=class_in)
    try:
        return text[0].text.strip()
    except:
        return 'NULL'


def get_count(soup_in: BeautifulSoup, class_in: str) -> int:
    """ Get second value after text from class name in soup """
    text = soup_in.find_all(class_=class_in)
    try:
        return int(text[0].text.split()[1])
    except:
        return -1


def get_sidebar(soup_in: BeautifulSoup, label_in: str) -> int:
    """ Get sidebar count from label name in soup """
    count_soup = soup_in.find_all('div', {'class': 'profile_item_links'})
    try:
        count_list = count_soup[0].text.split()
    except:
        print('ERROR: Could not find profile item links')
        exit()

    for i, val in enumerate(count_list):
        if label_in == val and len(count_list) > i:
            try:
                return int(count_list[i+1])
            except:
                break
    return -1


def get_avatar(soup_in: BeautifulSoup) -> str:
    """ Get account avatar picture from soup """
    text = soup_in.find_all('div', {'class': 'playerAvatarAutoSizeInner'})
    if len(text) == 0:
        print('ERROR: Could not get avatar picture')
        exit()

    # Loop through all images where last image is the actual avatar picture
    for line in text[0].prettify().split('\n'):
        if 'src' in line:
            string_out = get_text_between(line, 'src=\"', '\"')
    return string_out


def get_hour(soup_in: BeautifulSoup) -> list:
    text_list = soup_in.find_all('div', {'class': 'game_info_details'})

    hour_list = list()
    for text in text_list:
        try:
            # Where the 3rd item should be hrs on record
            hours = text.prettify().split()[2]
            # Where numbers greater than 3 digits have commas
            hour_list.append( float( hours.replace(',','') ) )
        except:
            print('ERROR: Cannot get hours played from account')
            exit()

    return hour_list


def get_comment(soup_in: BeautifulSoup, class_in: str) -> list:
    """ Get comment date or text from account """
    text_list = soup_in.find_all(class_=class_in)

    comment_list = list()
    for text in text_list:
        comment_list.append(text.text.strip())
    return comment_list


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


def in_dict(url_in: str, dictionary_list: list) -> bool:
    """ Check if string already exists in dictionary with url key """
    for dictionary in dictionary_list:
        if url_in == dictionary['url']:
            return True
    return False


def main():
    """ Do same tasks for both human and bot list """
    steam_list = [ [HUMAN_PICKLE, HUMAN_FILE],
                   [BOT_PICKLE,   BOT_FILE] ]

    """ Load previously loaded data if it exists """
    for fetch_list in steam_list:
        fetch_pickle = fetch_list[0]
        fetch_file = fetch_list[1]

        if os.path.exists(fetch_pickle):
            steam_data = pickle.load(open(fetch_pickle, 'rb'))
        else:
            steam_data = list()

        """ Read list of Steam accounts and stores the data """
        url_list = get_accounts(fetch_file)

        for url in url_list:
            if in_dict(url, steam_data):
                continue

            fetch_dict = dict()

            # Benchmark requests.get() speed
            time_page = time.time()
            page = requests.get(url)
            print('--- %0.4f sec --- %s' % (time.time() - time_page, page.url))

            time_page = time.time()
            page_soup = BeautifulSoup(page.content, 'html.parser')

            fetch_dict['url'] = url

            fetch_dict['avatar'] = get_avatar(page_soup)
            fetch_dict['level'] = get_count(page_soup, 'persona_level')

            fetch_dict['summary'] = get_summary(page_soup, 'profile_summary')

            fetch_dict['games'] = get_sidebar(page_soup, 'Games')
            fetch_dict['inventory'] = get_sidebar(page_soup, 'Inventory')
            fetch_dict['screenshots'] = get_sidebar(page_soup, 'Screenshots')
            fetch_dict['videos'] = get_sidebar(page_soup, 'Videos')
            fetch_dict['workshop'] = get_sidebar(page_soup, 'Workshop Items')
            fetch_dict['reviews'] = get_sidebar(page_soup, 'Reviews')
            fetch_dict['guides'] = get_sidebar(page_soup, 'Guides')
            fetch_dict['artwork'] = get_sidebar(page_soup, 'Artwork')

            fetch_dict['groups'] = get_count(page_soup, 'profile_group_links')
            fetch_dict['friends'] = get_count(page_soup, 'profile_friend_links')

            fetch_dict['hour_list'] = get_hour(page_soup)

            fetch_dict['stamp_list'] = get_comment(page_soup, 'commentthread_comment_timestamp')
            fetch_dict['comment_list'] = get_comment(page_soup, 'commentthread_comment_text')

            steam_data.append(fetch_dict)

        pickle.dump(steam_data, open(fetch_pickle, 'wb'))

        print( '%s has %i entries' % (fetch_pickle, len(steam_data)) )

if __name__ == "__main__":
    main()
