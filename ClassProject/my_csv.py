
import csv

def save(filename, my_dict):
    with open('{}'.format(filename), 'wt') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in my_dict.items():
            writer.writerow([key, value])
    return my_dict


#def read(filename, name):
#    with open('{}'.format(filename), 'rt') as csv_file:
#        reader = csv.reader(csv_file)
#        my_dict = dict(reader)
#    return name, my_dict[name]


def load(filename):
    try:
        with open('{}'.format(filename), 'rt') as csv_file:
            reader = csv.reader(csv_file)
            my_dict = dict(reader)
    except Exception as e:
        return {}
    return my_dict


