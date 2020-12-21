from flask import Flask, render_template, request
import json 
import plotly.graph_objects as go

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

def invalidInput():
     return render_template("home.html")

@app.route("/data", methods=["POST", "GET"])
def dataPage():
    opens = 0
    likes = 0
    dislikes = 0
    matches = 0
    if request.method == "POST":
        if request.files:

            data = request.files["json"]
            if badFile(data):
                return ("Bad file bro")
            data = json.loads(data.stream.read())
            for i in data["Usage"]["app_opens"]:
                opens += int(data["Usage"]["app_opens"][i])
            for i in data["Usage"]["swipes_likes"]:
                likes += int(data["Usage"]["swipes_likes"][i])
            for i in data["Usage"]["swipes_passes"]:
                dislikes += int(data["Usage"]["swipes_passes"][i])
            for i in data["Usage"]["matches"]:
                matches += int(data["Usage"]["matches"][i])
    sankey(likes, dislikes, matches)
    return ""


def badFile(data):
    if data.filename == "" or not "." in data.filename:
        return true
    
    ext = data.filename.rsplit(".", 1)[1]
    return not ext == "json"     


def sankey(likes, dislikes, matches):
    fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 5,
      line = dict(color = "black", width = 0.5),
      label = ["Profiles seen", "Likes", "Passes", "Matches", ":("],
      color = "black"
    ),
    link = dict(
      source = [0, 0, 1, 1], # indices correspond to labels, eg A1, A2, A1, B1, ...
      target = [1, 2, 3, 4],
      value = [int(likes), int(dislikes), int(matches), int(likes-matches)],
      color = ['#FD297D', '#004777', '#FF5864', '#08B2E3']
      ))])
    

    fig.update_layout(hovermode = 'x',
        title_text="Your Tinder History", 
        font_size=12,
        font_color = 'white',
        paper_bgcolor = '#FCF7F8')
    
    fig.show()
