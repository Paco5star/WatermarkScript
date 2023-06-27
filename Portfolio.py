from flask import Flask , render_template
import flask_bootstrap

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("portfolio.html")

if __name__ == "__main__":
    app.run(debug=True)