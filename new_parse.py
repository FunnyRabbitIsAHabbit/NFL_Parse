"""
NFL web page parsing

"""

import urllib.request
import re

LIST_LABELS = ['NAME', 'COMP', 'ATT', 'YDS', 'TD', 'INT', 'PR']


def parse_function():
    """Function returns list as
    [{'NAME': name, 'COMP': comp, 'ATT': att, 'YDS': yds,
    'TD': td, 'INT': INT, 'PR': pr}, ...]"""

    list_players = list()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}

    with open('input.txt') as inp_file:
        file_lines = inp_file.readlines()

    for url in file_lines:
        url_open = urllib.request.urlopen(url)
        url_read = url_open.read()
        url_text = str(url_read)
        string_name = url_text.find('player-name')
        name = url_text[url_text.find('>', string_name)+1:
                        url_text.find('&', string_name)]

        data = url_text[url_text.find('TOTAL'):
                        url_text.find('/tr',
                                      url_text.find('TOTAL'))]
        data = data.replace(',', '')

        params = re.findall(r'[-+]?\d*\.*\d+', data)
        comp = params[0]
        att = params[1]
        yds = params[3]
        td = params[5]
        INT = params[6]
        pr = params[9]

        list_values = [name, comp, att, yds, td, INT, pr]

        list_players.append(dict(zip(LIST_LABELS, list_values)))

    return list_players
