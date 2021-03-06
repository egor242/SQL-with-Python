import sqlite3


conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('''
CREATE TABLE Counts (email TEXT, count INTEGER)''')

fname = input("Enter the file name: ")
if len(fname) < 1: fname = 'mbox-short.txt'
fh = open(fname, encoding='UTF-8')
for line in fh:
    email = None
    if not ((line.startswith('From: ') or line.startswith('От:')) and ('@' in line)): continue
    pieces = line.split()
    for word in pieces:
        if '@' in word:
            email = word
    email = email.strip('<>')
    cur.execute('SELECT count FROM Counts WHERE email = ? ', (email,))
    row = cur.fetchone()
    if row is None:
        cur.execute('INSERT INTO Counts (email, count) VALUES (?, 1)', (email,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE email = ?', (email,))
    conn.commit()

sqlstr = 'SELECT email, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(row[0], row[1])

cur.close()