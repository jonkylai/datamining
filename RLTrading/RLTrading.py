from RLUtil import *
from SavedQueries import *


def main():
    # Create list of query options
    query_list = all_queries
    query_length = len(query_list)

    # Print options
    print('Existing queries:')
    for i in range(query_length):
        print( '%i. %s' % (i + 1, query_list[i].name) )

    # Prompt user
    user_input = input('Enter query: ')
    try:
        user_input = int(user_input)
    except ValueError:
        user_input = -1

    user_query = None
    for i in range(query_length):
        if user_input == i + 1:
            user_query = query_list[i]

    # Add functionality later
    if user_query is None:
        exit()

    results = RLTrades(user_query)

    return 0


if __name__ == "__main__":
    main()

