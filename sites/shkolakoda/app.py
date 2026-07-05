from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/camps")
def camps():
    return render_template("camps.html")


@app.route("/safety")
def safety():
    return render_template("safety.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
