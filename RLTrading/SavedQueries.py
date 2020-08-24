from RLUtil import Query

optimize = Query()
optimize.name = 'Optimize All'
optimize.action = 'Optimize'
optimize.max_search = 15
optimize.params = {'filterItem': '2615',
                   'filterPlatform': '1',
                   'filterSearchType': '0',
                   'filterCertification': '0',
                   'filterPaint': '0',
                   'filterItemType': '0'}

splash = Query()
splash.name = 'Splash'
splash.action = 'Watch'
splash.key = 'Big Splash --limited'
splash.max_search = 3
splash.params = {'filterItem': '1975',
                 'filterPlatform': '1',
                 'filterSearchType': '0',
                 'filterCertification': 'N',
                 'filterPaint': 'N',
                 'filterItemType': '0'}

gravity = Query()
gravity.name = 'Gravity'
gravity.action = 'Watch'
gravity.key = 'Gravity Bomb --black-market'
gravity.max_search = 3
gravity.params = {'filterItem': '2948',
                  'filterPlatform': '1',
                  'filterSearchType': '0',
                  'filterCertification': 'N',
                  'filterPaint': 'N',
                  'filterItemType': '0'}

stellar = Query()
stellar.name = 'Interstellar'
stellar.action = 'Watch'
stellar.key = 'Interstellar (Black Market) --black-market'
stellar.max_search = 3
stellar.params = {'filterItem': '2944',
                  'filterPlatform': '1',
                  'filterSearchType': '0',
                  'filterCertification': 'N',
                  'filterPaint': 'N',
                  'filterItemType': '0'}

single = Query()
single.name = 'Random'
single.action = 'Single'
single.key = 'Dissolver (Black Market) --black-market'
single.max_search = 3
single.params = {'filterItem': '1175',
                 'filterPlatform': '1',
                 'filterSearchType': '0',
                 'filterCertification': 'N',
                 'filterPaint': '0',
                 'filterItemType': '0'}

all_queries = [ optimize, single, splash, gravity, stellar ]
