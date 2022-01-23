from flask import Flask
from flask import render_template
from flask import request, flash
from flask import redirect, url_for
import model
messages = []

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
  messages = ["Test"]
  model.displayMessages(messages)
  return render_template("index.html", messages = messages)
  

@app.route("/keywords", methods=["GET", "POST"])
def change():
  if request.method == "POST":
      userdata = request.form
      print('userdata')
      return render_template("keywords.html")
  else:
      return "Sorry, there was an error."
  
@app.route("/post-story", methods = ["POST"])
def add_story():
  story = request.values.get("message")
  messages.append(story)
  model.displayMessages(messages)
  return render_template("index.html", messages = messages)
  

  
  
if __name__ == "__main__":
  app.run()