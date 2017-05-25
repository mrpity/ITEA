import base64

import xml.etree.ElementTree as et

if __name__ == '__main__':

    #print(dir(base64))
    a = base64.b64encode(b'Hello')
    print(a)
    print(base64.b64decode(a))


    # Create XML file
    '''
    root = et.Element('tasks')
    print(root)

    day = et.SubElement(root, 'day')
    print(day)
    day.set('date', '01.01.2018')
    #tasks1 = et.SubElement(day, 'Wake Up')
    #tasks2 = et.SubElement(day, 'Make coffee')

    tree = et.ElementTree(root)
    print(tree)

    task1 = et.SubElement(day, 'task')
    task1.text = 'Wake up'

    task2 = et.SubElement(day, 'task')
    task2.text = 'Make coffe'

    tree.write('tasks.xml')
    '''

    import pprint
    # Parse XML file
    tree = et.parse('tasks.xml')
    #pprint.pprint(dir(tree))

    #print(tree.getroot())
    for el in tree.findall("day[@date='01.01.2018']//task"):
        print(el.text)
