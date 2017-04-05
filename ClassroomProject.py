# contacts = {'Dima': '+380503520391', 'Pity':'+3805031231'}
import my_pickle
import my_csv

# contacts = my_pickle.load('phones.txt')
contacts = my_csv.load('csv_phones.txt')


def controller():
    select = input("Choose actions(ad,rd,rm,up): ")
    if select == 'ad':
        name = input("Enter name: ")
        phone = input("Enter phone number: ")
        try:
            add(name, phone)
            my_csv.save('csv_phones.txt', contacts)
#            my_pickle.save('phones.txt', contacts)
        except NameError:
            print("Cann't add phone number")

    elif select == 'rd':
        name = input("Enter name for searching: ")
        try:
#            read(name)
            my_csv.read('csv_phones.txt', name)
        except KeyError:
            print("Such name doesn't exist")

    elif select == 'rm':
        name = input("Enter name for removing: ")
        try:
            remove(name)
#            my_pickle.save('phones.txt', contacts)
        except KeyError:
            print("Such name doesn't exist")

    elif select == 'up':
        name = input("Enter name for updating: ")
        phone = input("Enter phone number for updating: ")
        try:
            update(name, phone)
#            my_pickle.save('phones.txt', contacts)
        except KeyError:
            print("Such name doesn't exist")
    else:
        print("I donn't know such action")


def add(name, phone):
    contacts[name] = phone


def read(name):
    if contacts[name]:
        print("Name: {}, Phone: {}".format(name, contacts[name]))


def remove(name):
    if contacts[name]:
        contacts.pop(name)


def update(name, phone):
    if contacts[name]:
        contacts[name] = phone


controller()

