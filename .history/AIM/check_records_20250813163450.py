import sqlite3

conn = sqlite3.connect('aim_data.db')
cursor = conn.cursor()

cursor.execute('SELECT COUNT(*) FROM user_data')
print('Total records:', cursor.fetchone()[0])

cursor.execute('SELECT id, name, product_type FROM user_data LIMIT 5')
print('Sample records:')
for row in cursor.fetchall():
    print(f'  ID: {row[0]}, Name: {row[1]}, Type: {row[2]}')

conn.close()
