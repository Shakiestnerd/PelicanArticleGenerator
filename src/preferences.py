import PySimpleGUI as sg
from .options import UserOptions


class Preferences:
    def __init__(self, theme="Light Brown 1"):
        self.options = options.UserOptions()
        sg.theme(new_theme=theme)
        label_size = (18, 1)
        layout = [
            [sg.Text("Article Preferences", font=("Any", 12, "bold"))],
            [
                sg.Text("Default File Type:", size=label_size),
                sg.Radio(
                    "Markdown",
                    group_id="Type",
                    default=(self.options.default_type == "md"),
                    size=label_size,
                    key="md",
                ),
                sg.Radio(
                    "Restructured Text",
                    group_id="Type",
                    key="rst",
                    default=(self.options.default_type == "rst"),
                ),
            ],
            [
                sg.Text("Content Folder:", size=label_size),
                sg.Input(
                    default_text=self.options.base_folder,
                    key="Content",
                    enable_events=True,
                    size=(50, 1),
                ),
                sg.Button(button_text="..."),
            ],
            [
                sg.Text("Default Author:", size=label_size),
                sg.Input(key="Author", size=(50, 1)),
            ],
            [
                sg.Text("Common Tags:", size=label_size),
                sg.Input(
                    key="Tags",
                    size=(50, 1),
                    tooltip="Comma separated list of tags / key words.",
                ),
            ],
            [
                sg.Text("Categories:", size=label_size),
                # sg.Input(key="Categories:", size=(50, 1)),
                sg.Listbox(values=["One", "Two", "Three", "Four"], size=(50, 7)),
                sg.Button(button_text="Scan"),
            ],
            [sg.Button(button_text="Save"), sg.Button(button_text="Cancel")],
        ]

        window = sg.Window("Article Generator", layout)
        event, values = window.read()


if __name__ == "__main__":
    Preferences()
