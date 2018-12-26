from flask import Flask, jsonify, request, render_template
import generator
app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/privacy")
def privacy_page():
    return render_template("privacy.html")


@app.route("/get-tweet")
def build_tweet():
    subject_string_param = request.args.get("subject", default="", type=str)
    tweet = generator.build_tweet(subject_string_param)
    return jsonify(tweet)
