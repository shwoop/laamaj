#!/usr/bin/python
# vim: set fileencoding=utf-8 :
'''
Lamaaj web portal

Stand along web portal using the laamaj resources.
'''

import database
from flask import Flask, render_template, url_for, session, jsonify, request
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

app = Flask(__name__)
app.secret_key = u'herpy derpy doo'

_db = database.Database()

REC_PER_PAGE = 10
FETCH_RECORDS_SQL = u'select ws_user, ws_url from websites where \
ws_id between {0} and {1} order by ws_id desc'

@app.route(u'/')
def relay_bitg():
    ''' Forward users accessing the domain to the youtube video. '''
    return render_template(u'redirect.htm',
        target=u'http://www.youtube.com/watch?v=my2NVhUjekA')

@app.route("/ip_echoj", methods=["GET"])
def ip_echo_json():
    ''' echo client ip address as json'''
    return jsonify({'ip': request.remote_addr}), 200

@app.route("/ip_echo", methods=["GET"])
def ip_echo():
    ''' echo client ip address '''
    return request.remote_addr, 200

@app.route(u'/ttg')
def ttg():
    ''' Tugrek Toilet Goblins: list laamaj contents '''
    head = int(_db.exe(u'select max(ws_id) from websites')[0][0])
    tail = head - REC_PER_PAGE if head - REC_PER_PAGE > 0 else 0
    results = _db.exe(FETCH_RECORDS_SQL.format(tail, head))
    output = render_template(u'main.htm', urllist=results)
    session[u'lastrecord'] = tail
    return output

@app.route(u'/cert')
def certificate():
    ''' present ssl certificate. '''
    output = render_template(u'cert.htm')
    return output

def _format_link(user, url):
    ''' return url format for each record displaying user and url. '''
    return u'{0}: <a href="{1}">{1}</a><br>'.format(user, url)

@app.route(u'/_more')
def _more():
    ''' Restful ajax call to return jason of next X records. '''
    if u'lastrecord' not in session:
        return jsonify(result = u'Something is Fucked<br>')
    fr = int(session[u'lastrecord']) - 1
    nlr = fr - REC_PER_PAGE if fr - REC_PER_PAGE > 0 else 0
    print u'fr: {0}, nlr: {1}.'.format(fr, nlr)
    results = _db.exe(FETCH_RECORDS_SQL.format(nlr, fr))
    outlist = [_format_link(usr, url) for usr, url in results]
    output = u''.join(outlist)
    session[u'lastrecord'] = nlr
    return jsonify(result = output,
            end = nlr == 0)

if __name__ == u'__main__':
    ''' Launch web service pointing to the app. '''
    https_server = HTTPServer(WSGIContainer(app),
        ssl_options={u'certfile': u'kyz/cert.pem',
            u'keyfile': u'kyz/key.pem'})

    ## rather than bind to 443 using sudo
    ## set up iptables redirect from 442 to 8869 and run as user
    https_server.listen(8869)
    IOLoop.instance().start()

    #app.run(host='0.0.0.0', port=80, debug=True)
