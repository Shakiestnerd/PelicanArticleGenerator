import tkinter as tk
from tkinter import ttk
import tkSimpleDialog
import article
# import tkinter.font as tkFont


class AboutDialog(tkSimpleDialog.Dialog):

    def body(self, master):

        msg = 'Article Generator'
        label = ttk.Label(master, text=msg, font='big')
        label.pack(padx=4, pady=4)
        msg = 'Create a new blank article in markdown\nor restructured text format.\n'
        label2 = ttk.Label(master, text=msg)
        label2.pack(padx=4, pady=4)
        msg = f'Author: {article.__author__}'
        label3 = ttk.Label(master, text=msg)
        label3.pack(padx=4, pady=4)
        return None

