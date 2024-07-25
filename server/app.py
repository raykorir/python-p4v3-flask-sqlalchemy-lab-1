# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route("/")
def index():
    body = {"message": "Flask SQLAlchemy Lab 1"}
    return make_response(body, 200)


# Add views here
@app.route("/earthquakes/<int:id>")
def earthquake_by_id(id):
    quake = Earthquake.query.filter_by(id=id).first()
    if quake:
        body = quake.to_dict()
        status = 200
    else:
        body = {"message": f"Earthquake {id} not found."}
        status = 404
    return make_response(body, status)


@app.route("/earthquakes/magnitude/<float:magnitude>")
def search_min(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    quakes = []

    for e in earthquakes:
        quakes.append({
            "id": e.id,
            "location": e.location,
            "magnitude": float(e.magnitude),
            "year": e.year
        })

    body = {"count": len(quakes), "quakes": quakes}
    status = 200
    return make_response(body, status)


if __name__ == "__main__":
    app.run(port=5555, debug=True)