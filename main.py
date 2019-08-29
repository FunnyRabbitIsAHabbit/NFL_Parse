"""
Visual demo for NFL parsing
Developer: Ermokhin Stanislav Alexandrovich

"""


import new_parse as parse
from tkinter import *
import OOP

LIST_PLAYERS = sorted(parse.parse_function(),
                      key=lambda dic: dic['PR'],
                      reverse=True)
LIST_LABELS = [''] + parse.LIST_LABELS

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
