from RLUtil import Query


optimize = Query()
optimize.key = 'Optimize All'
optimize.action = 'Optimize'
optimize.max_search = 15
optimize.params = {'filterItem': '2615',
                   'filterPlatform': '1',
                   'filterSearchType': '0',
                   'filterCertification': '0',
                   'filterPaint': '0',
                   'filterItemType': '0'}

splash = Query()
splash.key = 'Big Splash limited'
splash.action = 'Watch'
splash.max_search = 3
splash.params = {'filterItem': '1975',
                 'filterPlatform': '1',
                 'filterSearchType': '0',
                 'filterCertification': 'N',
                 'filterPaint': 'N',
                 'filterItemType': '0'}

gravity = Query()
gravity.key = 'Gravity Bomb black-market'
gravity.action = 'Watch'
gravity.max_search = 3
gravity.params = {'filterItem': '2948',
                  'filterPlatform': '1',
                  'filterSearchType': '0',
                  'filterCertification': 'N',
                  'filterPaint': 'N',
                  'filterItemType': '0'}

stellar = Query()
stellar.key = 'Interstellar black-market'
stellar.action = 'Watch'
stellar.max_search = 3
stellar.params = {'filterItem': '2944',
                  'filterPlatform': '1',
                  'filterSearchType': '0',
                  'filterCertification': 'N',
                  'filterPaint': 'N',
                  'filterItemType': '0'}

dueling = Query()
dueling.key = 'Tidal Stream black-market'
dueling.action = 'Watch'
dueling.max_search = 3
dueling.params = {'filterItem': '2807',
                  'filterPlatform': '1',
                  'filterSearchType': '0',
                  'filterCertification': 'N',
                  'filterPaint': 'N',
                  'filterItemType': '0'}

single = Query()
single.key = 'Octane Crimson common'  # keyword
single.action = 'Single'
single.max_search = 3
single.params = {'filterItem': '1',  # item number
                 'filterPlatform': '1',
                 'filterSearchType': '0',
                 'filterCertification': 'N',
                 'filterPaint': '0',  # paint number
                 'filterItemType': '0'}

all_queries = [ optimize, single, splash, gravity, stellar, dueling ]
