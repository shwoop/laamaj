import sqlite3 as lite
import sys
import appdir

con = ""
#APPDIR = "/home/alistair/repos/ircbot_laamaj"

class Database:
  con = None
  cur = None
  def connect(self, database=appdir.APPDIR+"/db/"+"laamaj.db"):
    try:
      con = lite.connect(database)
      cur = con.cursor()
      print("Connected to "+database)
    except lite.Error, e:
      print("Error : "+e.args[0])

  def close(self):
    if con:
      con.close()
      print("connection closed")
    else:
      pring("no open connection")

  def commit(self):
    if con:
     con.commit()

  def run_query(self, sequel):
    if con and cur:    
      if sequel is string:
        try:
          cur.execute(sequel)
          data = cur.fetchall()
          if data:
            print("Query Successful")
            return data;
        except lite.Error, e:
          print("Error : " + e.args[0])
          return -1


if __name__ == "__main__":
  try:
    con = lite.connect(appdir.APPDIR+"/db/"+"laamaj.db")
    cur = con.cursor()
    cur.execute("select * from users")
    users = cur.fetchall()
    for user in users:
      print(user)
  except lite.Error, e:
    print ("Error "+e.args[0])
    sys.exit(1)
  finally:
    if con:
      con.close()
