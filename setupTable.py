import sqlite3

conn = sqlite3.connect('database.db')
print ("Opened database successfully");

conn.execute('CREATE TABLE products (name TEXT, content TEXT, price TEXT, weight TEXT)')
print ("Table created successfully");
conn.close()