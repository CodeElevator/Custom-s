import sqlite3

db = sqlite3.connect("DB.sqlite")
cur = db.cursor()
result = cur.execute("SELECT role FROM rolereact WHERE msg_id = ? AND emoji = ?",(1043988724574330880, str("🟦")
))
r = result.fetchall()
for entry in r:
    print(entry[0])