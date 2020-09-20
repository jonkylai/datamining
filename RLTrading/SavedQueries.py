from RLUtil import Query


""" Main method of searching is using Optimize logic
    This will grab all most recent posts and compare them with itself """
optimize = Query()
optimize.key = 'Optimize All'
optimize.action = 'Optimize'
optimize.max_search = 15
optimize.url = 'https://rocket-league.com/trading?filterItem=2615&filterPlatform=1&filterSearchType=0&filterCertification=0&filterPaint=0&filterItemType=0'

""" Any custom items that are of interest can be added here """
splash = Query()
splash.key = 'Big Splash Limited'
splash.action = 'Watch'
splash.max_search = 2
splash.url = 'https://rocket-league.com/trading?filterItem=1975&filterPlatform=1&filterSearchType=0&filterCertification=N&filterPaint=N&filterItemType=0'

gravity = Query()
gravity.key = 'Gravity Bomb Black-Market'
gravity.action = 'Watch'
gravity.max_search = 2
gravity.url = 'https://rocket-league.com/trading?filterItem=2948&filterPlatform=1&filterSearchType=0&filterCertification=N&filterPaint=N&filterItemType=0'

""" From pickle save all steam accounts to SBotDetection """
mine_steam = Query()
mine_steam.key = 'Data Mine'
mine_steam.action = 'Data Mine'

""" Do nothing and delete pickle """
delete_pickle = Query()
delete_pickle.key = 'Delete Pickle'
delete_pickle.action = 'Delete Pickle'

""" Most important query which searches by user input
    Locally generated web page links will contain examples as well """
single_query = Query()
single_query.action = 'Single'
single_query.max_search = 2


all_queries = [ optimize, delete_pickle, mine_steam, splash, gravity ]


