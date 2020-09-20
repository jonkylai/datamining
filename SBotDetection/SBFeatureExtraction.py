from SBUtil import in_dict
from SBParse import is_private, get_summary, get_number, get_comment_count, get_sidebar, get_avatar, get_hour, get_comment, get_rep
import pickle
import os
import time

from bs4 import BeautifulSoup
from math import log


HUMAN_DIR = 'savedhumans'
BOT_DIR = 'savedbots'
HUMAN_PICKLE = 'steam_human.p'
BOT_PICKLE = 'steam_bot.p'


def calc_num(string_in: str) -> dict:
    """ Create dictionary with frequency of each word """
    dict_out = dict()
    word_list = string_in.split()

    # Create dictionary with zero counts for each word
    dict_out = dict.fromkeys(set(word_list), 0)
    for word in word_list:
        dict_out[word] += 1
    return dict_out


def calc_tf(dict_in: dict) -> dict:
    """ Compute term frequency
        tf_ij = n_ij / sum(n_ij)"""
    dict_out = dict(dict_in)

    # Normalize values
    length = len(dict_in)
    for word, count in dict_in.items():
        dict_out[word] = count / float(length)
    return dict_out


def calc_idf(list_in: list) -> dict:
    """ Compute inverse data frequency
        idf = log( N / df )"""
    N = len(list_in)

    dict_out = dict.fromkeys(list_in[0].keys(), 0)
    for document in list_in:
        for word, val in document.items():
            if val > 0:
                dict_out[word] += 1

    for word, val in dict_out.items():
        dict_out[word] = log(N / float(val))
    return dict_out


def main():
    """ Do same tasks for both human and bot list """
    steam_list = [ [HUMAN_PICKLE, HUMAN_DIR],
                   [BOT_PICKLE,   BOT_DIR] ]
    #steam_list = [ ['steam_tmp.p', 'savedata'] ]

    benchmark_time = time.time()

    for fetch_list in steam_list:
        fetch_pickle = fetch_list[0]
        fetch_dir = fetch_list[1]

        """ Load previously loaded data if it exists """
        #if os.path.exists(fetch_pickle):
        #    steam_data = pickle.load(open(fetch_pickle, 'rb'))
        #else:
        #    steam_data = list()
        steam_data = list()

        """ Read list of Steam accounts and stores their features """
        for local_file in os.listdir(fetch_dir):
            if in_dict(local_file, steam_data):
                continue

            fetch_dict = dict()

            # Read data
            source = '%s/%s' % (fetch_dir, local_file)
            f = open(source, 'r', encoding='utf-8')
            content = f.readlines()
            content = '\n'.join(content)
            f.close()

            page_soup = BeautifulSoup(content, 'html.parser')

            # Skip accounts that are kept private
            if not is_private(page_soup):
                fetch_dict['source'] = local_file

                fetch_dict['avatar'] = get_avatar(page_soup)
                fetch_dict['level'] = get_number(page_soup, 'persona_level')

                fetch_dict['summary'] = get_summary(page_soup, 'profile_summary')

                fetch_dict['games'] = get_sidebar(page_soup, 'Games')
                fetch_dict['inventory'] = get_sidebar(page_soup, 'Inventory')
                fetch_dict['screenshots'] = get_sidebar(page_soup, 'Screenshots')
                fetch_dict['videos'] = get_sidebar(page_soup, 'Videos')
                fetch_dict['workshop'] = get_sidebar(page_soup, 'Workshop Items')
                fetch_dict['reviews'] = get_sidebar(page_soup, 'Reviews')
                fetch_dict['guides'] = get_sidebar(page_soup, 'Guides')
                fetch_dict['artwork'] = get_sidebar(page_soup, 'Artwork')

                fetch_dict['groups'] = get_number(page_soup, 'profile_group_links')
                fetch_dict['friends'] = get_number(page_soup, 'profile_friend_links')

                fetch_dict['hour_list'] = get_hour(page_soup)

                fetch_dict['stamp_list'] = get_comment(page_soup, 'commentthread_comment_timestamp')
                fetch_dict['comment_list'] = get_comment(page_soup, 'commentthread_comment_text')
                fetch_dict['comment_count'] = get_comment_count(page_soup, 'commentthread_area')

                fetch_dict['bad_rep'] = get_rep('bad', fetch_dict['comment_list'])
                fetch_dict['good_rep'] = get_rep('good', fetch_dict['comment_list'])

                #word_num = calc_num(fetch_dict['summary'])
                #term_freq = calc_tf(word_num)
                #print(term_freq)
                #idf = calc_idf([word_num])
                #print(idf)
                #exit()

                steam_data.append(fetch_dict)
                print('Done reading \"%s\"' % local_file)

        print('--- %0.4f sec --- Total time' % (time.time() - benchmark_time))

        pickle.dump(steam_data, open(fetch_pickle, 'wb'))

        print( '%s has %i entries' % (fetch_pickle, len(steam_data)) )


if __name__ == "__main__":
    main()