"""
Visual demo for NFL parsing
Developer: Stanislav Alexandrovich Ermokhin

"""

import asyncio
import aiohttp
from re import findall
from tkinter import *
from operator import itemgetter

import OOP

LIST_LABELS_start = ['NAME', 'COMP', 'ATT', 'YDS', 'TD', 'INT', 'PR']
main_list = list()


async def mutate_func(html):
    """
    Function to search for certain characteristics for players

    :param html: html type text
    :return: dict
    """

    url_text = html
    string_name = url_text.find('player-name')
    name = url_text[url_text.find('>', string_name) + 1:
                    url_text.find('&', string_name)]

    data = url_text[url_text.find('TOTAL'):
                    url_text.find('/tr',
                                  url_text.find('TOTAL'))]
    data = data.replace(',', '')

    params = findall(r'[-+]?\d*\.*\d+', data)
    comp = params[0]
    att = params[1]
    yds = params[3]
    td = params[5]
    INT = params[6]
    pr = params[9]

    list_values = [name, comp, att, yds, td, INT, pr]

    return dict(zip(LIST_LABELS_start, list_values))


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def wow(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)

        return await mutate_func(html)


async def main_async(filename):

    global main_list

    with open(filename) as inp_file:
        file_lines = inp_file.readlines()
        for i in range(len(file_lines)):
            file_lines[i] = file_lines[i].rstrip('\n')

    for url in file_lines:
        main_list.append(await wow(url))


asyncio.run(main_async('input.txt'))

LIST_PLAYERS = sorted(main_list,
                      key=itemgetter('PR', 'NAME'),
                      reverse=True)
LIST_LABELS = [''] + LIST_LABELS_start

main_window = Tk()
main_window.title('NFL Ratings')

main_frame = OOP.VerticalScrolledFrame(main_window,
                                       width=430,
                                       height=730)
main_frame.grid(row=0,
                column=0)

for i in range(len(LIST_LABELS)):
    Label(main_frame, text=LIST_LABELS[i]).grid(row=0,
                                                column=i)
    for j in range(len(LIST_PLAYERS)):
        for key in LIST_PLAYERS[j]:
            if key == LIST_LABELS[i]:
                Label(main_frame, pady=7,
                      text=LIST_PLAYERS[j][key]).grid(row=j+1,
                                                      column=i)

for i in range(len(LIST_PLAYERS)):
    Label(main_frame, text=i+1).grid(row=i+1,
                                     column=0)

main_window.mainloop()
