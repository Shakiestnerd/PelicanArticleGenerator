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
                sg.Input(default_text=self.options.base_folder, key="Folder"),
                sg.Button(button_text="..."),
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
            ],
            [sg.Text("Author(s):", size=label_size), sg.Input(key="Author")],
            [
                sg.Text("Status:", size=label_size),
                sg.Combo(status_choices, default_value="draft", key="Status"),
            ],
            [
                sg.Text("Category:", size=label_size),
                sg.Listbox(
                    values=["Listbox 1", "Listbox 2", "Listbox 3"], size=(30, 6)
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
            elif event == "...":
                window["Folder"].update(self.load_folder_name())
            elif event in ("Title", "Date"):
                slug = values["Date"] + "-" + values["Title"].lower().replace(" ", "-")
                window["Slug"].update(slug)
            elif event == "About...":
                print("About box")
            elif event == "Documentation":
                print("Documentation")
            elif event == "Generate Article":
                self.create_article()

            print(event, values)

        window.close()

    def create_article(self, values):
        filename = values["Slug"]
        folder = self.options.base_folder
        if values["md"]:
            ext = "md"
        else:
            ext = "rst"
        message = f"Create article file:\n{folder}/{filename}.{ext}?"
        if sg.PopupYesNo(message):
            art = Output()
            art.output_type = ext
            art.title = values["Title"]
            art.slug = values["Slug"]
            art.date = values["Date"]
            art.author = values["Author"]
            art.category = values["Category"]
            art.tags = values["Tags"]
            art.status = values["Status"]
            art.summary = values["Summary"].strip()
            art.is_recipe = values["Is_Recipe"]
            art.base_folder = self.options.base_folder
            art.save_article()

    def load_folder_name(self):
        folder = sg.PopupGetFolder(
            "Select your Pelican 'content' folder.",
            "Select Folder",
            default_path=self.options.base_folder,
        )
        if folder is None:
            return "Click button to select folder --->"
        else:
            return folder


if __name__ == "__main__":
    UI()
