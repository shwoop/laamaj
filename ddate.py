#!/usr/bin/python
# vim: set fileencoding=utf8 :

from apscheduler.scheduler import Scheduler
from subprocess import check_output

class Ddate():
    ''' Scheduling class to post ddate each morning. '''

    def __init__(self, connection, target):
        ''' Set irc details, initialise scheduler, set daily task,
        and grab the current date. '''
        self.con = connection
        self.target = target
        self.sched = Scheduler()
        self.sched.start()
        self.fetch_ddate()
        self.sched.add_cron_job(self.change_date, hour=10, minute=15)

    def change_date(self):
        ''' update ddate and announce to channel. '''
        self.fetch_ddate()
        self.post_ddate()

    def fetch_ddate(self):
        ''' fetch ddate from shell.'''
        #date = check_output(['ddate'])
        # trim `today is ` and return
        #self.date = date[9:-2]
        self.date = 'Pungenday, the 40th day of Discord in the YOLD 318'

    def post_date(self):
        ''' post date to connection/channel supplied on startup. '''
        self.con.send_msg(self.target, self.date)

    def __del__():
        ''' Kill scheduler on close. '''
        self.sched.shutdown()
