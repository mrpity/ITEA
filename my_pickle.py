
import pickle

def save(filename, phone_dict):
    with open('{}'.format(filename), 'wb') as f:
        pickle.dump(phone_dict, f)


def load(filename):
    try:
        with open('{}'.format(filename), 'rb') as f:
            my_dict = pickle.load(f)
    except Exception as e:
        return {}
    return my_dict


def decor_save(filename, phone_dict):
    def decor(add_f):
        def wrapper(name, phone):
            add_f(name, phone)
            with open('{}'.format(filename), 'wb') as f:
                pickle.dump(phone_dict, f)
        return wrapper
    return decor


