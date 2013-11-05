#!/usr/bin/python
# vim: set fileencoding=utf-8 :
'''
Lamaaj web portal

Stand along web portal using the laamaj resources.
'''

import database
from flask import Flask, render_template, url_for, session

app = Flask(__name__)
app.secret_key = u'herpy derpy doo'

_db = database.Database()

@app.route(u'/')
def relay_bitg():
    ''' Forward users accessing the domain to the youtube video. '''
    return render_template(u'redirect.htm',
        target=u'http://www.youtube.com/watch?v=my2NVhUjekA')


@app.route(u'/tor')
@app.route(u'/bitg2')
@app.route(u'/atlas')
@app.route(u'/relay')
def relay_atlas_bitg2():
    ''' Redirect tor related queries to the atlas for BITG2. '''
    return render_template(u'redirect.htm',
        target=u'https://atlas.torproject.org/#details/50D921F0D34F5D4E74F86EDB90F3E9F10A89DC01')


@app.route(u'/test')
def test():
    ''' Test code accessed at <domain>/test. '''
    sites = _db.list_last_sites()
    output = u'The sites are:<br \>'
    for site in sites:
        output = output +  unicode(site[0]) + u',<br \>'  
    output = output + u'fin.'
    return output


@app.route(u'/test2')
def test2():
    ''' toying with db access '''
    results = _db.exe(u'select count(*) from websites')
    num_of_websites = u'There are these many websites store in laamaj : '
    for result in results:
        num_of_websites += str(result[0])
    results = _db.exe(
            u"select count(*) from websites where ws_localfile != ''")
    num_of_images = u'There are thes many images stored in laamaj : '
    for result in results:
        num_of_images += str(result[0])
    output = num_of_websites + u'<br />' + num_of_images
    return output

@app.route(u'/ttg')
def ttg():
    ''' Tugrek Toilet Goblins: list laamaj contents '''
    output = render_template(u'main.htm')
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
    #app.run(host='0.0.0.0', port=80)
    app.run(host='0.0.0.0', port=80, debug=True)
