import PySimpleGUI as sg
import webbrowser


def about():
    """An about box to let people know the underlying information about the application.
    """
    layout = [
        [sg.Text("Article Generator", font=("Arial", 12), justification="center")],
        [sg.Text("Version: 0.5")],
        [sg.Text("Create a new blank article in markdown\nor restructured text format.\n")],
        [sg.Text("Author: Shakiestnerd")],
        [sg.Text("License: MIT License")],
        [
            sg.Text(
                "http://www.canofworms.com",
                key="website",
                font=("All", 10, "underline"),
                text_color="blue",
                enable_events=True,
            )
        ],
        [sg.OK()],
    ]

    window = sg.Window("About", layout=layout, finalize=True)
    window["website"].set_cursor(cursor="hand2")
    while True:
        event, values = window.read()
        if event in (None, "OK"):
            break
        if event == "website":
            webbrowser.open(window["website"].DisplayText)
            break
    window.close()
