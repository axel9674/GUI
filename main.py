# GUI Test Project

import PySimpleGUI as gui
import json
import ctypes

from Character import Character
from CharactersWrapper import CharactersWrapper
from CustomEncoder import CustomEncoder

from bk_auto_mission import *

with open('config.json', 'r') as json_file:
    data = json.load(json_file)["pgs"]
    json_file.close()

missioni_list = ["DragonLair", "missione2"]

character_list = []
usernames = []

selected_pg = None
pg_index = None


def Mbox(title, texts, style):
    return ctypes.windll.user32.MessageBoxW(0, "\n".join(texts), title, style)


def the_gui():
    global selected_pg, pg_index
    for selected_pg in data:
        character = Character(selected_pg["user"], selected_pg["password"], selected_pg["server"],
                              selected_pg["premium"],
                              selected_pg["mission_string"],
                              selected_pg["allineamento"], selected_pg["enabled"])

        character_list.append(character)
        usernames.append(selected_pg["user"])
        pg_index = None
        selected_pg = None

    pg_list_column = [
        [gui.Text("Lista PG")],
        [gui.Listbox(values=[], enable_events=True, size=(40, 20), key="-LISTBOX-")],
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
        [gui.Button("Start", key="-START-"), gui.Button("Stop", key="-STOP-")]
    ]

    window = gui.Window("BattleKnight auto mission", layout, finalize=True)

    def save_json():

        characters_wrapper = CharactersWrapper(character_list)

        # json_string = '{\n"pgs": ' + json.dumps([obj.__dict__ for obj in character_list], indent=4) + '\n}'
        json_string = json.dumps(characters_wrapper, indent=4, cls=CustomEncoder)

        with open('config.json', 'w') as json_file:
            json_file.write(json_string)
            json_file.close()

    def clear_form():
        window["-USERNAME-"].update("")
        window["-PASSWORD-"].update("")
        window["-SERVER-"].update("")
        window["-PREMIUM-"].update("")
        window["-MISSIONE-"].update("")
        window["-ALLINEAMENTO-"].update("")
        window["-ABILITATO-"].update("")

    def update_list():
        usernames.clear()
        for c in character_list:
            usernames.append(c["user"])

        listbox = window["-LISTBOX-"]
        listbox.update(usernames)

        for c in character_list:
            if c.enabled:
                listbox.Widget.itemconfigure(character_list.index(c), bg='green', fg='black')
            else:
                listbox.Widget.itemconfigure(character_list.index(c), bg='red', fg='black')

    while True:
        update_list()
        event, values = window.read()
        if event in (gui.WIN_CLOSED, 'Exit'):
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
                window["-MISSIONE-"].update(selected_pg["mission_string"])
                window["-ALLINEAMENTO-"].update(selected_pg["allineamento"])
                window["-ABILITATO-"].update(selected_pg["enabled"])
            except:
                pass

        elif event == "-NEW-":  # crea un nuovo pg
            pg_index = None
            selected_pg = None
            clear_form()

        elif event == "-DELETE-":  # cancella un pg
            if selected_pg is not None:
                character_list.pop(pg_index)

                pg_index = None
                selected_pg = None
                # clear_form()

                save_json()
                update_list()
            else:
                pass

        elif event == "-SAVE-":  # scrive sul json
            error_messages = []
            if selected_pg is not None:
                # sovrascrivi
                character_list.pop(pg_index)
                selected_pg.user = values["-USERNAME-"]
                selected_pg.password = values["-PASSWORD-"]
                selected_pg.server = values["-SERVER-"]
                selected_pg.premium = values["-PREMIUM-"]
                selected_pg.mission_string = values["-MISSIONE-"]
                selected_pg.allineamento = values["-ALLINEAMENTO-"]
                selected_pg.enabled = values["-ABILITATO-"]
                character_list.insert(pg_index, selected_pg)

            else:  # salva nuovo

                if values["-USERNAME-"] == "":
                    error_messages.append("Lo username non può essere vuoto")
                if values["-PASSWORD-"] == "":
                    error_messages.append("La password non può essere vuota")
                if values["-SERVER-"] == "":
                    error_messages.append("Selezionare il server")
                if values["-MISSIONE-"] == "":
                    error_messages.append("Selezionare la missione")
                if values["-ALLINEAMENTO-"] == "":
                    error_messages.append("Selezionare l'allineamento")

                if error_messages.__len__() > 0:
                    Mbox("Errore", error_messages, 0)
                else:
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
                    pg_index = character_list.__len__() - 1

            if error_messages.__len__() == 0:
                save_json()
                update_list()

        elif event == "-START-":  # inizia l'esecuzione
            bk_auto_mission(character_list)

        elif event == "-STOP-":  # inizia l'esecuzione
            for thread in threads:
                threadEvent.set()
                thread.join()

    window.close()


if __name__ == '__main__':
    the_gui()
    print('Exiting Program')
