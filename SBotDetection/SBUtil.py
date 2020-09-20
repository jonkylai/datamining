

def in_dict(source_in: str, dictionary_list: list) -> bool:
    """ Check if string already exists in dictionary with source key """
    for dictionary in dictionary_list:
        if source_in == dictionary['source']:
            return True
    return False
