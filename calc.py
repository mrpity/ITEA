FILE_NAME='/tmp/test.log'




if __name__ == '__main__':

    mydict = {}
    with open(FILE_NAME, 'r') as f:
        for line in f.readlines():
            for word in line.split():
                if not mydict[word]:
                    mydict[word] = 1
                elif mydict[word]:
                    mydict[word] += 1

    print(mydict)