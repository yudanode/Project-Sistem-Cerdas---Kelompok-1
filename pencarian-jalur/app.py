
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def beranda():
    return render_template("beranda.html")


@app.route("/data-sekolah")
def data_sekolah():
    return render_template("data_sekolah.html")


if __name__ == "__main__":
    app.run(debug=True)
