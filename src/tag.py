import PySimpleGUI as sg


def tag(tags, cats, folder):
    tag_list = []
    check_layout = []
    results = []
    if type(tags) is str:
        tag_list = sorted([item.strip() for item in tags.split(",")])
    else:
        tag_list = tags

    layout = [
        [sg.Text(text="Tag Selector")],
        [
            sg.Text(text="Add New Tag:"),
            sg.Input(key="Tag"),
            sg.Button(button_text="Add", key="Add"),
        ],
        [
            sg.Text(text="Select Tags:"),
            sg.Listbox(
                values=tag_list,
                key="Tag_List",
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                size=(45, 10),
            ),
            sg.Button("Scan", key="Scan"),
        ],
        [sg.OK(), sg.Cancel()],
    ]

    window = sg.Window("Tags", layout=layout, finalize=True)

    while True:
        event, values = window.read()
        if event in (None, "Cancel"):
            break
        elif event == "OK":
            results = window["Tag_List"].get()

            if not results:
                print("No tags selected.")
            break
        elif event == "Scan":
            tag_scan(folder, cats)
        elif event == "Add":
            tag_add(values["Tag"], window["Tag_List"].get_list_values())
            window["Tag_List"].update(tag_list)
            window["Tag"].update("")

    window.close()
    print(results)
    return results


def tag_add(value, tags):
    print(value, tags)
    tags.append(value)


def tag_scan(folder, categories):
    print(folder)
    for category in categories:
        print(category)


if __name__ == "__main__":
    tag(
        ["one", "two", "three", "four", "python", "pysimplegui"],
        ["Technology", "Family"],
        "/home/keith/pyprojects/blog-pelican/content",
    )
