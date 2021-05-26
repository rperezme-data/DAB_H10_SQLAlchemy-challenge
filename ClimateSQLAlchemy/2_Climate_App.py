## DEPENDENCIES
## Numpy
import numpy as np
## Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
## Flask
from flask import Flask, jsonify

## DATABASE SETUP
## Create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
## Reflect an existing database into a new model
Base = automap_base()
## Reflect the tables
Base.prepare(engine, reflect=True)
## Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
## Create session (link) from Python to the DB
session = Session(engine)

## FLASK SETUP
app = Flask(__name__)

## FLASK ROUTES
## Homepage
@app.route("/")
def home():
    """Homepage"""
    return (
        f"Welcome to the Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

## Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    """- Query hawaii.sqlite database
        - Convert query results to dictionary {date(key) : prcp(value)}
        - Return the JSON representation of dictionary"""

    ## Prompt to terminal
    print("Server received request for 'precipitation' page...")

    ## Open session, store query results & close terminal
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    ## Convert query results to dictionary {date(key) : prcp(value)}
    prcp_response = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_response.append(prcp_dict)

    ## Return JSON representation of dictionary
    return jsonify(prcp_response)


## Stations
@app.route("/api/v1.0/stations")
def stations():
    """- Return a JSON list of stations from the dataset"""

    ## Prompt to terminal
    print("Server received request for 'stations' page...")

    ## Open session, store query results & close terminal
    session = Session(engine)
    results = session.query(Station.name).all()
    session.close()

    ## Convert query results to list
    stations_response = list(np.ravel(results))
    
    ## Return JSON representation of list
    return jsonify(stations_response)


## RUN FLASK APP
if __name__ == "__main__":
    app.run(debug=True)

    