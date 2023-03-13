import sqlite3 as sql 

con = sql.connect("urls.db")
cursor = con.cursor()

query = "CREATE TABLE url_data(short_url TEXT primary key, url TEXT )"

cursor.execute(query)

con.commit()

cursor.close()
con.close()
