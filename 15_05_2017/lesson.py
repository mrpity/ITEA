import sqlite3


## Databases

if __name__ == '__main__':

    db = sqlite3.connect("/home/dkhodakivsky/Downloads/test/db.sqlite3")
    print(db)

    cursor = db.cursor()
    print(cursor)
    c1 = cursor.execute("select * from groups")

    c1.fetchone()  ## получить 1 строку

    for row in c1:
        print(row)

    cursor.execute("insert into groups (ids, name_g) values (?, ?)", (1, 'AA-16'))   ### ? -- отправляются данные по частям. сначала отправляются вопросы. потом данные которые надо поставить вместо ?

    db.commit()
    db.close()
    #cursor.close()