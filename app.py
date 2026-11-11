
from flask import Flask, render_template, request
from ev_charging import system

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/request", methods=["GET", "POST"])
def charging_request():

    if request.method == "POST":

        owner = request.form.get("owner")
        vehicle = request.form.get("vehicle")
        battery = request.form.get("battery")
        station = request.form.get("station")

        system.request_ev()

        return render_template(
            "request.html",
            success=True,
            owner=owner,
            vehicle=vehicle,
            battery=battery,
            station=station
        )

    return render_template("request.html")


@app.route("/stations")
def stations():
    data = system.get_snapshot()
    return render_template("stations.html", data=data)


@app.route("/sessions")
def sessions():
    data = system.get_snapshot()

    return render_template(
        "sessions.html",
        data=data
    )


@app.route("/admin")
def admin():
    data = system.get_snapshot()
    return render_template("admin.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
