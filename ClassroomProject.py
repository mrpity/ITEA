#import my_pickle
#import my_csv
import configparser
import sys

def getConfig(config_file, module_name):
    config = configparser.ConfigParser()
    conf_dir = '{}'.format(config_file)
    config.read(conf_dir)
    return config['{}'.format(module_name)]

config = getConfig('file_storage.ini', 'pickle')
print(config['module'])
print(type(config['module']))

print(config.items())
print(config)


sys.exit(0)

# contacts = my_pickle.load('phones.txt')
#contacts = my_csv.load('csv_phones.txt')


def controller():

    select = input("Choose module for storing data(pickle or csv): ")
    if select == 'csv':
        config = getConfig('file_storage.ini', '{}'.format(select))

        contacts = config['module'].load('phones.txt')
    elif select == 'pickle':
        config = getConfig('file_storage.ini', '{}'.format(select))
        contacts = config['module'].load('phones.txt')
    else:
        raise("ERROR.Cann't recognize module name!!")

    select = input("Choose actions(ad,rd,rm,up): ")
    if select == 'ad':
        name = input("Enter name: ")
        phone = input("Enter phone number: ")
        try:
            add(name, phone)
            config['module'].save('phones.txt', contacts)
        except NameError:
            print("Cann't add phone number")

    elif select == 'rd':
        name = input("Enter name for searching: ")
        try:
            read(name)
        except KeyError:
            print("Such name doesn't exist")

    elif select == 'rm':
        name = input("Enter name for removing: ")
        try:
            remove(name)
            config['module'].save('phones.txt', contacts)
        except KeyError:
            print("Such name doesn't exist")

    elif select == 'up':
        name = input("Enter name for updating: ")
        phone = input("Enter phone number for updating: ")
        try:
            update(name, phone)
            config['module'].save('phones.txt', contacts)
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

