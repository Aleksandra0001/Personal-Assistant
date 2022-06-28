from pick import pick
from difflib import get_close_matches
from styles import show_records, show_notes, show_print
from classes import Record, SomeBook, Name, Phone, Address, Email, Birthday, NoteBookRecord, NoteBookText, NoteBookTeg

addressbook = SomeBook('data.bin')
notebook = SomeBook('notebook_data.bin')
add_commands = ["add", "+", "new"]
exit_commands = ["exit", "bye", "goodbye", "close"]
update_commands = ["update", "change", "edit"]
back_to_menu_commands = ["menu", "quit", "back to menu", "back"]

commands = [f'{", ".join(add_commands)}', "show", "delete", "find", f'{", ".join(update_commands)}', "menu",
            "help", f'{", ".join(exit_commands)}']
description = ['Add contact', 'Show contacts', 'Delete Contact', 'Find Contact', 'Update Contact', 'Back to Menu',
               'Help', 'Exit Commands']

all_commands = commands + add_commands + exit_commands + update_commands + back_to_menu_commands

menu_title = f"Hi! Welcome to personal assistant bot!\nSelect menu option please.\n{'=' * 60}".upper()
menu_options = ["AddressBook", "NoteBook", "Help", "Folder Sorter ", "Exit"]

submenu_options = [f"{cmd:<20} -  {desc}" for cmd, desc in zip(commands, description)]
submenu_title = f"Command name and description. Select command.\n{'=' * 46}"


def show_menu():
    option, index = pick(menu_options, menu_title, indicator="=>")
    print(f"You have chosen a command: {option}.\nLet's continue.\n{'=' * 60}")

    return menu_switcher(index)


def menu_switcher(index):
    if index == 0:
        print("welcome to Addressbook")
        addressbook.load_data()
        command = input("Write your command: ").casefold().strip()
        while command_handler(command):
            command = input("Write your command: ").casefold().strip()

    if index == 1:
        print("Welcome to Notebook")
        notebook.load_data()
        command = input("Write your command: ").casefold().strip()
        while notes_handler(command):
            command = input("Write your command: ").casefold().strip()
    if index == 2:
        show_submenu()
    if index == 3:
        print("Welcome to Folder Sorter")  # запускаем функцию сортировки
    if index == 4:
        print("See you later!")
        addressbook.save_data()
        notebook.save_data()


def show_submenu():
    option, index = pick(submenu_options, submenu_title, indicator="=>")
    option = option.split(" - ")[1]
    print(f"You have chosen a command: {option}.\nLet's continue.\n{'=' * 60}")

    return submenu_switcher(index)


def submenu_switcher(index):
    return command_handler(index)


def show_edit_submenu():
    edit_options = ["Contact name", "Contact phone number", "contact address", "Contact email", "Contact birthday",
                    "Back"]
    option, index = pick(edit_options, f"Choose a field to update:\n{'=' * 60}", indicator="=>")
    print(f"You have chosen a command: {option}.\nLet's continue.\n{'=' * 60}")
    return index


def command_handler(command):
    if not isinstance(command, int):
        try:
            command = get_close_matches(command, all_commands, n=1, cutoff=0.5)[0]
            # print(all_commands)
            print(f'You have chosen a command: {command}')
        except IndexError:
            print("Sorry, I don't understand. Please try again.")
            return True
    if command == "help" or command == 6:
        show_submenu()
        # return command_handler(show_commands())
    if command == "add" or command == 0:
        try:
            name = input("Enter name: ").title().strip()
            phone_number = input("Enter phone-number: ").strip()
            address = input("Enter address: ").strip()
            email = input("Enter email: ").strip()
            birthday = input("Enter birthday dd-mm-yyyy: ").strip()
            record = Record(Name(name), Phone(phone_number), Address(address), Email(email))
            record.add_birthday(Birthday(birthday))
            addressbook.add_record(record)
            addressbook.save_data()
            return True
        except ValueError as e:
            print(f"Sorry, {e}. Please try again.")
            return True
    if command == "show" or command == 1:
        show_records(addressbook)
        return True
    if command == "delete" or command == 2:
        name = input("Enter name: ").title().strip()
        addressbook.delete_record(name)
        addressbook.save_data()
        return True
    if command == "find" or command == 3:
        value = input("Enter name/phone/birthday for find: ")
        addressbook.to_find(value)
        return True
    if command in update_commands or command == 4:
        updated_position = show_edit_submenu()
        if updated_position == 0:
            old_value = input("Enter old name: ").title()
            new_value = input("Enter new name: ").title()
            addressbook.update_record(old_value, new_value)
            addressbook.save_data()
            return True
        elif updated_position == 1:
            old_value = input("Enter old phone-number: ")
            new_value = input("Enter new phone-number: ")
            addressbook.update_record(old_value, Phone(new_value))
            return True
        elif updated_position == 2:
            old_value = input("Enter old address: ").strip()
            new_value = input("Enter new address: ").strip()
            addressbook.update_record(old_value, Address(new_value))
            addressbook.save_data()
            return True
        elif updated_position == 3:
            old_value = input("Enter old email: ").strip()
            new_value = input("Enter new email: ").strip()
            addressbook.update_record(old_value, Email(new_value))
            return True
        elif updated_position == 4:
            old_value = input("Enter old birthday: ")
            new_value = input("Enter new birthday: ")
            addressbook.update_record(old_value, new_value)
            return True
        elif updated_position == 5:
            addressbook.save_data()
            return True
        else:
            print("Wrong command")
            return True
    if command in back_to_menu_commands or command == 5:
        show_menu()
        return True
    if command in exit_commands or command == 7:
        print("Goodbye!")
        addressbook.save_data()
        return False
    else:
        print("Unknown command")


def notes_handler(command):
    if not isinstance(command, int):
        try:
            command = get_close_matches(command, all_commands, n=1, cutoff=0.5)[0]
            print(f'You have chosen a command: {command}')
        except IndexError:
            print("Sorry, I don't understand. Please try again.")
            return True
    if command == "help" or command == 6:
        show_submenu() #дополнить команды по notes
    if command == "add" or command == 0:
        try:
            title = input("Enter title: ").title().strip()
            text = input("Enter text: ").strip()
            teg = input("Enter tag like teg1, teg2: ").strip()
            show_print([title, text, teg])
            note = NoteBookRecord(Name(title), NoteBookText(text))
            tegs_list = teg.split(',')
            for tg in tegs_list:
                note.add_teg(NoteBookTeg(tg.strip()))
            notebook.add_record(note)
            notebook.save_data()
            return True
        except ValueError as e:
            print(f"Sorry, {e}. Please try again.")
            return True
    if command == "show" or command == 1:
        # show_notes(notebook)
        print("\n".join([f"{v}" for k, v in notebook.items()]) if len(
        notebook) > 0 else 'Contacts are empty')
        return True
    if command == "delete" or command == 2:
        title = input("Enter title: ").title().strip()
        notebook.pop(title)
        notebook.save_data()
        return True
    if command == "find" or command == 3:
        value = input("Enter value for find: ")
        result_str = ''
        for k, v in notebook.items():
            found = False
            if value.title() in k.title():
                found = True
            text = v.text.value.upper()
            if text.find(value.upper()) != -1:
                found = True
            else:
                for teg in v.tegs:
                    tg = teg.value.upper()
                    if tg.find(value.upper()) != -1:
                        found = True
            if found:
                result_str += f'{v}\n'
        print(result_str if result_str else 'Nothing found')
        return True
    if command in update_commands or command == 4:
        updated_position = show_edit_note_submenu()
        if updated_position == 0:
            old_title = input("Enter old title: ").title().strip()
            new_title = input("Enter new title: ").title().strip()
            new_value = str(new_title)
            for name, record in notebook.data.items():
                if name == old_title:
                    record.name.value = new_value
                    notebook.pop(old_title)
                    notebook[new_value] = record
                    print(f"Record {old_title} was updated to {new_value}")
                    return True
            notebook.save_data()
            return True
        if updated_position == 1:
            name = input("Enter name: ").title().strip()
            new_text = input("Enter new text: ").strip()
            note = notebook.get(name, -1)
            if note != -1:
                note.text = NoteBookText(new_text)
            else:
                print(f'Note title {name} is nit found')
            notebook.save_data()
            return True
        if updated_position == 2:
            name = input("Enter name: ").title().strip()
            new_teg = input("Enter new tag: ").strip()
            note = notebook.get(name, -1)
            if note != -1:
                note.add_teg(NoteBookTeg(new_teg))
            notebook.save_data()
            return True
        if updated_position == 3:
            name = input("Enter name: ").title().strip()
            new_teg = input("Enter del tag: ").strip()
            note = notebook.get(name, -1)
            if note != -1:
                note.del_teg(new_teg)
            notebook.save_data()
            return True
    if command in back_to_menu_commands or command == 5:
        show_menu()
        return True
    if command in exit_commands or command == 7:
        print("Goodbye!")
        notebook.save_data()
        return False
    else:
        print("Unknown command")


def show_edit_note_submenu():
    edit_options = ["Note title", "Note text", "Add note tag", "Del note tag","Back"]
    option, index = pick(edit_options, f"Choose a field to update:\n{'=' * 60}", indicator="=>")
    print(f"You have chosen a command: {option}.\nLet's continue.\n{'=' * 60}")
    return index
