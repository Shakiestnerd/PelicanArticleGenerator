import os
import PySimpleGUI as sg
from datetime import date
import options
from output import Output


class UI:
    def __init__(self):
        super().__init__()
        self.options = options.UserOptions()
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
                    "Markdown", group_id="Type", default=True, size=label_size, key="md"
                ),
                sg.Radio("Restructured Text", group_id="Type", key="rst"),
            ]
        ]

        frame_layout2 = [
            [sg.Checkbox(" Recipe", auto_size_text=True, key="Is_Recipe"),]
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
                ),
                sg.FolderBrowse(
                    button_text="...",
                    initial_folder=self.options.base_folder,
                    key="Browse",
                ),
            ],
            [
                sg.Text("", size=label_size),
                sg.Frame("Format", frame_layout, title_color="blue"),
            ],
            [
                sg.Text("Title:", size=label_size),
                sg.Input(default_text="", key="Title", enable_events=True),
            ],
            [
                sg.Text("Slug:", size=label_size),
                sg.Input(default_text="Slug Value", disabled=True, key="Slug"),
            ],
            [
                sg.Text("Date:", size=label_size),
                sg.Input(
                    default_text=date.today().strftime("%Y-%m-%d"),
                    key="Date",
                    enable_events=True,
                ),
                sg.CalendarButton(
                    "...", key="Date_Pick", target="Date", format="%Y-%m-%d"
                ),
            ],
            [sg.Text("Author(s):", size=label_size), sg.Input(key="Author")],
            [
                sg.Text("Status:", size=label_size),
                sg.Combo(status_choices, default_value="draft", key="Status"),
            ],
            [
                sg.Text("Category:", size=label_size),
                sg.Listbox(
                    values=self.options.categories, key="Categories", size=(30, 6)
                ),
            ],
            [sg.Text("Tags:", size=label_size), sg.Input(key="Tags")],
            [
                sg.Text("", size=label_size),
                sg.Frame("Special Template", frame_layout2, title_color="blue"),
            ],
            [
                sg.Text("Summary:", size=label_size),
                sg.Multiline(size=(45, 3), key="Summary"),
            ],
            [sg.Button(button_text="Generate Article"),],
        ]

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
                    window["Categories"].update(categories)
            elif event in ("Title", "Date"):
                slug = values["Date"] + "-" + values["Title"].lower().replace(" ", "-")
                window["Slug"].update(slug)
            elif event == "About...":
                sg.popup(
                    "About Article Generator",
                    "Version 0.1",
                    "Author: Shakiestnerd",
                    "http://www.canofworms.com",
                    title="About",
                )
            elif event == "Documentation":
                print("Documentation")
            elif event == "Generate Article":
                self.create_article(values)

            print(event, values)

        window.close()

    def create_article(self, values):
        art = Output()

        try:
            art.filename = values["Slug"]

            if values["md"]:
                art.output_type = "md"
            else:
                art.output_type = "rst"

            art.title = values["Title"]
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
                art.base_folder, art.category, art.filename, art.output_type
            )
            message = ["Create article file:", art.full_file]
            if sg.PopupYesNo(message, title="Generate Article?"):
                art.save_article()

        except ValueError as err:
            sg.PopupError(err.args)

    def category_scan(self, folder):
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


if __name__ == "__main__":
    UI()
