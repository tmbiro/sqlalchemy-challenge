import pandas as pd

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
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"<h3>Available Routes:</h3><br/>"
        f"<b>Weather stations:</b> <br/>/api/v1.0/stations<br/>"
        f"<br/><b>Precipitation measurements for the last 12 months of data:</b> <br/>/api/v1.0/precipitation<br/>"
        f"<br/><b>Temperature measurements for the last 12 months of the data:</b> <br/>/api/v1.0/tobs<br/>"
        f"<br/><b>Temperature information for a specific date <br/>(add date to end using YYYY-MM-DD format):</b> <br/>/api/v1.0/<start><br/>"
        f"<br/><b>Temperature information for a date range <br/>(add start and end dates to end using YYYY-MM-DD format, with '/' in-between the dates):</b> <br/>/api/v1.0/<start>/<end><br/>"
        f"<br/><b>Note: The last date recorded in the dataset is 2017-08-23"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation measures from the latest year in the dataset"""

    # Perform a query to retrieve the data and precipitation scores
    last_year_data = (
        session
        .query(Measurement.date, Measurement.prcp) #query the measurement date and precipitation columns
        .filter(Measurement.date >= '2016-08-23') #only keep dates that are greater than or equal to '2016-08-23'
        .all()) #grab everything that matches the filter

    session.close()

    return jsonify(dict(last_year_data))

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    station_data = session.query(Station.station, Station.name).all()

    session.close()

    return jsonify(dict(station_data))

@app.route("/api/v1.0/tobs")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all temperature measures from the latest year in the dataset"""

    # Perform a query to retrieve the data and precipitation scores
    temp_data = (
        session
        .query(Measurement.date, Measurement.tobs) #query the measurement date and precipitation columns
        .filter(Measurement.date >= '2016-08-23') #only keep dates that are greater than or equal to '2016-08-23'
        .filter(Measurement.station == 'USC00519281') #only keep data from the most active station
        .all()) #grab everything that matches the filter

    session.close()

    return jsonify(dict(temp_data))

if __name__ == '__main__':
    app.run(debug=True)