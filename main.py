from address_book import AddressBook, Record
import pickle

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            return str(error)
        except IndexError:
            return "Enter all required arguments."
        except KeyError:
            return "Contact not found."
    return inner


@input_error
def add_contact(args, book):
    name, phone = args
    name = name.lower()

    record = book.find(name)

    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."

    record.add_phone(phone)
    return "Contact updated."


@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    name = name.lower()

    record = book.find(name)

    if record is None:
        raise KeyError

    record.edit_phone(old_phone, new_phone)
    return "Contact changed."


@input_error
def phone_contact(args, book):
    name = args[0].lower()

    record = book.find(name)

    if record is None:
        raise KeyError

    phones = "; ".join(str(phone) for phone in record.phones)

    return f"{record.name.value}: {phones}"


@input_error
def show_all(book):
    if not book:
        return "No contacts saved."

    return "\n".join(str(record) for record in book.values())


@input_error
def add_birthday(args, book):
    name, birthday = args
    name = name.lower()

    record = book.find(name)

    if record is None:
        raise KeyError

    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book):
    name = args[0].lower()

    record = book.find(name)

    if record is None:
        raise KeyError

    if record.birthday is None:
        return "Birthday is not set."

    birthday = record.birthday.value.strftime("%d.%m.%Y")
    return f"{record.name.value}'s birthday is {birthday}"


@input_error
def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()

    if not upcoming_birthdays:
        return "No upcoming birthdays."

    lines = []

    for birthday in upcoming_birthdays:
        lines.append(
            f"{birthday['name']}: "
            f"{birthday['congratulation_date']}"
        )

    return "\n".join(lines)


def parse_input(user_input):
    parts = user_input.split()

    if not parts:
        return "", []

    command, *args = parts
    return command.lower(), args


def main():
    book = load_data()
    # book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ").strip()
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(phone_contact(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()