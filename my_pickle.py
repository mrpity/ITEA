
import pickle

def save(filename, phone_dict):
    with open('{}'.format(filename), 'wb') as f:
        pickle.dump(phone_dict, f)


def load(filename):
    try:
        with open('{}'.format(filename), 'rb') as f:
            obj = pickle.load(f)
    except Exception as e:
        return {}
    return obj


