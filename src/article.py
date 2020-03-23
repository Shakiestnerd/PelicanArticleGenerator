import os
import platform
import subprocess
import string
import PySimpleGUI as sg
from datetime import date
from .options import UserOptions
from .output import Output
from .about import about
from .tag import tag


class UI:
    def __init__(self):
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
            [sg.Text("Create a new src", font=("Any", 12, "bold"))],
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
                    tooltip="The src headline (Required)",
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
                    tooltip="The date for the src",
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
                    tooltip="Initial status for the src",
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
                sg.Input(key="Tags", tooltip="Tags associated with this src"),
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

        # key function that reads the layout and displays the UI on screen.
        window = sg.Window("Article Generator", layout)

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
                print("Documentation")
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
        Then save the src file.  Should this method be part of the output
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
            message = f"Create src file:\n{art.full_file}"
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
        """ Open the newly minted src in the default editor for your OS
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
