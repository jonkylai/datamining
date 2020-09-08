from RLUtil import Query


""" Main method of searching is using Optimize logic
    This will grab all most recent posts and compare them with itself """
optimize = Query()
optimize.key = 'Optimize All'
optimize.action = 'Optimize'
optimize.max_search = 10
optimize.url = 'https://rocket-league.com/trading?filterItem=2615&filterPlatform=1&filterSearchType=0&filterCertification=0&filterPaint=0&filterItemType=0'

""" Any custom items that are of interest can be added here """
splash = Query()
splash.key = 'Big Splash limited'
splash.action = 'Watch'
splash.max_search = 2
splash.url = 'https://rocket-league.com/trading?filterItem=1975&filterPlatform=1&filterSearchType=0&filterCertification=N&filterPaint=N&filterItemType=0'

""" Most important query which searches by user input
    Locally generated web page links will contain examples as well """
single_query = Query()
single_query.action = 'Single'
single_query.max_search = 2
single_query.url = None


all_queries = [ optimize, splash ]
