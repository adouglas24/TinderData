from flask import Flask, render_template, request
import json 

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

def invalidInput():
     return render_template("home.html")

@app.route("/data", methods=["POST", "GET"])
def dataPage():
    sum = 0
    if request.method == "POST":
        if request.files:

            data = request.files["json"]
            if badFile(data):
                return ("Bad file bro")
            data = json.loads(data.stream.read())
            for i in data["Usage"]["app_opens"]:
                sum += int(data["Usage"]["app_opens"][i])
    return render_template("data.html")


def badFile(data):
    if data.filename == "" or not "." in data.filename:
        return true
    
    ext = data.filename.rsplit(".", 1)[1]
    return not ext == "json"     