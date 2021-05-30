## DEPENDENCIES
## Numpy
import numpy as np
## Datetime & Relative Delta
import datetime as dt
from dateutil.relativedelta import relativedelta
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
        f"Welcome to the Climate App!<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2010-01-01<br/>"
        f"/api/v1.0/2010-01-01/2017-08-18<br/>"
    )

## Precipitation route
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


## Stations route
@app.route("/api/v1.0/stations")
def stations():
    """- Return a JSON list of stations from the dataset"""

    ## Prompt to terminal
    print("Server received request for 'stations' page...")

    ## Open session, store query results & close terminal
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    ## Convert query results to list
    stations_response = list(np.ravel(results))
    
    ## Return JSON representation of list
    return jsonify(stations_response)


## TOBS route
@app.route("/api/v1.0/tobs")
def tobs():
    """- Query dates and TOBS of the most active station for the last year of data
        - Return JSON list of temperature observations (TOBS) for the previous year"""
    
    ## Prompt to terminal
    print("Server received request for 'tobs' page...")

    ## Open session, store query results & close terminal
    session = Session(engine)

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(last_date[0], "%Y-%m-%d").date()
    minus_one_year = last_date - relativedelta(years=1)

    most_active = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()
    most_active = most_active[0]

    slct = [Measurement.date, Measurement.tobs]

    results = session.query(*slct).\
        filter(Measurement.date >= func.strftime(minus_one_year)).\
        filter(Measurement.station == most_active).\
        order_by(Measurement.date).all()

    session.close()

    ## Convert query results to dictionary
    tobs_response = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_response.append(tobs_dict)
    
    ## Return JSON representation of dictionary
    return jsonify(tobs_response)


## Start route
@app.route("/api/v1.0/<start_date>")
def start(start_date):
    """- Return JSON list of the min, avg & max temp for a given start date
        - Range: All dates greater than and equal to the start date"""
    
    ## Prompt to terminal
    print("Server received request for 'start' page...")

    ## Open session, store query results & close terminal
    session = Session(engine)

    slct = [func.min(Measurement.tobs),
          func.avg(Measurement.tobs),
          func.max(Measurement.tobs)]

    results = session.query(*slct).\
        filter(Measurement.date >= start_date).\
        order_by(Measurement.date).all()

    session.close()

    ## Convert query results to list
    start_response = list(np.ravel(results))
       
    ## Return JSON representation of list
    return jsonify(start_response)


## Start/End route
@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
    """- Return JSON list of the min, avg & max temp for a given start/end range
        - Range: Dates between the start and end date inclusive"""
    
    ## Prompt to terminal
    print("Server received request for 'start/end' page...")

    ## Open session, store query results & close terminal
    session = Session(engine)

    slct = [func.min(Measurement.tobs),
          func.avg(Measurement.tobs),
          func.max(Measurement.tobs)]

    results = session.query(*slct).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).\
        order_by(Measurement.date).all()

    session.close()

    ## Convert query results to list
    start_end_response = list(np.ravel(results))
       
    ## Return JSON representation of list
    return jsonify(start_end_response)


## RUN FLASK APP
if __name__ == "__main__":
    app.run(debug=True)

    