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
        self.__con = None
        self.__cur = None
        self.__db = database
        self.__connect()

        self.__imgdir = imgdir

    def __del__(self):
        self.__close()

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

    def close(self):
        self.__close()

    def __commit(self):
        if self.__con:
            self.__con.commit()

    def add_website(self, user, chan, website):
        print("adding website")
        exts = ['.jpg', '.jpeg', '.png', '.gif']
        for ext in exts:
            if (website.endswith(ext)):
                origfile = website.split('/')
                origfile = origfile.pop()
                print('Original filename: ' + origfile)

                localfilename = md5.new(origfile).hexdigest() + ext

                urlretrieve(website, self.__imgdir + localfilename)

                output = self.__cur.execute("INSERT INTO websites (ws_date, ws_user, ws_chan, ws_url, ws_localfile) VALUES (date('now'), ?, ?, ?, ?);", (user, chan, website, localfilename))
                self.__con.commit()
                return output

        output = self.__cur.execute("INSERT INTO websites (ws_date, ws_user, ws_chan, ws_url, ws_localfile) VALUES (date('now'), ?, ?, ?, ?);", (user, chan, website, ''))
        self.__con.commit()
        return output

    def list_last_sites(self, numero=5):
        print("output sites")
        try:
            print((str(numero)))
            data = self.__cur.execute("select ws_user||\' - \'||ws_chan||\' - \'||ws_url from websites where ws_id > (select max(ws_id) from websites) - ? order by ws_id desc;", (str(numero)))
            if data:
                print (data)
            else:
                data = "No Results"
            return(data)
        except sqlite3.Error, e:
            print("Error : ",e.args[0])
            data = "Error : {error}".format(error=e.args[0])
            return(data)
        
