# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start]<br/>"
        f"/api/v1.0/[start]/[end]<br/><br/>"
        f"Please enter date in yyyy-mm-dd format for the [start] and [end] routes"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return precipitation data of last year"""
    recent_date = dt.date(2017,8,23)
    last_year = recent_date - dt.timedelta(days=365)
    # Query all precipitation data
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of all_prcp
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all station names"""
    # Query all stations
    results = session.query(Measurement.station).distinct(Measurement.station).order_by(Measurement.date).all()
    
    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return data for most active station"""
    # Query all tobs data
    results = session.query(Measurement.date, Measurement.tobs, Measurement.prcp).filter(Measurement.date >= '2016-08-23').filter(Measurement.station == 'USC00519281').order_by(Measurement.date).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of all_tobs
    all_tobs = []
    for date, tobs, prcp in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_dict["prcp"] = prcp
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    """Return start date to end date of dataset data"""
    # Query data from start date to the end date of the dataset
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of all_start
    all_start = []
    for min, max, avg in results:
        start_dict = {}
        start_dict["min"] = min
        start_dict["max"] = max
        start_dict["avg"] = avg
        all_start.append(start_dict)

    return jsonify(start_dict)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    """Return start date to end date data"""
    # Query data from start date to the end date
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of all_start_end
    all_start_end = []
    for min, max, avg in results:
        start_end_dict = {}
        start_end_dict["min"] = min
        start_end_dict["max"] = max
        start_end_dict["avg"] = avg
        all_start_end.append(start_end_dict)

    return jsonify(start_end_dict)

if __name__ == '__main__':
    app.run(debug=True)