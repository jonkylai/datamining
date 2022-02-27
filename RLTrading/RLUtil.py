from pandas import DataFrame
from os import path

import re
import time


""" All constants are stored in utility """
# Number of posts to store per repeated item
MAX_ITEMS = 5
# Age to remove old posts
HOUR_THRESHOLD = 72
# Maximum value of item
MAX_VALUE = 99999

# Time format
TIME_FORMAT = "%Y%m%d%H%M%S"
# Time between monitor loads in seconds
SLEEP_TIME = 60

# Name of blacklist file
BLACKLIST_FILE = path.abspath(path.join(path.dirname(__file__), '..', 'SBotDetection', 'blacklist.txt'))
# RL Trading url
BASE_URL = 'https://rocket-league.com'
# Watch list directory name
WATCH_DIR = 'watchlist'
# Name of save file
PICKLE_FILE = 'RLTrading.p'


class Query:
    """ Search parameters to get poster listings """
    def __init__(self):
        self.key = None
        self.action = None
        self.monitor_mode = False
        self.url = None


def print_time(string_in: str, time_in: float, benchmark_in: float) -> float:
    """ Benchmark run time of specified chunks of code
        Usage requires time.time() before and print_time() after
        Also removes this time from total program benchmark time """
    elapsed_time = time.time() - time_in
    print('--- %0.4f sec --- %s' % (elapsed_time, string_in))

    return benchmark_in + elapsed_time


def get_df_index(key_in: str, df_in: DataFrame) -> int:
    """ Returns index of a key with error checking """
    index_list = df_in.index[df_in['Item Name'] == key_in].tolist()
    if len(index_list) != 1:
        print('ERROR: Cannot find %s in dataframe' % key_in)
        exit()
    else:
        return index_list[0]


def int_cast(user_in: str) -> int:
    """ Int cast with failure checking """
    try:
        return int( user_in.strip() )
    except ValueError:
        print('ERROR: Cannot cast int on %s' % user_in)
        exit()
    finally:
        pass


def string_clean(text_in: str) -> str:
    """ Clean strings to remove weird characters and extra spaces """
    text_out = re.sub('[^ A-Za-z0-9:/-]', '', text_in)
    # Remove duplicate spaces
    text_out = ' '.join(text_out.split())
    return text_out


""" The rest of this file contains words for processing """
# Item types to exclude from list
#   Excludes "Offer" types
EXCLUDE_LIST = [
    'Uncommon Offer Uncommon',
    'Rare Offer Rare',
    'Very Rare Offer Very-Rare',
    'Import Offer Import',
    'Exotic Offer Exotic',
    'Overpay Uncommon',
    'Placeholder Uncommon'
]

COLOR_LIST = [
    'Black',
    'Burnt Sienna',
    'Cobalt',
    'Crimson',
    'Forest Green',
    'Grey',
    'Lime',
    'Orange',
    'Pink',
    'Purple',
    'Saffron',
    'Sky Blue',
    'Titanium White'
]

# Lists for each type of NC
NCC_LIST = [
    'Cromulon',
    'Devil Horns',
    'Fez',
    'Fire Helmet',
    'Halo',
    'Hard Hat',
    'Mariachi Hat',
    'Pirates Hat',
    'Royal Crown',
    'Top Hat',
    'Witchs Hat',
    'Wizard Hat'
]

NCU_LIST = [
    'Alien',
    'Balloon Dog',
    'Candle',
    'Chick Magnet',
    'Cuckoo Clock',
    'Cupcake',
    'Disco Ball',
    'Doughnut',
    'Flower - Daisy',
    'Flower - Orchid',
    'Flower - Tulip',
    'Flower - Rose',
    'Foam Finger',
    'Genie Lamp',
    'Giant Panda',
    'Harpoon',
    'Hot Dog',
    'Hula Girl',
    'Lollipop',
    'Macaron',
    'Parrot',
    'Piata',
    'Pinwheel',
    'Rainbow Flag',
    'Rocket',
    'Rubber Duckie',
    'Satellite',
    'Seastar',
    'Sunflower',
    'Trident',
    'Venus Flytrap',
    'Waffle',
    'Antlers',
    'Baseball Cap B',
    'Baseball Cap F',
    'Beret',
    'Biker Cap',
    'Birthday Cake',
    'Bowler',
    'Brodie Helmet',
    'Bycocket',
    'Captains Hat',
    'Cattleman',
    'Chainsaw',
    'Chefs Hat',
    'Cockroach',
    'Deerstalker',
    'Derby',
    'Foam Hat',
    'Fruit Hat',
    'Graduation Cap',
    'Hawaiian Lei',
    'Heart Glasses',
    'Homburg',
    'Hotcakes',
    'Ivy Cap',
    'Jack-In-The-Box',
    'Latte',
    'Light Bulb',
    'Little Bow',
    'Little Bunny',
    'Little Cow',
    'Little Dog',
    'Little Elephant',
    'Little Owl',
    'Little Sloth',
    'Mouse Trap',
    'Paper Boat',
    'Party Hat',
    'Pigeon',
    'Plunger',
    'Police Hat',
    'Pork Pie',
    'Rasta',
    'Rhino Horns',
    'Shuriken',
    'Stegosaur',
    'Surfboard',
    'Tiara',
    'Traffic Cone',
    'Trucker Hat',
    'Uncle Sam',
    'Unicorn',
    'Visor',
    'Work Boot'
]

NCR_LIST = [
    'Catfish',
    'Chafed Cherry',
    'Clamshell',
    'Dragon Wings',
    'Drink Helmet',
    'Fishbowl',
    'MMS Headphones',
    'Mr Banana',
    'Mr Hot Dog',
    'Mr Hot Pepper',
    'Mrs Avocado',
    'Octopus',
    'ROBO-Visor',
    'Rooster Comb',
    'Sad Strawberry',
    'Wildcat Ears',
    'Worried Watermelon',
    'Ball King',
    'Call Sign RL',
    'Dead Serious',
    'Dendritic',
    'Hearts',
    'Maximon',
    'MDGA',
    'Narwhal',
    'Rockat',
    'Salty',
    'Shattered',
    'Soccer Ball',
    'Sticker Bomb',
    'Tagged',
    'Turtle',
    'Flex Venom',
    'Flower Power Merc',
    'Glyphtrix Triton',
    'Junk Food Breakout',
    'Min-Spec Masamune',
    'Racer Octane',
    'Royalty Dominus',
    'Shaperacer Paladin',
    'Tiger Tiger Aftershock',
    'Asterias',
    'Gearlock',
    'Zeta',
    'Mothership',
    'Sanchez DC-137',
    'Vulcan'
]

NCVR_LIST = [
    'Butterfly',
    'Goldfish',
    'Beaten Egg',
    'Calculated',
    'Junk Food',
    'Moai',
    'Nice Slice',
    'Pigeon',
    'Starbase ARC',
    'Unicorn',
    'Burlap',
    'Cookie Dough',
    'Knitted Yarn',
    'Metallic Smooth',
    'Metallic Pearl Smooth',
    'Moon Rock',
    'Feather',
    'Frostbite',
    'Hearts',
    'Ink',
    'Lightning',
    'Lightning Yellow',
    'Magmus',
    'Taco',
    'Toon Smoke',
    'Treasure'
]

NCI_LIST = [
    'Datastream',
    'Flamethrower',
    'Ion',
    'Plasma',
    'Sacred',
    'Sparkles',
    'Standard',
    'Thermal',
    'Breakout',
    'Merc',
    'Octane',
    'Road Hog',
    'Venom',
    'X-Devil'
]

NCE_LIST = [
    'Alchemist',
    'Almas',
    'Dieci',
    'Falco',
    'Invader',
    'Lowrider',
    'Neptune',
    'Octavian',
    'OEM',
    'Rat Rod',
    'Spyder',
    'Stern',
    'Sunburst',
    'Trahere',
    'Tunica',
    'Veloce',
    'Vortex'
]

IGNORE_LIST = [
    'Overpay Uncommon',
    'Discotheque Exotic',
    'Infinium Exotic',
    'Fgsp Exotic',
    'Kalos Exotic',
    'Lobo Exotic',
    'Equalizer Exotic',
    'Turbine Exotic',
    'Pyrrhos Exotic',
    'Roulette Exotic',
    'Clockwork Exotic',
    'Raijin Exotic',
    'Draco Exotic',
    'Ara-51 Exotic',
    'Zowie Exotic',
    'Balla-Carr Exotic',
    'Hikari P5 Exotic',
    'Dynamo Exotic',
    'Gernot Exotic',
    'Zowie Exotic',
    'Zomba Exotic',
    'Looper Exotic',
    'Centro Exotic',
    'Reevrb Exotic',
    'Santa Fe Exotic',
    'Pulsus Exotic',
    'Hypnotik Exotic',
    'Reactor Exotic',
    'Photon Exotic',
    'K2 Exotic',
    'Chrono Exotic',
    'Zefram Exotic',
    'Fgsp Exotic'
]