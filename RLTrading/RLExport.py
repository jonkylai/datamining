from RLUtil import TIME_FORMAT

from pandas import DataFrame
from datetime import datetime, timedelta


def get_color(item_in) -> str:
    """ Determines the background color of item based on various criteria
        If item is null, black
        If item is new, yellow
        If item is old, grey
        Shades of yellow and grey are determined by age of post """
    if item_in.post_time == 'NULL':
        return '000000'

    # Colors for new items
    elif item_in.is_new == True:
        post_time = datetime.strptime(item_in.post_time, TIME_FORMAT)
        time_ago = datetime.now() - post_time
        if time_ago < timedelta(minutes=10):
            return 'FFFF00'
        elif time_ago < timedelta(minutes=30):
            return 'CCCC00'
        elif time_ago < timedelta(hours=1):
            return '999900'
        elif time_ago < timedelta(hours=2):
            return '666600'
        else:
            return '333300'

    # Colors for old items
    else:
        post_time = datetime.strptime(item_in.post_time, TIME_FORMAT)
        time_ago = datetime.now() - post_time
        if time_ago < timedelta(minutes=30):
            return '606060'
        elif time_ago < timedelta(hours=1):
            return '404040'
        elif time_ago < timedelta(hours=2):
            return '202020'
        else:
            return '000000'


def create_page(df_in: DataFrame, type_in: str) -> None:
    """ Exports DataFrame to interactive web page for easiest consumption
        Web page is local and will be overwritten """
    if type_in == 'General':
        fid = open('RLTrading.html', 'w')
    else:
        print('ERROR: Wrong input %s to create_page()' % type_in)
        exit()

    # Static web tags
    content_header = """<!DOCTYPE html>
<html>

<head>
<style>
body {
    background-color: black;
    color: white;
}
a:link {
    color: grey;
}
a:visited {
    color: green;
}
</style>
</head>
<body>
"""
    content_footer = """
</body>

</html>
"""

    # Initialize table creation
    content_table = list()
    content_table.append('<table border="1">')
    # Set table header as DataFrame columns
    header_row = df_in.columns
    content_table.append(create_page_row(header_row))
    # Write each row to table
    for row in df_in.values.tolist():
        content_table.append(create_page_row(row))
    content_table.append('</table>')

    # Write to file in proper order
    fid.write(content_header)
    fid.write('\n'.join(content_table))
    fid.write(content_footer)


def create_page_row(list_in: list) -> str:
    """ Generates html for single row of table
        Length of list_in will be 4 + MAX_ITEMS*4 """
    content_table = list()

    # Do not write if the gains are unreasonable
    try:
        if int(list_in[2]) < -1000:
            return ''
    except:
        pass

    # Begin tag
    content_table.append('<tr>')

    past_threshold = False
    for i in range(len(list_in)):
        # First column has link of item
        if i == 0:
            content_table.append('  <td><a href="%s">%s</a></td>' % (list_in[1], list_in[0]))
        elif i == 1:
            continue
        elif i == 2 or i == 3:
            content_table.append('  <td>%s</td>' % list_in[i])
        # Afterwards every third column has a link
        elif i % 4 == 0:
            # Background color is three columns later
            content_table.append( '  <td><a href="%s" style="background-color:#%s">%s</a></td>' %
                                  (list_in[i + 1], list_in[i + 3], list_in[i]) )

        if past_threshold:
            break

    # End tag
    content_table.append('</tr>')

    # Output table with newlines
    return '\n'.join(content_table)

