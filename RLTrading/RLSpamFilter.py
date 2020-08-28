from pandas import DataFrame
from RLDatabase import ItemDatabase
from RLUtil import MAX_VALUE, LINK_INDEX, USERNAME_INDEX


def spam_filter(db_in: ItemDatabase, df_in: DataFrame) -> ItemDatabase:
    """ Uses various methods to filter out bots """
    # Declare return variable
    db_out = db_in

    """ Too-good-to-be-true method:
        If any username has greater than N number of positive gains over M """
    username_dict = dict()
    link_dict = dict()

    i = 0
    gain = df_in.iloc[0]['Possible Gain']
    # Repeated gains of more than 100 are suspect
    while gain > 100:
        # Store cost post
        username = df_in.iloc[i]['Cost Info 0'][USERNAME_INDEX]
        if username not in username_dict.keys():
            username_dict[username] = 1
        else:
            username_dict[username] += 1
        link_dict[username] = df_in.iloc[i]['Cost Info 0'][LINK_INDEX]

        # Store price post
        username = df_in.iloc[i]['Price Info 0'][USERNAME_INDEX]
        if username not in username_dict.keys():
            username_dict[username] = 1
        else:
            username_dict[username] += 1
        link_dict[username] = df_in.iloc[i]['Price Info 0'][LINK_INDEX]

        gain = df_in.iloc[i]['Possible Gain']
        i += 1

    # Remove database of bots by username
    for username in username_dict:
        # Greater than 4 suspect items are flagged as a bot
        if username_dict[username] > 4:
            db_out.remove_username(username)
            # Print out information
            print('SPAM BOT: %s flagged as a bot %s' % (username, link_dict[username]) )

    return db_out


