import csv
# import profile

#### Профилировщики
# line_prifiler, memory_profiler, pympler

#@profile   #--- нужно профилировать тут функцию для которой хотим применинть line_profile. kernprog -l script.py
def load():
    res = []
    with open('Pokemon.csv', 'rt') as f:
        r = csv.reader(f)
        next(r, None)  ## прочитать первую строку но никуда не записывать. Например пропустить заголовок.
        for row in r:
            res.append(row)
    return res

#@profile
def max_total(r):
    m = 0
    for row in r:
        if m < int(row[4]):
            m = int(row[4])

    return m

if __name__ == '__main__':

    # profile.run('pok_parse.max_total(pok_parse.load())')

    # import profile
    #profile.run('max_total(load())')

    print(max_total(load()))
