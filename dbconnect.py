#in case you want to use MySQL instead on your local host, use this confgiuration
import MySQLdb
import sys
try:
    conn = MySQLdb.Connect(
        host='localhost',
        user='root',
        passwd='',
        db ='mydata'
    )
except Exception as e:
    sys.exit("we can not get to database")
# c = conn.cursor()




