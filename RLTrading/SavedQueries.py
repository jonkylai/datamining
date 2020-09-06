from RLUtil import Query


optimize = Query()
optimize.key = 'Optimize All'
optimize.action = 'Optimize'
optimize.max_search = 12
optimize.url = 'https://rocket-league.com/trading?filterItem=2615&filterPlatform=1&filterSearchType=0&filterCertification=0&filterPaint=0&filterItemType=0'

splash = Query()
splash.key = 'Big Splash limited'
splash.action = 'Watch'
splash.max_search = 2
splash.url = 'https://rocket-league.com/trading?filterItem=1975&filterPlatform=1&filterSearchType=0&filterCertification=N&filterPaint=N&filterItemType=0'

single_query = Query()
single_query.action = 'Single'
single_query.max_search = 2
single_query.url = None

all_queries = [ optimize, splash ]
