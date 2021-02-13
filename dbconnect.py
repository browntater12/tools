import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd = "Browntater12")
    c = conn.cursor()
    c.execute("CREATE DATABASE tools;")
    return c, conn
		
connection()