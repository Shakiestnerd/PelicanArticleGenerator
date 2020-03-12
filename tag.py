import PySimpleGUI as sg


def tag(tags):
    tag_list = sorted([item.strip() for item in tags.split(",")])
    check_layout = []
    for item in tag_list:
        check_layout.append([sg.Checkbox(f" {item}", pad=(10, 2))])

    layout = [
        [sg.Frame("Select Tag(s)", check_layout,), sg.Button("Scan")],
        [sg.OK(), sg.Cancel()],
    ]

    window = sg.Window("Tags", layout=layout, finalize=True)

    while True:
        event, values = window.read()
        if event in (None, "Cancel"):
            break
        elif event == "OK":
            print(event)

    window.close()


if __name__ == "__main__":
    tag("one, two, three, four, python,pysimplegui")
