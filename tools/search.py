import sqlite3

text  = '%รถ%'
database = "../database.db"
try:
    with sqlite3.connect(database) as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM documents WHERE title like ? OR content like ? ',(text,text))
        rows = cur.fetchall()
        for row in rows:
            print(row[1])

except sqlite3.Error as e:
    print(e)