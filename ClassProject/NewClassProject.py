import pickle
import csv
import configparser

class MyCVS:

    def __init__(self, filename, phone_dict):
        self.filename = filename
        self.phone_dict = phone_dict

    def save(self):
        with open('{}'.format(self.filename), 'wt') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in self.phone_dict.items():
                writer.writerow([key, value])
        return self.phone_dict


    def load(filename):
        try:
            with open('{}'.format(filename), 'rt') as csv_file:
                reader = csv.reader(csv_file)
                my_dict = dict(reader)
        except Exception as e:
            return {}
        return my_dict

class MyPickle:

    # def __init__(self):
    #     self.filename = ''

    def save(filename, phone_dict):
        with open('{}'.format(filename), 'wb') as f:
            pickle.dump(phone_dict, f)

    def load(self, filename):
        try:
            with open('{}'.format(filename), 'rb') as f:
                my_dict = pickle.load(f)
        except Exception as e:
            return {}
        return my_dict




class ModelPhone:

    CONF_FILE_ = 'store_mode.cnf'
    SECTION_ = 'MAIN'
    VAR_ = 'mode'
    PHONE_BOOK = 'phones.txt'


    def __init__(self):
        self.mode = self.get_config()
        self.phonebook = self.check_mode().load(self.PHONE_BOOK)

    def get_config(self):
        config = configparser.ConfigParser()
        config.read(self.CONF_FILE_)
        try:
            mode = config['{}'.format(self.SECTION_)]['{}'.format(self.VAR_)]
            return mode
        except KeyError:
            print("ERROR. File: {} doesn't exist or SECTION: {} isn't valid!".format(self.CONF_FILE_, self.SECTION_))

    def check_mode(self):

        if self.mode == 'pickle':
            return MyPickle()
        if self.mode == 'csv':
            return MyCVS()
        else:
            raise Exception

    def add(self):
        CONTACTS[self.name] = self.phonenumber

    def read(self):
        if CONTACTS[self.name]:
            print("Name: {}, Phone: {}".format(self.name, CONTACTS[self.name]))

    def remove(self):
        if CONTACTS[self.name]:
            CONTACTS.pop(self.name)

    def update(self):
        if CONTACTS[self.name]:
            CONTACTS[self.name] = self.phonenumber


class ControllerPhone:

    # CONF_FILE_ = 'store_mode.cnf'
    # SECTION_ = 'MAIN'
    # VAR_ = 'mode'

    def __init__(self):
        self.model_ = ModelPhone()
        # self.mode = self.get_config()
        # if self.mode == 'pickle':
        #     self.phonebook = MyPickle.load('pickle')
        # elif self.mode == 'csv':
        #     self.phonebook == MyCVS.load('csv')
        # else:
        #     raise

    # def __repr__(self):
    #     return "Class name: {}, Settings: {}".format(self.__class__.__name__, self.get_config())
    #
    # def get_config(self):
    #     config = configparser.ConfigParser()
    #     config.read(self.CONF_FILE_)
    #     try:
    #         mode = config['{}'.format(self.SECTION_)]['{}'.format(self.VAR_)]
    #         return mode
    #     except KeyError:
    #         print("ERROR. File: {} doesn't exist or SECTION: {} isn't valid!".format(self.CONF_FILE_, self.SECTION_))


if __name__ == '__main__':

    controller = ControllerPhone()
    print(controller)