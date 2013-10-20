#!/usr/bin/python
# vim: set fileencoding=utf-8 :
"""
Lamaaj web portal

Stand along web portal using the laamaj resources.
"""

import database
from flask import Flask, render_template, url_for

app = Flask(__name__)

_db = database.Database()

@app.route("/")
def relay_bitg():
    """ Forward users accessing the domain to the youtube video. """
    return render_template("redirect.htm",
        target="http://www.youtube.com/watch?v=my2NVhUjekA")


@app.route("/tor")
@app.route("/bitg2")
@app.route("/atlas")
@app.route("/relay")
def relay_atlas_bitg2():
    """ Redirect tor related queries to the atlas for BITG2. """
    return render_template("redirect.htm",
        target="https://atlas.torproject.org/#details/50D921F0D34F5D4E74F86EDB90F3E9F10A89DC01")


@app.route("/test")
def test():
    """ Test code accessed at <domain>/test. """
    sites = _db.list_last_sites()
    output = "The sites are:<br \>"
    for site in sites:
        output = output +  str(site[0]) + ',<br \>'  
    output = output + 'fin.'
    return output


@app.route("/test2")
def test2():
    results = _db.exe('select count(*) from websites;')
    num_of_websites = "There are these many websites store in laamaj : "
    for result in results:
        num_of_websites += str(result[0])
    results = _db.exe("select count(*) from websites where ws_localfile != '';")
    num_of_images = 'There are thes many images stored in laamaj : '
    for result in results:
        num_of_images += str(result[0])
    output = num_of_websites + '<br />' + num_of_images
    return output


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
    #app.run(host='0.0.0.0', port=80, debug=True)
