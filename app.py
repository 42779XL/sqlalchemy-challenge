# Import dependency
import numpy as np
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify

# Setup database
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base=automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table
M = Base.classes.measurement
S = Base.classes.station
session = Session(engine)

# Flask Setup
app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<end>/<br/>"
    )

def prcps():
    session=Session(engine)
    last_date = session.query(M.date).order_by(M.date.desc()).first()
    current_date = session.query(M.date,M.prcp).filter(M.date>last_date).all()
    prcp_value=[]
    for date,prcp in current_date:
        dict_data={}
        dict_data['date']=date
        dict_data['prcp']=prcp
        prcp_value.append(dict_data)
    return jsonify(prcp_value)


if __name__ == "__main__":
    app.run(debug=True)


