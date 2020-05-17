import os
import platform
import subprocess
import string
import PySimpleGUI as sg
import webbrowser
from datetime import date
from article.options import UserOptions
from article.output import Output
from article.about import about
from article.tag import tag


class UI:
    def __init__(self):
        """ Load the user interface
        """
        super().__init__()
        self.options = UserOptions()
        self.filename = None
        sg.theme("Reddit")  # please make your windows colorful
        label_size = (15, 1)

        status_choices = [
            "published",
            "draft",
            "hidden",
        ]

        # ------ Menu Definition ------ #
        menu_def = [
            ["&File", ["E&xit"]],
            ["&Help", ["&Documentation", "&About..."],],
        ]

        frame_layout = [
            [
                sg.Radio(
                    "Markdown",
                    group_id="Type",
                    default=True,
                    size=label_size,
                    key="md",
                    tooltip="Save the file in markdown format",
                ),
                sg.Radio(
                    "Restructured Text",
                    group_id="Type",
                    key="rst",
                    tooltip="Save the file in restructured text format",
                ),
            ]
        ]

        frame_layout2 = [
            [
                sg.Checkbox(
                    " Recipe",
                    auto_size_text=True,
                    key="Is_Recipe",
                    tooltip="Include section for a food recipe",
                ),
            ]
        ]

        layout = [
            [sg.Menu(menu_def, tearoff=False)],
            [sg.Text("Create a new article", font=("Any", 12, "bold"))],
            [
                sg.Text("Content Folder:", size=label_size),
                sg.Input(
                    default_text=self.options.base_folder,
                    key="Folder",
                    enable_events=True,
                    disabled=True,
                    tooltip="Choose your Pelican/content folder (Required)",
                ),
                sg.FolderBrowse(
                    button_text="...",
                    initial_folder=self.options.base_folder,
                    key="Browse",
                ),
            ],
            [
                sg.Text("", size=label_size),
                sg.Frame(
                    "Format", frame_layout, title_color="blue", tooltip="Output format"
                ),
            ],
            [
                sg.Text("Title:", size=label_size),
                sg.Input(
                    default_text="",
                    key="Title",
                    enable_events=True,
                    tooltip="The article headline (Required)",
                ),
            ],
            [
                sg.Text("Slug:", size=label_size),
                sg.Input(
                    default_text="Slug Value",
                    disabled=True,
                    key="Slug",
                    tooltip="Slug is used as the filename",
                ),
            ],
            [
                sg.Text("Date:", size=label_size),
                sg.Input(
                    default_text=date.today().strftime("%Y-%m-%d"),
                    key="Date",
                    enable_events=True,
                    tooltip="The date for the article",
                ),
                sg.CalendarButton(
                    "...", key="Date_Pick", target="Date", format="%Y-%m-%d"
                ),
            ],
            [
                sg.Text("Author(s):", size=label_size),
                sg.Input(
                    default_text=self.options.author,
                    key="Author",
                    tooltip="Article author(s)",
                ),
            ],
            [
                sg.Text("Status:", size=label_size),
                sg.Combo(
                    status_choices,
                    default_value="draft",
                    key="Status",
                    tooltip="Initial status for the article",
                ),
            ],
            [
                sg.Text("Category:", size=label_size),
                sg.Listbox(
                    values=self.options.categories,
                    key="Categories",
                    size=(30, 6),
                    tooltip="Categories based on folder names (Required)",
                ),
            ],
            [
                sg.Text("Tags:", size=label_size),
                sg.Input(
                    key="Tags",
                    tooltip="Tags associated with this article",
                    default_text=",".join(self.options.last_tags),
                ),
                sg.Button("Show", key="Show"),
            ],
            [
                sg.Text("", size=label_size),
                sg.Frame("Special Template", frame_layout2, title_color="blue"),
            ],
            [
                sg.Text("Summary:", size=label_size),
                sg.Multiline(
                    size=(45, 3),
                    key="Summary",
                    tooltip="Summary is used for the 1st paragraph (Optional)",
                ),
            ],
            [
                sg.Button(button_text="Generate Article", key="generate"),
                sg.Button(button_text="Edit Article", key="edit", disabled=True),
            ],
        ]
        icon = b"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"
        # key function that reads the layout and displays the UI on screen.
        window = sg.Window("Article Generator", layout, font=("Ubuntu", 15), icon=icon)

        # Event dispatch handler
        while True:
            event, values = window.read()
            if event in (None, "Exit"):
                break
            elif event == "Folder":
                self.options.base_folder = values["Folder"]
                categories = self.category_scan(self.options.base_folder)
                if categories:
                    self.options.categories = categories
                    window["Categories"].update(categories)
            elif event in ("Title", "Date"):
                # strip out punctuation and replace spaces with dashes.
                dummy = (
                    "".join(
                        ch for ch in values["Title"] if ch not in string.punctuation
                    )
                    .lower()
                    .replace(" ", "-")
                )
                slug = values["Date"] + "-" + dummy
                window["Slug"].update(slug)
            elif event == "About...":
                about()
            elif event == "Documentation":
                browse = webbrowser.get()
                url = "https://pelican-article-generator.readthedocs.io/en/latest/index.html"
                browse.open_new_tab(url=url)
            elif event == "generate":
                self.filename = self.create_article(values)
                self.options.save_config()
                window["edit"].update(disabled=False)
            elif event == "edit":
                if self.filename:
                    self.open_article(self.filename)
            elif event == "Show":
                if self.options.base_folder:
                    categories = window["Categories"].get_list_values()
                    result, self.options.favorite_tags = tag(
                        self.options.favorite_tags, categories, self.options.base_folder
                    )
                    window["Tags"].update(", ".join(result))
                else:
                    sg.PopupOK(
                        "Please select content folder first.", title="No Content folder"
                    )

            print(event, values)

        window.close()

    def create_article(self, values):
        """Validate the field values while populating the output object.
        Then save the article file.  Should this method be part of the output
        object?
        """
        art = Output()

        try:
            art.filename = values["Slug"]

            if values["md"]:
                art.output_type = "md"
            else:
                art.output_type = "rst"
            if values["Title"]:
                art.title = values["Title"]
            else:
                raise ValueError("The title can not be blank.")
            art.slug = values["Slug"]
            art.date = values["Date"]
            art.author = values["Author"]
            if values["Categories"]:
                art.category = values["Categories"][0]
            else:
                raise ValueError("Select a category from the list.")
            art.tags = values["Tags"]
            art.status = values["Status"]
            art.summary = values["Summary"].strip()
            art.is_recipe = values["Is_Recipe"]
            art.base_folder = values["Folder"]
            art.full_file = os.path.join(
                art.base_folder, art.category, art.filename + "." + art.output_type
            )
            message = f"Create article file:\n{art.full_file}"
            if sg.PopupYesNo(message, title="Generate Article?"):
                art.save_article()
                self.update_config(values)
                return art.full_file
            else:
                return None
        except ValueError as err:
            sg.PopupError(err.args[0])
            return None

    def category_scan(self, folder):
        """Search the selected content folder for sub-folders that meet the 
        category criteria.
        """
        cat_list = []
        if len(folder) == 0:
            sg.popup(
                "Please select the pelican content folder.", title="Warning",
            )
            return
        elif "content" not in folder:
            sg.popup(
                "The selected folder does not appear",
                "to be a Pelican 'content' folder.",
                title="Warning",
            )
            return
        if os.path.isdir(folder):
            cats = os.listdir(folder)
            for item in cats:
                test = os.path.join(folder, item)
                if os.path.isdir(test):
                    if item not in ["images", "pages", "static"]:
                        cat_list.append(item)
        return cat_list

    def open_article(self, filepath):
        """ Open the newly minted article in the default editor for your OS
        """
        if platform.system() == "Darwin":  # macOS
            subprocess.call(("open", filepath))
        elif platform.system() == "Windows":  # Windows
            os.startfile(filepath)
        else:  # linux variants
            subprocess.call(("xdg-open", filepath))

    def update_config(self, values):
        # self.options.base_folder = ""  # should be filled in already
        self.options.author = values["Author"]
        # self.options.categories = []
        self.options.last_tags = values["Tags"]
        if self.options.favorite_tags == "":
            self.options.favorite_tags = self.options.last_tags
        if values["md"]:
            self.options.default_type = "md"
        else:
            self.options.default_type = "rst"
        self.options.save_config()


if __name__ == "__main__":
    UI()
