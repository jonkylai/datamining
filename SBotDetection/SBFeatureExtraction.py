from SBParser import is_private, get_summary, get_number, get_comment_count, get_sidebar, get_avatar, get_hour, get_comment, get_rep
from SBUtil import in_list, string_clean

import numpy as np
import pickle
import os
import time

from bs4 import BeautifulSoup
from math import log


""" Note that bot labels are synonymous to phishing labels
    Most scammers use a hybrid of bot and human phishing scam """
HUMAN_DIR = 'savedhumans'
BOT_DIR = 'savedbots'
TEST_DIR = 'savedtest'
HUMAN_PICKLE = 'steam_human.p'
BOT_PICKLE = 'steam_bot.p'
TEST_PICKLE = 'steam_test.p'


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
    """ Compute inverse document frequency
        idf = log( N / df )"""
    N = len(list_in)

    all_keys = set().union(*list_in)
    dict_out = dict.fromkeys(all_keys, 0)
    for document in list_in:
        for word, val in document.items():
            if val > 0:
                dict_out[word] += 1

    for word, val in dict_out.items():
        dict_out[word] = log(N / float(val))
    return dict_out


def dict2list(dict_in: dict) -> list:
    """ Convert dictionary to list
        First item will be bot classification. Other keys will be sorted """
    list_out = list()
    list_out.append(dict_in['bot'])

    key_list = sorted(dict_in.keys(), key=lambda x: x.lower())
    key_list.remove('bot')
    for key in key_list:
        list_out.append(dict_in[key])
    return list_out


def main():
    """ Do same tasks for both human and bot list """
    steam_list = [ [HUMAN_PICKLE, HUMAN_DIR],
                   [BOT_PICKLE,   BOT_DIR],
                   [TEST_PICKLE,  TEST_DIR] ]

    benchmark_time = time.time()
    total_entries = 0

    for fetch_list in steam_list:
        fetch_pickle = fetch_list[0]
        fetch_dir = fetch_list[1]

        """ Load previously loaded data if it exists """
        if os.path.exists(fetch_pickle):
            steam_data = pickle.load(open(fetch_pickle, 'rb'))
        else:
            steam_data = list()

        # Force reload (should be removed for larger data sets)
        steam_data = list()

        """ Read list of Steam accounts and stores their features """
        steam_dicts = list()
        for local_file in os.listdir(fetch_dir):

            # Skip if file already processed
            if in_list(local_file, steam_data) or 'Community __ Error.html' in local_file:
                continue

            # Read data
            source = '%s/%s' % (fetch_dir, local_file)
            f = open(source, 'r', encoding='utf-8')
            content = f.readlines()
            content = '\n'.join(content)
            f.close()

            fetch_dict = dict()
            page_soup = BeautifulSoup(content, 'html.parser')

            # Skip accounts that are kept private
            if not is_private(page_soup):
                print('Reading \"%s\"' % local_file)

                fetch_dict['source'] = local_file

                # Classification: either supervised or labeled as -1
                if fetch_dir == BOT_DIR:
                    fetch_dict['bot'] = 1
                elif fetch_dir == HUMAN_DIR:
                    fetch_dict['bot'] = 0
                else:
                    fetch_dict['bot'] = -1

                # Unused features
                avatar = get_avatar(page_soup)
                stamp_list = get_comment(page_soup, 'commentthread_comment_timestamp')

                # General count features
                fetch_dict['level'] = get_number(page_soup, 'persona_level')

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
                fetch_dict['comment_count'] = get_comment_count(page_soup, 'commentthread_area')

                hour_list = get_hour(page_soup)
                fetch_dict['total_hour'] = sum(hour_list)

                comment_list = get_comment(page_soup, 'commentthread_comment_text')
                bad_rep = get_rep('bad', comment_list)
                good_rep = get_rep('good', comment_list)

                # Combine summary and comment_list
                summary = get_summary(page_soup, 'profile_summary')
                summary += ' '.join(comment_list)
                fetch_dict['summary'] = string_clean(summary)

                # Assign bot labels for testing, since rep feature is highly correlated to bot
                if fetch_dir == TEST_DIR:
                    if bad_rep == 0 and good_rep > 1:
                        fetch_dict['bot'] = 0
                    else:
                        fetch_dict['bot'] = 1

                steam_dicts.append(fetch_dict)

        # Calculate TF-IDF
        document_list = list()

        print("Creating term_freq key for each profile")
        for item_dict in steam_dicts:
            # Add term frequency key
            word_dict = calc_num(item_dict['summary'])
            term_freq_dict = calc_tf(word_dict)
            item_dict['term_freq'] = term_freq_dict
            # Add to total document list
            document_list.append(word_dict)

        if len(document_list) != 0:
            print("Adding tfidf_%%s key for each profile")
            # THIS PART IS TOO MEMORY INTENSIVE, FIND A BETTER WAY

            all_keys = set().union(*document_list)

            idf_dict = calc_idf(document_list)

            for item_dict in steam_dicts:
                # Store TF-IDF calculation
                for word in all_keys:
                    new_key = 'tfidf_%s' % word
                    if word in item_dict['term_freq']:
                        item_dict[new_key] = item_dict['term_freq'][word] * idf_dict[word]
                    else:
                        item_dict[new_key] = 0.00001

                # Remove term frequency from dict
                item_dict.pop('term_freq', None)
        else:
            print("Skipping TF-IDF because documents do not exist")

        # Convert dictionary to list before appending to data
        for item_dict in steam_dicts:
            steam_data.append(dict2list(item_dict))

        print('--- %0.4f sec --- Total time' % (time.time() - benchmark_time))

        pickle.dump(steam_data, open(fetch_pickle, 'wb'))

        steam_length = len(steam_data)
        print( '%s has %i entries' % (fetch_pickle, steam_length) )
        total_entries += steam_length

    print('Total number of entries = %i' % total_entries)


if __name__ == "__main__":
    main()
