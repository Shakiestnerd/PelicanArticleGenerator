import PySimpleGUI as sg
import os


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
            tag_list = tag_scan(folder, cats)
            window["Tag_List"].update(tag_list)
        elif event == "Add":
            tag_add(values["Tag"], window["Tag_List"].get_list_values())
            window["Tag_List"].update(tag_list)
            window["Tag"].update("")

    window.close()
    print(results)
    return results, tag_list


def tag_add(value, tags):
    print(value, tags)
    tags.append(value)


def tag_scan(folder, categories):
    """ Scan all existing blog articles and extract the tags """
    print(folder)
    results = []
    for category in categories:
        print(category)
        path = os.path.join(folder, category)
        blogfiles = [
            f for f in os.listdir(path) if f.endswith(".rst") or f.endswith(".md")
        ]
        for file in blogfiles:
            with open(os.path.join(path, file)) as f:
                for line in f.readlines():
                    if line[:5] == "Tags:":
                        results += [x.strip() for x in line[6:].split(",")]

    return sorted(set(results))


if __name__ == "__main__":
    tag(
        ["one", "two", "three", "four", "python", "pysimplegui"],
        ["Technology", "Family"],
        "/home/keith/pyprojects/blog-pelican/content",
    )
