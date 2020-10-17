from RLUtil import Query


""" Main method of searching is using Optimize logic
    This will grab all most recent posts and compare them with itself """
optimize = Query()
optimize.key = 'Optimize Monitoring'
optimize.action = 'Optimize'
optimize.monitor_mode = True
optimize.url = 'https://rocket-league.com/trading?filterItem=2615&filterPlatform=1&filterSearchType=0&filterCertification=0&filterPaint=0&filterItemType=0&filterPlatform%5B%5D=1'
optimize.url = 'https://rocket-league.com/trading?filterItem=2615&filterCertification=0&filterPaint=0&filterMinCredits=0&filterMaxCredits=100000&filterPlatform%5B%5D=1&filterSearchType=0&filterItemType=0'

""" Any custom items that are of interest can be added here """
splash = Query()
splash.key = 'Big Splash Limited'
splash.action = 'Watch'
splash.url = optimize.url.replace('=2615', '=1975')

gravity = Query()
gravity.key = 'Gravity Bomb Black-Market'
gravity.action = 'Watch'
gravity.url = optimize.url.replace('=2615', '=2948')

""" From pickle save all steam accounts to SBotDetection """
mine_steam = Query()
mine_steam.key = 'Data Mine'
mine_steam.action = 'Data Mine'

""" Delete pickle and optimize """
delete_pickle = Query()
delete_pickle.key = 'Delete Pickle'
delete_pickle.action = 'Delete Pickle'
delete_pickle.monitor_mode = True
delete_pickle.url = optimize.url

""" Most important query which searches by user input
    Locally generated web page links will contain examples as well """
single_query = Query()
single_query.action = 'Single'


all_queries = [ optimize, delete_pickle, mine_steam, splash, gravity ]

