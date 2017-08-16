import MySQLdb

db = MySQLdb.connect("11.11.11.15","root","work@good308","temp" )
 

cursor = db.cursor()
 
cursor.execute("DROP TABLE IF EXISTS TEMP_M1_TOP_TWO")
 
sql = """CREATE TABLE TEMP_M1_TOP_TWO (
         TEMP_M1_TOP_TWO INT,
         HUM_M1_TOP_TWO INT,
                 TIME CHAR(100),
                 STATE CHAR(10)
                 """

cursor.execute(sql)
 

db.close()
