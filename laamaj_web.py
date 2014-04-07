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
from re import match

app = Flask(__name__)
app.secret_key = u'herpy derpy doo'

_db = database.Database(database=u'/home/shwoop/laamaj/db/laamaj.db')

REC_PER_PAGE = 10
FETCH_RECORDS_SQL = u'select ws_user, ws_url from websites where \
ws_id between {0} and {1} order by ws_id desc'

FETCH_RECORDS_SQL_2 = u'select ws_id, ws_user, ws_url, ws_date, ws_localfile \
from websites where ws_id between {0} and {1} order by ws_id desc'

FETCH_SINGLE_RECORD = u'select ws_id, ws_user, ws_url, ws_date, ws_localfile \
from websites where ws_id = {0}'


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

def pad_page_results(results):
    ''' generate truncated name based on url and convert image name to bool. '''
    MAXNAME = 60
    output = []
    for key, user, url, date, local in results:
        name = url
        if len(url) > MAXNAME:
            name = url.split(u'/')[-1]
            if name == u'':
                ## trailing / leaves empty string at end of list
                name = url.split(u'/')[-2]
            name = u''+ url[0:MAXNAME-len(name)] + u"\u2026" + name
        ## if there's a local image, or the link is to youtube
        ## set local to true so we can host link
        local = bool(local)
        if not local:
            if match(u'^https?://(www.)?youtube.com.*', url):
                local = True
        record = [key, user, url, name, date, local]
        output.append(record)
    return output

@app.route(u'/page<int:pagenum>')
def pages(pagenum):
    ''' mark 2 or laamaj site '''
    head = int(_db.exe(u'select max(ws_id) from websites')[0][0])
    head = max(0, head - ((pagenum -1) * REC_PER_PAGE)) 
    tail = max(0, head - REC_PER_PAGE)
    results = _db.exe(FETCH_RECORDS_SQL_2.format(tail, head))
    results = pad_page_results(results)
    minpage = max(1, pagenum - 2)
    pagelist = range(minpage, minpage + 5)
    output = render_template(u'page.htm',
                page=pagenum, links=results, pages = pagelist)
    return output

@app.route(u'/hosted/<int:record>')
def hosted_content(record):
    head = int(_db.exe(u'select max(ws_id) from websites')[0][0])
    if record < 1 or record > head:
        return u'Get Tae Fuck', 404
    key, user, url, dat, local = _db.exe(FETCH_SINGLE_RECORD.format(record))[0]
    if local:
        output = u'image'
    else:
        if match(u'^https?://(www.)?youtube.com.*', url):
            ## Hack the url to embed and force https
            url = url.replace('watch?v=','embed/')
            url = url.replace('http:','https:')
            output = render_template(u'yatube.htm', record=record,
                        user=user, dat=dat, url=url)
        else:
            output = u'away', 404
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
