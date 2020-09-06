import time
import requests

from bs4 import BeautifulSoup


HUMAN_FILE = 'truthlist.txt'
BOT_FILE = 'blacklist.txt'


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


def main():
    """ Read list of Steam accounts and stores the data """
    human_list = get_accounts(HUMAN_FILE)
    bot_list = get_accounts(BOT_FILE)

    for url in human_list:

        # Benchmark requests.get() speed
        time_page = time.time()
        page = requests.get(url)
        print('--- %0.4f sec --- %s' % (time.time() - time_page, page.url))

        # Benchmark soup speed
        time_page = time.time()
        page_soup = BeautifulSoup(page.content, 'html.parser')

        avatar = get_avatar(page_soup)
        level = get_count(page_soup, 'persona_level')
        summary = get_summary(page_soup, 'profile_summary')
        count_games = get_sidebar(page_soup, 'Games')
        count_inventory = get_sidebar(page_soup, 'Inventory')
        count_screenshots = get_sidebar(page_soup, 'Screenshots')
        count_videos = get_sidebar(page_soup, 'Videos')
        count_workshop = get_sidebar(page_soup, 'Workshop Items')
        count_reviews = get_sidebar(page_soup, 'Reviews')
        count_guides = get_sidebar(page_soup, 'Guides')
        count_artwork = get_sidebar(page_soup, 'Artwork')
        count_groups = get_count(page_soup, 'profile_group_links')
        count_friends = get_count(page_soup, 'profile_friend_links')


        # Get account level
        print('--- %0.4f sec --- soup time' % (time.time() - time_page))
        print(level)
        print(avatar)
        print(summary)
        print(count_games, count_inventory, count_screenshots, count_videos, count_workshop, count_reviews, count_guides, count_artwork)
        print(count_groups, count_friends)

        exit()


if __name__ == "__main__":
    main()
