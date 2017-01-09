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




