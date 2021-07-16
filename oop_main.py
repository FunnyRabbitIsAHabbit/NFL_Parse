"""
Visual demo for NFL parsing
Developer: Stanislav Alexandrovich Ermokhin
Version: 1.1

"""

import asyncio
from operator import itemgetter
from tkinter import *

import aiohttp

import OOP


class App(Tk):

    def __init__(self):
        super().__init__()

        self.main_list = list()
        self.LIST_LABELS_START = ['NAME', 'COMP', 'ATT', 'YDS', 'TD', 'INT', 'PR']
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
        self.LIST_LABELS = [''] + self.LIST_LABELS_START
        self.list_players = list()
        self.title('NFL Ratings')
        self.main_frame = OOP.VerticalScrolledFrame(self,
                                                    width=430,
                                                    height=730)
        self.main_frame.grid(row=0,
                             column=0)

        self.run()

    def run(self):
        asyncio.run(self.main_async('input.txt'))

        for i in range(len(self.LIST_LABELS)):
            Label(self.main_frame, text=self.LIST_LABELS[i]).grid(row=0,
                                                                  column=i)

            for j in range(len(self.list_players)):
                for key in self.list_players[j]:
                    if key == self.LIST_LABELS[i]:
                        Label(self.main_frame, pady=7,
                              text=self.list_players[j][key]).grid(row=j + 1,
                                                              column=i)

        for i in range(len(self.list_players)):
            Label(self.main_frame, text=i + 1).grid(row=i + 1,
                                                    column=0)

    async def mutate_func(self, html):
        """
        Function to search for certain characteristics for players

        :param html: html type text
        :return: dict
        """

        attr_name = "<th aria-label"
        p = "passing"
        comp_name = "Completions"
        att_name = "Attempts"
        yds_name = "Yards"
        td_name = "Touchdowns"
        int_name = "Interceptions"
        pr_name = "PasserRating"

        to_find_str = 'class="nfl-c-player-header__title"'
        name = html[html.find(to_find_str) + len(to_find_str) + 1:html.find('</h1>', html.find(to_find_str))]
        to_find_str = f'{attr_name}="{p + comp_name}"'
        relatively_large_number = 100
        expr1 = "html.find(to_find_str)"
        expr2 = "html.find(to_find_str)+len(to_find_str)+relatively_large_number"

        list_values = list()
        lst = [p + comp_name, p + att_name, p + yds_name, p + td_name, p + int_name, p + pr_name]
        r_exp = r'[-+]?\d*\.*\d+'

        for item in lst:
            to_find_str = f'{attr_name}="{item}"'

            get_number = re.findall(r_exp, html[eval(expr1):eval(expr2)])[0]
            list_values.append(get_number)

        new_lst = [name, *list_values]
        return dict(zip(self.LIST_LABELS_START, new_lst))

    @staticmethod
    async def fetch(session, url):
        async with session.get(url=url) as response:
            return await response.text()

    async def create_new_session(self, url):
        async with aiohttp.ClientSession(headers=self.HEADERS) as session:
            html = await self.fetch(session, url)

            return await self.mutate_func(html)

    async def main_async(self, filename):

        with open(filename) as inp_file:
            file_lines = inp_file.readlines()
            for i in range(len(file_lines)):
                file_lines[i] = file_lines[i].rstrip('\n')

        for url in file_lines:
            try:
                self.main_list.append(await self.create_new_session(url))
                self.list_players = sorted(self.main_list,
                                           key=itemgetter('PR', 'NAME'),
                                           reverse=True)
            except IndexError:
                pass


app = App()
app.mainloop()
