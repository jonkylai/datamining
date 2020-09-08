from RLUtil import DESC_POSTLINK_IND, DESC_ITEMLINK_IND
from pandas import DataFrame


def create_page(df_in: DataFrame, type_in: str) -> None:
    """ Exports DataFrame to interactive web page for easiest consumption
        Web page is local and will be overwritten """
    if type_in == 'General':
        fid = open('RLTrading.html', 'w')
    elif type_in == 'Single':
        fid = open('RLTradingSingle.html', 'w')
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
        Length of list_in will be 2 + MAX_ITEMS*2 """
    content_table = list()

    # Begin tag
    content_table.append('<tr>')

    for i, val in enumerate(list_in):
        # First column has link of item
        if i == 0:
            content_table.append('  <td><a href="%s">%s</a></td>' % (list_in[3][DESC_ITEMLINK_IND], val))
        elif i == 1:
            content_table.append('  <td>%s</td>' % val)
        # Every column has a link in second element
        elif i % 2 == 0:
            # The zeroth item in description holds poster link
            content_table.append('  <td><a href="%s">%s</a></td>' % (list_in[i + 1][DESC_POSTLINK_IND], val))

    # End tag
    content_table.append('</tr>')

    # Output table with newlines
    return '\n'.join(content_table)

