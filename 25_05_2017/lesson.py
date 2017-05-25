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


########## DOM parser

    from xml.dom import minidom

    tree = minidom.parse('tasks.xml')
    print(tree)
    # pprint.pprint(dir(tree))
    print(tree.firstChild.firstChild)

    for el in tree.firstChild.firstChild.childNodes:
        print(el.firstChild.wholeText)


########## Stax parser

    from xml.dom import pulldom

    doc = pulldom.parse('tasks.xml')

    for event, node in doc:
        if event == pulldom.START_ELEMENT and node.localName == 'tasks':
            doc.expandNode(node)
            print(node.toxml())
            print(node.firstChild.firstChild)


######### SAX parser

    from xml import sax

    class TasksHandler(sax.ContentHandler):

        def __init__(self):
            super().__init__()
            self.is_task = False

        # открывающй тег
        def startElement(self, name, attrs):
            if name == 'task':
                self.is_task = True

        # закривающий тег
        def endElement(self, name):
            if name == 'task':
                self.is_task = False

        def characters(self, content):
            if self.is_task:
                print(content)


    parser = sax.make_parser()
    parser.setContentHandler(TasksHandler())

    a = parser.parse(open('tasks.xml', 'rt'))

    print(a)