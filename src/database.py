##
##        DATABASE
##    
##    TODO
##    * checking for dropped connection
##

import sqlite3
import md5
from urllib import urlretrieve

class Database:
    """
    Database Class
    Connects on init and has add_website and list_last_sites for adding or reading a website from the database.
    """
    def __init__(self, database="../db/laamaj.db", imgdir = '../db/img/'):
        self._con = None
        self._cur = None
        self._db = database
        self._connect()

        self._imgdir = imgdir

    def __del__(self):
        self._close()

    def _connect(self):
        try:
            self._con = sqlite3.connect(self._db)
            self._cur = self._con.cursor()
            print("Connected to "+self._db)
        except sqlite3.Error, e:
            print("Error : "+e.args[0])

    def _close(self):
        if self._con:
            self._con.close()
            self._con = None
            self._cur = None
            print("connection closed")
        else:
            print("no open connection")
            self._cur = None

    def close(self):
        self._close()

    def _commit(self):
        if self._con:
            self._con.commit()

    def add_website(self, user, chan, website):
        print("adding website")
        exts = ['.jpg', '.jpeg', '.png', '.gif']
        for ext in exts:
            if (website.endswith(ext)):
                origfile = website.split('/')
                origfile = origfile.pop()
                print('Original filename: ' + origfile)

                localfilename = md5.new(origfile).hexdigest() + ext

                urlretrieve(website, self._imgdir + localfilename)

                output = self._cur.execute("INSERT INTO websites (ws_date, ws_user, ws_chan, ws_url, ws_localfile) VALUES (date('now'), ?, ?, ?, ?);", (user, chan, website, localfilename))
                self._con.commit()
                return output

        output = self._cur.execute("INSERT INTO websites (ws_date, ws_user, ws_chan, ws_url, ws_localfile) VALUES (date('now'), ?, ?, ?, ?);", (user, chan, website, ''))
        self._con.commit()
        return output

    def list_last_sites(self, numero=5):
        print("output sites")
        try:
            print((str(numero)))
            data = self._cur.execute("select ws_user||\' - \'||ws_chan||\' - \'||ws_url from websites where ws_id > (select max(ws_id) from websites) - ? order by ws_id desc;", (str(numero)))
            if data:
                print (data)
            else:
                data = "No Results"
            return(data)
        except sqlite3.Error, e:
            print("Error : ",e.args[0])
            data = "Error : {error}".format(error=e.args[0])
            return(data)


if __name__ == "__main__":
    t_db = Database()
    t_db.list_last_sites()
