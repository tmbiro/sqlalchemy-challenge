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
        f"<b>Weather stations:</b> /api/v1.0/stations<br/>"
        f"<b>Precipitation measurements:</b> /api/v1.0/precipitation<br/>"
        f"<b>Temperature measurements:</b> /api/v1.0/tobs<br/>"
        f"<b>Temperature information for a specific date (replace YYYY-MM-DD with desired date):</b> /api/v1.0/YYYY-MM-DD<br/>"
        f"<b>Temperature information for a date range (replace YYYY-MM-DD with start and end dates, respectively):</b> /api/v1.0/YYYY-MM-DD/YYYY-MM-DD"
    )

@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation measures from the latest year in the dataset"""
    
    # Find the most recent date in the dataset
    recent_date = (
    session #take the session we've opened
    .query(Measurement) #Look in the Measurement dataset
    .order_by(Measurement
              .date #Order by date
              .desc()) #In decending order
    .first() #Pull the first row
    .date) #Take the value in the "date" column
    
    # Design a query to retrieve the last 12 months of precipitation data and plot the results. 
    last_date = ((
        dt #Using datetime module
        .datetime #retrieve datetime object

    # Starting from the most recent data point in the database. 
        .strptime(recent_date, '%Y-%m-%d') #grab the recent date as a string in '%Y-%m-%d'format

    # Calculate the last date one year from the most recent date in data set.
        - #subtract
        dt
        .timedelta(days=365)) #365 days from it
        .strftime('%Y-%m-%d')) #put the result in '%Y-%m-%d' format

    last_date

    # Perform a query to retrieve the data and precipitation scores
    last_year_data = (
        session
        .query(Measurement.date, Measurement.prcp) #query the measurement date and precipitation columns
        .filter(Measurement.date >= last_date) #only keep dates that are greater than or equal to last_date
        .all()) #grab everything that matches the filter

    session.close()

    return jsonify(dict(last_year_data))

if __name__ == '__main__':
    app.run(debug=True)