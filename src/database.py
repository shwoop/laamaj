#!/usr/bin/python
# vim: set fileencoding=utf-8 :
##
##        DATABASE
##    
##    TODO
##    * checking for dropped connection
##

import sqlite3
import hashlib
from urllib import urlretrieve

def cur2lst(sqlite3cursor):
    ''' flip sqlite3 cursor's into lists before returning them '''
    try:
        output = [x for x in sqlite3cursor]
    except TypeError, e:
        print u'cur2lst: {0}'.format(e.strerror)
        output = []
    
    return output


class Database:
    '''
    Database Class
    Connects on init and has add_website and list_last_sites for adding
    or reading a website from the database.
    '''
    def __init__(self, care_about_threads=False, database=u'../db/laamaj.db',
            imgdir = u'../db/img/'):
        ## Create a database connection.
        self._con = None
        self._cur = None
        self._db = database
        self._care_about_threads = care_about_threads
        self._connect()

        self._imgdir = imgdir

        self._sql_insert_website = u'''INSERT INTO websites \
            (ws_date, ws_user, ws_chan, ws_url, ws_localfile) \
            VALUES (date('now'), ?, ?, ?, ?);'''
        self._sql_retreive_website = u'''SELECT ws_user||\' - \'||ws_chan\
            ||\' - \'||ws_url FROM websites WHERE ws_id > (SELECT max(ws_id) \
            FROM websites) - ? ORDER BY ws_id DESC;'''
        self._sql_duplicate_check = u'''SELECT ws_user FROM websites WHERE \
                ws_url = ? ORDER BY ws_id ASC;'''

    def __del__(self):
        self._close()


    def _connect(self):
        try:
            self._con = sqlite3.connect(self._db,
                check_same_thread=self._care_about_threads)
            self._cur = self._con.cursor()
            print(u'Connected to '+self._db)
        except sqlite3.Error, e:
            print(u'Error : '+e.args[0])


    def _close(self):
        if self._con:
            self._con.close()
            self._con = None
            self._cur = None
            print(u'connection closed')
        else:
            print(u'no open connection')
            self._cur = None


    def close(self):
        self._close()


    def _commit(self):
        if self._con:
            self._con.commit()


    def add_website(self, user, chan, website):
        print u'adding website'

        ## Linkpolis
        speedy = self._cur.execute(self._sql_duplicate_check,
                (website,)).fetchone()
        if speedy:
              status = u'repost'
              output = [speedy[0]]

        else:
            ## image check 
            exts = [u'.jpg', u'.jpeg', u'.png', u'.gif']

            if [ext for ext in exts if website.endswith(ext)]:
                origfile = website.split(u'/').pop()
                print u'Original filename: {0}'.format(origfile)
                localfilename = hashlib.md5(origfile).hexdigest() + ext[0]
                urlretrieve(website, self._imgdir + localfilename)
                status = u'image'

            else:
                localfilename = u''
                status = u'site'

            ## update the db
            output = self._cur.execute(
                self._sql_insert_website,
                (user, chan, website, localfilename))
            self._con.commit()
            output = cur2lst(output)
        
        return status, output


    def list_last_sites(self, numero=5):
        print(u'output sites')
        try:
            print((unicode(numero)))
            data = self._cur.execute(
                self._sql_retreive_website,
                (unicode(numero))
            )
            data = cur2lst(data)
            if data:
                print data
            else:
                data = [u'No Results']

        except sqlite3.Error, e:
            print u'Error : ',e.args[0]
            data = [u'Error : {error}'.format(error=e.args[0])]

        return data


    def exe(self, toexecute):
        tmp = cur2lst(self._cur.execute(toexecute))
        return tmp



if __name__ == '__main__':
    t_db = Database()
    t_db.list_last_sites()
    t_db.exe(1)
    t_db.exe(u'select count(*) from websites')
    t_db.add_website('test','test','http://www.test.com/image.jpg')
    t_db.add_website(u'test',u'test',u'http://www.test.com/')
