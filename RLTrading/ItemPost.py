import re

class ItemPost:
    def __init__(self ):
        self.item = []

    def __init__(self, data_in):
        # Process data
        data_out = []
        for item in data_in.get_text().splitlines():
            if item != '':
                # If item is a number (excluding whitespace), update count value
                if item.strip().isdecimal():
                    data_out[-1][1] = item
                # Add item to list with a default of one count
                else:
                    data_out.append( [ item, 1 ] )
        print(data_out)