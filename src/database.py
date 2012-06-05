import sqlite3
#import sys


class Database:
  def __init__(self, database="../db/laamaj.db"):
    self.__con = None
    self.__cur = None
    self.__db = database

  def __connect(self):
    try:
      self.__con = sqlite3.connect(self.__db)
      self.__cur = self.__con.cursor()
      print("Connected to "+self.__db)
    except sqlite3.Error, e:
      print("Error : "+e.args[0])

  def __close(self):
    if self.__con:
      self.__con.close()
      self.__con = None
      self.__cur = None
      print("connection closed")
    else:
      print("no open connection")
      self.__cur = None

  def __commit(self):
    if self.__con:
      self.__con.commit()

  def __run_query(self, sequel):
    if self.__con and self.__cur:    
      if isinstance(sequel, str):
        try:
          self.__cur.execute(sequel)
          print("query run")
          data = self.__cur.fetchall()
          if data:
            print("Query Successful")
            return data;
        except sqlite3.Error, e:
          print("Error : " + e.args[0])
          return False
      else:
        print("sequel not a string")
    else:
      print("connection and/or cursor not valid")

  def add_website(self, user, chan, website):
    print("adding website")
    self.__connect()
    output = self.__run_query("INSERT INTO websites (ws_date, ws_user, ws_chan, ws_url) VALUES (date(\'now\'),\'"+user+"\',\'"+chan+"\',\'"+website+"\');")
    self.__commit()
    self.__close()
    return output

  def list_last_sites(self, numero=5):
    print("output sites")
    try:
      self.__connect()
      data = self.__run_query("select ws_user||\' - \'||ws_chan||\' - \'||ws_url from websites where ws_id > (select max(ws_id) from websites) - "+str(numero)+" order by ws_id desc;")
      if data:
        print (data)
    except sqlite3.Error, e:
      print("Error : ",e.args[0])
      data = False
    finally:
      self.__close()
      return data
    






if __name__ == "__main__":
  db = Database()
  try:
    db.__connect()
    data = db.__run_query("select count(*) from websites")
    if data:
      for d in data:
        print(d[0])
  except sqlite3.Error, e:
    print("Error : "+e.args[0])
  finally:
    db.__close()
    db = None
