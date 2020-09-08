from pandas import DataFrame
from RLDatabase import ItemDatabase
from RLUtil import MAX_VALUE, DESC_USERNAME_IND, BLACKLIST_FILE


def spam_filter(db_in: ItemDatabase, df_in: DataFrame) -> ItemDatabase:
    """ Uses various methods to filter out bots """
    # Declare return variable
    db_out = db_in
    username_list = list()

    """ Blacklist method:
        Using data from DetectSteamBot, exclude any usernames generated from it """
    with open(BLACKLIST_FILE, 'r') as f:
        for line in f.readlines():
            # Get first character except when line is empty
            try:
                first_char = line[0]
            except IndexError:
                first_char = '#'

            # Ignore comments and non username format
            if first_char == 'h':
                username_list.append(line.strip())

    """ Too-good-to-be-true method:
        If any username has greater than N number of items over M gains """
    gain_dict = dict()

    i = 0
    gain = df_in.iloc[0]['Possible Gain']
    # Repeated gains of more than 100 are suspect
    while gain > 100:
        # Store cost post
        username = df_in.iloc[i]['Cost Info 0'][DESC_USERNAME_IND]
        if username not in gain_dict.keys():
            gain_dict[username] = 1
        else:
            gain_dict[username] += 1

        # Store price post
        username = df_in.iloc[i]['Price Info 0'][DESC_USERNAME_IND]
        if username not in gain_dict.keys():
            gain_dict[username] = 1
        else:
            gain_dict[username] += 1

        gain = df_in.iloc[i]['Possible Gain']
        i += 1

    # Store database of bots by username
    for username in gain_dict:
        # Greater than 6 suspect items are flagged as a bot
        if gain_dict[username] > 6:
            username_list.append(username)

    """ Remove all usernames that have been stored by method above
        Not all usernames will exist, so calls to remove_username() can do nothing """
    for username in username_list:
        db_out.remove_username(username)

    return db_out


