#for web shit
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return """<meta HTTP-EQUIV="REFRESH" content="0; url=http://www.youtube.com/watch?v=my2NVhUjekA">"""

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
