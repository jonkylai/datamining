

def in_list(source_in: str, list_in: list) -> bool:
    """ Check if string already exists in list of lists with source string """
    for item_list in list_in:
        if source_in in item_list:
            return True
    return False
