#!/usr/bin/python
# vim: set fileencoding=utf-8 :
'''
Lamaaj web portal

Stand along web portal using the laamaj resources.
'''

import database
from flask import Flask, render_template, url_for, session, jsonify
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


app = Flask(__name__)
app.secret_key = u'herpy derpy doo'

_db = database.Database()


REC_PER_PAGE = 10

@app.route(u'/')
def relay_bitg():
    ''' Forward users accessing the domain to the youtube video. '''
    return render_template(u'redirect.htm',
        target=u'http://www.youtube.com/watch?v=my2NVhUjekA')

@app.route(u'/ttg')
def ttg():
    ''' Tugrek Toilet Goblins: list laamaj contents '''
    head = int(_db.exe(u'select max(ws_id) from websites')[0][0])
    tail = head - REC_PER_PAGE if head - REC_PER_PAGE > 0 else 0
    results = _db.exe(u'select ws_user, ws_url from websites where ws_id between {0} and {1} order by ws_id desc'.format(tail, head))
    output = render_template(u'main.htm', urllist=results)
    session[u'lastrecord'] = tail
    return output

@app.route(u'/_more')
def _more():
    if u'lastrecord' not in session:
        return jsonify(result = u'Something is Fucked<br>')
    fr = int(session[u'lastrecord']) - 1
    nlr = fr - REC_PER_PAGE if fr - REC_PER_PAGE > 0 else 0
    print u'fr: {0}, nlr: {1}.'.format(fr, nlr)
    results = _db.exe(u'select trim(ws_user), trim(ws_url) from websites where ws_id between {0} and {1} order by ws_id desc'.format(nlr, fr))
    output = u''
    for usr, url in results:
        output += u'{0}: <a href="{1}">{1}</a><br>'.format(usr, url)
    session[u'lastrecord'] = nlr
    return jsonify(result = output,
            end = nlr == 0)


if __name__ == u'__main__':
    '''http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(80)
    IOLoop.instance().start()'''

    app.run(host='0.0.0.0', port=80, debug=True)
