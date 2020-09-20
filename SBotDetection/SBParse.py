from bs4 import BeautifulSoup


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


def is_private(soup_in: BeautifulSoup) -> bool:
    """ Checks if the account is private """
    text = soup_in.find_all(class_='private_profile')
    if len(text) > 0:
        return True
    else:
        return False


def get_summary(soup_in: BeautifulSoup, class_in: str) -> str:
    """ Get account summary from class name in soup """
    text = soup_in.find_all(class_=class_in)
    try:
        text_out = text[0].text.strip()
    except:
        text_out = 'NULL'
    
    if text_out == 'No information given.':
        return 'NULL'
    else:
        return text_out


def get_number(soup_in: BeautifulSoup, class_in: str) -> int:
    """ Get second value after text from class name in soup """
    text = soup_in.find_all(class_=class_in)
    try:
        return int(text[0].text.split()[1])
    except:
        return -1


def get_comment_count(soup_in: BeautifulSoup, class_in: str) -> int:
    """ Get number of comments on account profile in soup """
    text = soup_in.find_all(class_=class_in)
    try:
        text_split = text[0].text.split()
    except:
        return -1

    # First line should be "View all ## comments", otherwise do not store number
    if text_split[0] == 'View' and text_split[1] == 'all':
        number = text_split[2]
        # Remove commas before converting to int
        return int(''.join(number.split(',')))
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
        comment_list.append(text.text.lower().strip())
    return comment_list


def get_rep(type_in: str, comment_in: list) -> int:
    """ Counts the number of comments that are positive or negative """
    count_out = 0

    for comment in comment_in:
        if type_in == 'good' and '+rep' in comment:
            count_out += 1
        elif type_in == 'bad' and ('-rep' in comment or 'scam' in comment):
            count_out += 1

    return count_out


