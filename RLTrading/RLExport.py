from pandas import DataFrame


def create_page(df_in: DataFrame) -> None:
    """ Exports DataFrame to interactive web page for easiest consumption
        Web page is local and will be overwritten """
    fid = open('RLTrading.html', 'w')

    # Static web tags
    content_header = """<!DOCTYPE html>
<html>

<head>
<title>Data Mining Results</title>
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
        # First 2 columns have no link
        if i < 2:
            content_table.append('  <td>%s</td>' % val)
        # Every column has a link in second element
        elif i % 2 == 0:
            # The zeroth item in description holds poster link
            content_table.append('  <td><a href="%s">%s</a></td>' % (list_in[i + 1][0], val))

    # End tag
    content_table.append('</tr>')

    # Output table with newlines
    return '\n'.join(content_table)

