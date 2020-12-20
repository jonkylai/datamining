import re


def in_list(source_in: str, list_in: list) -> bool:
    """ Check if string already exists in list of lists with source string """
    for item_list in list_in:

        # True if in list
        if source_in in item_list:
            return True

    # Otherwise false to append
    return False


def string_clean(text_in: str) -> str:
    """ Clean strings to be used for language processing """
    text_out = re.sub('[^ A-Za-z0-9+-_]', '', text_in)
    return text_out
