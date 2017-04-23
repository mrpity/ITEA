import pickle
import csv
import configparser

class MyException(Exception):
    pass

class MyCSV:

    def __init__(self):
        self.filename = 'phones_csv.txt'

    def save(self, phone_dict):
        with open('{}'.format(self.filename), 'wt') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in phone_dict.items():
                writer.writerow([key, value])
        return phone_dict


    def load(filename):
        try:
            with open('{}'.format(filename), 'rt') as csv_file:
                reader = csv.reader(csv_file)
                my_dict = dict(reader)
        except Exception as e:
            return {}
        return my_dict

class MyPickle:

    def __init__(self):
         self.filename = 'phones_pickle.txt'

    def save(self, phone_dict):
        with open('{}'.format(self.filename), 'wb') as f:
            pickle.dump(phone_dict, f)

    def load(self):
        try:
            with open('{}'.format(self.filename), 'rb') as f:
                my_dict = pickle.load(f)
        except Exception as e:
            print(e, ": Return empty phonebook dictionary")
            return {}
        return my_dict


class ModelPhone:

    CONF_FILE_ = 'store_mode.cnf'
    SECTION_ = 'MAIN'
    VAR_ = 'mode'


    def __init__(self):
        self.mode = self.get_config()
        self.phonebook = self.check_mode().load()
        print(self.phonebook)

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
        elif self.mode == 'csv':
            return MyCSV()
        else:
            raise MyException("ERROR. Mode: {} isn't implemented yet".format(self.mode))

    def add(self, name, phonenumber):
        self.phonebook[name] = self.phonenumber

    def read(self, name):
        if self.phonebook[name]:
            self.phonebook("Name: {}, Phone: {}".format(name, self.phonebook[name]))

    def remove(self, name):
        if self.phonebook[name]:
            self.phonebook.pop(name)

    def update(self, name):
        if self.phonebook[name]:
            self.phonebook[name] = self.phonenumber


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
