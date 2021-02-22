from flask import Flask, render_template, redirect, request
from scrapper import start_scrapper

app = Flask(__name__)

db = {}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/report")
def report():
    word = request.args.get("word")
    if word:
        word = word.lower()
        extract_db = db.get(word)
        if extract_db:
            jobs = extract_db
        else:
            jobs = start_scrapper()
            db[word] = jobs
    else:
        return redirect("/")
    return render_template("report.html", jobs = jobs, result_number = len(jobs), word = word)




if __name__=="__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)