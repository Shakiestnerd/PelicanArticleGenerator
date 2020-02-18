"""
article.py

Create a new article.
"""

import sys
import os
from datetime import datetime, date
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import BOTH, W, E, N, WORD, filedialog, messagebox, StringVar, END
import tkinter.font as tkFont
import options
from output import Output
import about

__author__ = "Keith Sanders"
__version__ = "0.1.0"
__license__ = "MIT"
__email__ = "keith.sanders@fluor.com"

TEMPLATE = """
---
title: {title}
date: {year}-{month}-{day}
tags:
category:
slug: {slug}
summary:
status: draft
author: ShakiestNerd
---

"""


class UI:
    """Markdown article generator application user interface using tkinter"""

    def __init__(self, parent):
        self.parent = parent
        nb = ttk.Notebook(parent, padding=8)
        nb.grid(row=0, column=0, columnspan=4)
        nb.pack(fill=BOTH, expand=True)
        self.options = options.UserOptions()
        # self.db = None

        #####################
        # Define the menu bar
        #####################
        self.menubar = tk.Menu(parent)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Exit", command=exit_callback)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Documentation", command=self.show_docs)
        self.helpmenu.add_command(label="About", command=self.show_about)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        parent.config(menu=self.menubar)
        #######################################################
        # adding Frames as pages for the ttk.Notebook
        # first page, which would get widgets gridded into it
        #######################################################
        page1 = ttk.Frame(nb)
        # page1.columnconfigure(0, weight=1)
        # page1.columnconfigure(3, pad=5)
        # page1.columnconfigure(4, pad=5)
        # page1.rowconfigure(0, pad=10)
        page1.pack(fill=BOTH, expand=True)

        # row 0
        row = 0
        p1_label_title = ttk.Label(page1, text="Create new article:")
        p1_label_title.grid(column=1, row=row, padx=5, pady=5, sticky=W)

        p1_create = ttk.Button(page1, text="Create", command=self.create_article)
        p1_create.grid(row=row, column=4, padx=5, pady=5, sticky=E)

        # row 1

        row += 1
        self.md_or_rst = tk.StringVar()
        self.md_or_rst.set("md")
        p1_md_label = ttk.Label(page1, text="File Type:")
        p1_md_label.grid(column=0, row=row, padx=5, pady=5, sticky=W)
        p1_md_or_rst1 = ttk.Radiobutton(
            page1, text="Markdown", value="md", variable=self.md_or_rst
        )
        p1_md_or_rst1.grid(row=row, column=1, padx=5, pady=5, sticky=W)
        row += 1
        p1_md_or_rst2 = ttk.Radiobutton(
            page1, text="Restructured Text", value="rst", variable=self.md_or_rst
        )
        p1_md_or_rst2.grid(row=row, column=1, padx=5, pady=5, sticky=W)

        row += 1
        p1_title_label = ttk.Label(page1, text="Title:")
        p1_title_label.grid(row=row, column=0, padx=5, pady=5, sticky=E)
        self.p1_title_value = StringVar()
        self.p1_title = ttk.Entry(page1, textvariable=self.p1_title_value)
        self.p1_title.grid(
            row=row, column=1, columnspan=2, padx=5, pady=5, sticky=W + E
        )
        self.p1_title.bind("<KeyRelease>", self.set_slug)

        # row 3
        row += 1
        p1_slug_label = ttk.Label(page1, text="Slug:")
        p1_slug_label.grid(row=row, column=0, padx=5, pady=5, sticky=E)
        self.p1_slug_value = StringVar()
        self.p1_slug_value.set("Slug value")
        self.p1_slug = ttk.Label(page1, textvariable=self.p1_slug_value)
        self.p1_slug.grid(row=row, column=1, columnspan=2, padx=5, pady=5, sticky=W + E)

        # row 4
        row += 1
        p1_date_label = ttk.Label(page1, text="Date:")
        p1_date_label.grid(row=row, column=0, padx=5, pady=5, sticky=E)
        self.p1_date_value = StringVar()
        self.p1_date_value.set(date.today().strftime("%Y-%m-%d"))
        self.p1_date = ttk.Entry(page1, textvariable=self.p1_date_value)
        self.p1_date.grid(row=row, column=1, columnspan=2, padx=5, pady=5, sticky=W + E)

        # row 5
        row += 1
        p1_author_label = ttk.Label(page1, text="Author:")
        p1_author_label.grid(row=row, column=0, padx=5, pady=5, sticky=E)
        self.p1_author_value = StringVar()
        self.p1_author_value.set("shakiestnerd")
        self.p1_author = ttk.Entry(page1, textvariable=self.p1_author_value)
        self.p1_author.grid(
            row=row, column=1, columnspan=2, padx=5, pady=5, sticky=W + E
        )

        # row 6
        row += 1
        p1_status_label = ttk.Label(page1, text="Status:")
        p1_status_label.grid(row=row, column=0, padx=5, pady=5, sticky=E)
        p1_status_value = StringVar(page1)
        choices = [
            "published",
            "draft",
            "hidden",
        ]
        # p1_status_value.set(choices[0])
        self.p1_status_menu = ttk.Combobox(page1, values=choices, state="readonly")
        self.p1_status_menu.current(0)
        self.p1_status_menu.grid(row=row, column=1, padx=5, pady=5, sticky=W)

        # row 7
        row += 1
        p1_cat_label = ttk.Label(page1, text="Category:")
        p1_cat_label.grid(row=row, column=0, padx=5, pady=5, sticky=E)
        choices2 = ["Technology", "Reading", "Faith", "Family"]
        self.p1_cat_menu = ttk.Combobox(page1, values=choices2)
        self.p1_cat_menu.current(0)
        self.p1_cat_menu.grid(row=row, column=1, padx=5, pady=5, sticky=W)

        row += 1
        p1_tags_label = ttk.Label(page1, text="Tags:")
        p1_tags_label.grid(row=row, column=0, padx=5, pady=5, sticky=E)
        self.p1_tags_value = StringVar(page1)
        p1_tags = ttk.Entry(page1, textvariable=self.p1_tags_value)
        p1_tags.grid(row=row, column=1, columnspan=2, padx=5, pady=5, sticky=W + E)

        row += 1
        self.p1_recipe_value = tk.IntVar()
        self.p1_recipe_value.set(0)
        p1_recipe = ttk.Checkbutton(
            page1,
            text="Recipe Article?",
            variable=self.p1_recipe_value,
            onvalue=1,
            offvalue=0,
        )
        p1_recipe.grid(row=row, column=1, padx=5, pady=5, sticky=W)

        row += 1
        p1_summary_label = ttk.Label(page1, text="Summary:")
        p1_summary_label.grid(row=row, column=0, padx=5, pady=5, sticky=E)
        self.p1_summary = ScrolledText(page1, height=5)
        self.p1_summary.grid(row=row, column=1, columnspan=2, padx=5, pady=5)

        nb.add(page1, text="Article")

        # ==========================
        page2 = ttk.Frame(nb)
        page2.pack(fill=BOTH, expand=True)

        # row 0
        row = 0
        p2_label_title = ttk.Label(page2, text="Basic Configuration Information:")
        p2_label_title.grid(column=1, row=row, padx=5, pady=5, sticky=W)

        p2_create = ttk.Button(page2, text="Save Config", command=self.save_config)
        p2_create.grid(row=row, column=3, padx=5, pady=5, sticky=E)

        # row 1
        row += 1
        p2_folder_label = ttk.Label(page2, text="Content Folder:")
        p2_folder_label.grid(row=row, column=0, padx=5, pady=5, sticky=E)
        self.p2_folder_value = StringVar()
        self.p2_folder_value.set(self.options.base_folder)
        self.p2_folder = ttk.Entry(page2, textvariable=self.p2_folder_value)
        self.p2_folder.grid(
            row=row, column=1, columnspan=2, padx=5, pady=5, sticky=W + E
        )
        p2_picker = ttk.Button(
            page2, text="...", command=lambda: self.folder_select(self.p2_folder_value)
        )
        p2_picker.grid(row=row, column=3, padx=5, pady=5, sticky=E)

        # row 2
        row += 1
        p2_categories_label = ttk.Label(page2, text="Categories:")
        p2_categories_label.grid(row=row, column=0, padx=5, pady=5, sticky=E + N)
        p2_categories_value = StringVar()
        self.p2_categories = ScrolledText(page2, height=5)
        self.p2_categories.grid(row=row, column=1, columnspan=2, padx=5, pady=5)
        p2_cat_scan = ttk.Button(page2, text="Scan", command=self.cat_scan)
        p2_cat_scan.grid(row=row, column=3, padx=5, pady=5, sticky=E + N)

        # row 3
        row += 1
        p2_default_author_label = ttk.Label(page2, text="Default Author:")
        p2_default_author_label.grid(row=row, column=0, padx=5, pady=5, sticky=E)
        self.p2_default_author_value = StringVar()
        self.p2_default_author_value.set(self.options.author)
        self.p2_default_author = ttk.Entry(
            page2, textvariable=self.p2_default_author_value
        )
        self.p2_default_author.grid(
            row=row, column=1, columnspan=2, padx=5, pady=5, sticky=W + E
        )

        nb.add(page2, text="Configuration")

    def set_slug(self, event):
        self.p1_slug_value.set(
            "-".join(
                [
                    self.p1_date_value.get(),
                    self.p1_title_value.get().lower().replace(" ", "-"),
                ]
            )
        )

    def create_article(self):
        filename = self.p1_slug_value.get()
        folder = self.p1_cat_menu.get()
        ext = self.md_or_rst.get()
        message = f"Create article file:\n{folder}/{filename}.{ext}?"
        if messagebox.askyesno("Proceed?", message):
            art = Output()
            art.output_type = self.md_or_rst.get()
            art.title = self.p1_title_value.get()
            art.slug = self.p1_slug_value.get()
            art.date = self.p1_date_value.get()
            art.author = self.p1_author_value.get()
            art.category = self.p1_cat_menu.get()
            art.tags = self.p1_tags_value.get()
            art.status = self.p1_status_menu.get()
            art.summary = self.p1_summary.get(1.0, END)
            art.is_recipe = self.p1_recipe_value.get()
            art.save_article()

    def make_entry(title, category):
        """Create a new entry
        """
        today = datetime.today()
        slug = title.lower().strip().replace(" ", "-")
        f_create = "content/{}/{}_{:0>2}_{:0>2}_{}.md".format(
            category, today.year, today.month, today.day, slug
        )
        t_body = TEMPLATE.strip().format(
            title=title, year=today.year, month=today.month, day=today.day, slug=slug,
        )
        with open(f_create, "w") as write_out:
            write_out.write(t_body)
        print("File created -> " + f_create)

    def save_config(self):
        self.options.author = self.p2_default_author_value.get()
        self.options.categories = self.p2_categories.get("1.0", END).split("\n")
        self.options.base_folder = self.p2_folder_value.get()
        self.options.save_config()

    def folder_select(self, tk_var):
        """ folder select button callback"""
        root.config(cursor="watch")
        fn = self.load_folder_name("Select 'Pelican' content folder")
        # user_options.tos_report = fn
        tk_var.set(fn)

        root.config(cursor="")

    def cat_scan(self):
        folder = self.p2_folder_value.get()
        cat_list = []
        if len(folder) == 0:
            msg = "Please enter the pelican content\nfolder in the 'Content Folder' field above."
            messagebox.showinfo("No folder selected", message=msg)
        if os.path.isdir(folder):
            cats = os.listdir(folder)
            for item in cats:
                test = os.path.join(folder, item)
                if os.path.isdir(test):
                    if item not in ["images", "pages", "static"]:
                        cat_list.append(item)
        self.p2_categories.insert("1.0", "\n".join(cat_list))

    @staticmethod
    def load_folder_name(title):
        folder = filedialog.askdirectory(title=title)
        if folder is None:
            return "Click button to select folder --->"
        else:
            return folder

    def show_docs(self):
        """
        Launch the default web browser and display the documentation.
        """
        # Menu bar methods
        browse = webbrowser.get()
        url = "http://www.canofworms.com/docs/article/"
        browse.open_new_tab(url=url)

    def show_about(self) -> None:
        """ Display the about box """
        about.AboutDialog(self.parent)


def exit_callback():
    """
    Exit the application
    """
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        # user_options.save_config()
        root.destroy()


def set_icon(icon_name):
    window_system = root.tk.call("tk", "windowingsystem")
    if window_system == "win32":  # Windows
        icon_name += ".ico"
    elif window_system == "x11":  # Unix
        icon_name = "@" + icon_name + ".xbm"
    try:
        root.iconbitmap(icon_name)
    except:
        return


def main():
    """ The main controlling function """
    root.title("Article Generator")
    #  root.after(1000, update_handler)
    root.protocol("WM_DELETE_WINDOW", exit_callback)
    root.geometry("850x500+300+100")
    if sys.platform == "linux":
        # clam, alt, default, classic
        s = ttk.Style()
        s.theme_use("clam")

    set_icon("favicon")
    UI(root)
    root.mainloop()


if __name__ == "__main__":
    # user_options = options.UserOptions()
    root = tk.Tk()
    main()
