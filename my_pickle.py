
import pickle

def save(filename, phone_dict):
    with open('{}'.format(filename), 'wb') as f:
        pickle.dump(phone_dict, f)

#contacts = {'Dima': '+380503520391', 'Pity':'+3805031231'}
#insert('my_phones.txt',contacts)

def load(filename):
    try:
        with open('{}'.format(filename), 'rb') as f:
            obj = pickle.load(f)
    except Exception as e:
        return {}
    return obj

#print((type(load('my_phones.txt'))))


