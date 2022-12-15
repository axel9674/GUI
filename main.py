# GUI Test Project

import PySimpleGUI as gui
import json

from Character import Character

with open('config.json', 'r') as json_file:
    data = json.load(json_file)["pgs"]
    json_file.close()

missioni_list = ["DragonLair", "missione2"]

character_list = []
usernames = []

pg_index = None
selected_pg = None

for selected_pg in data:
    character = Character(selected_pg["user"], selected_pg["password"], selected_pg["server"], selected_pg["premium"],
                          selected_pg["missionString"],
                          selected_pg["allineamento"], selected_pg["enabled"])

    character_list.append(character)
    usernames.append(selected_pg["user"])

pg_list_column = [
    [gui.Text("Lista PG")],
    [gui.Listbox(values=usernames, enable_events=True, size=(40, 20), key="-LISTBOX-")],
    [gui.Button("NEW", key="-NEW-")]
]

pg_viewer_column = [
    [gui.Text("Username: "), gui.InputText(size=(40, 1), key="-USERNAME-")],
    [gui.Text("Password: "), gui.InputText(size=(40, 1), key="-PASSWORD-")],
    [gui.Text("Server: "), gui.InputText(size=(40, 1), key="-SERVER-")],
    [gui.Text("Premium: "), gui.Checkbox('', key="-PREMIUM-")],
    [gui.Text("Missione: "), gui.DropDown(values=missioni_list, key="-MISSIONE-")],
    [gui.Text("Allineamento: "), gui.DropDown(values=["buono", "malvagio"], key="-ALLINEAMENTO-")],
    [gui.Text("Abilitato: "), gui.Checkbox('', key="-ABILITATO-")],
    [gui.Button("SAVE", key="-SAVE-"), gui.Button("DELETE", key="-DELETE-")]
]

layout = [
    [
        gui.Column(pg_list_column),
        gui.VSeperator(),
        gui.Column(pg_viewer_column),
    ],
    [gui.Button("Start", key="-START-")]
]

window = gui.Window("Image Viewer", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == gui.WIN_CLOSED:
        break

    elif event == "-LISTBOX-":  # A file was chosen from the listbox
        try:
            username = ''.join(values[event])
            pg_index = usernames.index(username)
            selected_pg = character_list[pg_index]
            window["-USERNAME-"].update(selected_pg["user"])
            window["-PASSWORD-"].update(selected_pg["password"])
            window["-SERVER-"].update(selected_pg["server"])
            window["-PREMIUM-"].update(selected_pg["premium"])
            window["-MISSIONE-"].update(selected_pg["missionString"])
            window["-ALLINEAMENTO-"].update(selected_pg["allineamento"])
            window["-ABILITATO-"].update(selected_pg["enabled"])
        except:
            pass

    elif event == "-NEW-":  # crea un nuovo pg
        pg_index = None
        selected_pg = None
        window["-USERNAME-"].update("")
        window["-PASSWORD-"].update("")
        window["-SERVER-"].update("")
        window["-PREMIUM-"].update("")
        window["-MISSIONE-"].update("")
        window["-ALLINEAMENTO-"].update("")
        window["-ABILITATO-"].update("")

    elif event == "-DELETE-":  # cancella un pg
        if selected_pg is not None:
            character_list.pop(pg_index)

            pg_index = None
            selected_pg = None
            window["-USERNAME-"].update("")
            window["-PASSWORD-"].update("")
            window["-SERVER-"].update("")
            window["-PREMIUM-"].update("")
            window["-MISSIONE-"].update("")
            window["-ALLINEAMENTO-"].update("")
            window["-ABILITATO-"].update("")

            json_string = '{"pgs": ' + json.dumps([obj.__dict__ for obj in character_list]) + ' }'

            with open('config.json', 'w') as json_file:
                json_file.write(json_string)
                json_file.close()

            usernames.clear()
            for c in character_list:
                usernames.append(c["user"])

            window["-LISTBOX-"].update(usernames)
        else:
            pass

    elif event == "-SAVE-":  # scrive sul json
        if selected_pg is not None:
            # sovrascrivi
            character_list.pop(pg_index)
            selected_pg.user = values["-USERNAME-"]
            character_list.insert(pg_index, selected_pg)

        else:  # salva nuovo
            new_character = Character(
                values["-USERNAME-"],
                values["-PASSWORD-"],
                values["-SERVER-"],
                values["-PREMIUM-"],
                values["-MISSIONE-"],
                values["-ALLINEAMENTO-"],
                values["-ABILITATO-"])

            character_list.append(new_character)
            selected_pg = new_character
            pg_index = character_list.__len__() + 1

        json_string = '{"pgs": ' + json.dumps([obj.__dict__ for obj in character_list]) + ' }'

        with open('config.json', 'w') as json_file:
            json_file.write(json_string)
            json_file.close()

        usernames.clear()
        for c in character_list:
            usernames.append(c["user"])

        window["-LISTBOX-"].update(usernames)


    elif event == "-START-":  # inizia l'esecuzione
        break

window.close()
