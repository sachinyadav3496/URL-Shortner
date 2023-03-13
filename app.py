from flask import Flask
from flask import request
from flask import jsonify
from secrets import token_hex
from flask import redirect
import sqlite3 as sql 
from flask import url_for
from flask import render_template



app = Flask(__name__)


def create_short_url(url):
    while True:
        try:
            token = token_hex(5)
            con = sql.connect("urls.db")
            cursor = con.cursor()
            cursor.execute("INSERT INTO url_data VALUES (?, ?)", (token, url))
        except Exception:
            print("!!!trying again!!!")
        else:
            con.commit()
            cursor.close()
            con.close()
            break
    return f"{request.url_root}{token}"
            
def get_shorten_url(url):
    con = sql.connect("urls.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM url_data WHERE url=?", (url,))
    row = cursor.fetchone()
    cursor.close()
    con.close()
    if row:
        short_url = row[0]
    else:
        short_url = create_short_url(url)
    return short_url
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/shorten", methods=["POST"])
def shorten_url():
    url = request.form.get("link")
    print("Shorten URL: ", url)
    new_url = get_shorten_url(url)
    return jsonify({"url": new_url})

@app.route("/<key>", methods=["GET"])
def get_data(key):
    con = sql.connect("urls.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM url_data WHERE short_url=?", (key, ))
    row = cursor.fetchone()
    if row:
        return redirect(row[1])
    else:
        return redirect("http://localhost:5000/not_found")

@app.route("/not_found")
def not_found():
    return "<h1>Invalid URL Given</h1>"


if __name__ == "__main__":
    app.run()
        