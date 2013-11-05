#!/usr/bin/python
# vim: set fileencoding=utf-8 :
'''
Lamaaj web portal

Stand along web portal using the laamaj resources.
'''

import database
from flask import Flask, render_template, url_for, session

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


app = Flask(__name__)
app.secret_key = u'herpy derpy doo'

_db = database.Database()

@app.route(u'/')
def relay_bitg():
    ''' Forward users accessing the domain to the youtube video. '''
    return render_template(u'redirect.htm',
        target=u'http://www.youtube.com/watch?v=my2NVhUjekA')

@app.route(u'/ttg')
def ttg():
    ''' Tugrek Toilet Goblins: list laamaj contents '''
    results = _db.exe(u'select ws_user user, ws_url url from websites order by ws_id desc')
    output = render_template(u'main.htm', urllist=results)
    return output

@app.route(u'/sess')
def sess():
    ''' toying with sessions '''
    if u'count' in session:
        output = u'count is in session: '
        count = unicode(session[u'count'])
        output += count
        count = int(count) + 1
    else:
        output = u'count is not in session'
        count = 0
    session[u'count'] = count
    return output

@app.route(u'/unsess')
def unsess():
    ''' reset /sess session '''
    session.pop(u'count', None)
    return u'reset count'


if __name__ == u'__main__':
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(80)
    IOLoop.instance().start()

    #app.run(host='0.0.0.0', port=80)
    #app.run(host='0.0.0.0', port=80, debug=True)
