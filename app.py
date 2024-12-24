from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

from ice_breaker import ice_break_with


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    name = request.form["name"]
    summary, profile_pic_url = ice_break_with(
        name=name
    )
    print('name', name)
    print('summary', summary)
    print('profile_pic_url', profile_pic_url)
    return jsonify(
        {
            "summary_and_facts": summary.to_dict(),
            #"picture_url": profile_pic_url,
            "picture_url" : 'static/banner.jpeg' 
        }
    )


if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)