import pandas as pd
import re

import requests
from bs4 import BeautifulSoup

from ItemPost import ItemPost

def main():
    splash = { 'filterItem'          : '1975',
               'filterPlatform'      : '1',
               'filterSearchType'    : '1',
               'filterCertification' : 'N',
               'filterPaint'         : 'N',
               'filterItemType'      : '0' }

    page = requests.get( 'https://rocket-league.com/trading', params=splash )
    page_soup = BeautifulSoup( page.content, 'html.parser' )
    has_list  = page_soup.find_all( 'div', {'id' : 'rlg-youritems'}  )
    want_list = page_soup.find_all( 'div', {'id' : 'rlg-theiritems'} )

    # Check if parsing correctly counted number of posts
    if len(has_list) != len(want_list):
        print("ERROR: Length of item_has and item_want do not match")
        exit()

    # Loop over each listing
    for i in range(len(has_list)):
        item_has  = ItemPost( has_list[i] )
        item_want = ItemPost( want_list[i] )
        exit()

if __name__ == "__main__":
    main()