import pandas as pd
import datetime as dt

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
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

#List all the available routes
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

#Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value. Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation measures from the latest year in the dataset"""

    # Perform a query to retrieve the data and precipitation scores
    last_year_data = (
        session
        .query(measurement.date, measurement.prcp) #query the measurement date and precipitation columns
        .filter(measurement.date >= '2016-08-23') #only keep dates that are greater than or equal to '2016-08-23'
        .all()) #grab everything that matches the filter

    session.close()

    # Return JSON representation as dictionary.
    return jsonify(dict(last_year_data))

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    station_data = session.query(station.station, station.name).all() #Grab stations and their names

    session.close()

    #Return a JSON list
    return jsonify(dict(station_data))

#Query the dates and temperature observations of the most-active station for the previous year of data. Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def temperature():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all temperature measures from the latest year in the dataset"""

    # Perform a query to retrieve the data and temperature scores
    temp_data = (
        session
        .query(measurement.date, measurement.tobs) #query the measurement date and temperature columns
        .filter(measurement.date >= '2016-08-23') #only keep dates that are greater than or equal to '2016-08-23'
        .filter(measurement.station == 'USC00519281') #only keep data from the most active station
        .all()) #grab everything that matches the filter

    session.close()

    #Return a JSON list
    return jsonify(dict(temp_data))

@app.route("/api/v1.0/<start>")
def date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Change the date in string format to datatime.date
    start = dt.datetime.strptime(start, '%Y-%m-%d').date()

    # Perform a query to retrieve the data and temperature scores
    temp_data = (
        session
        .query(
            func.min(measurement.tobs), #Obtain the lowest of temperature
            func.max(measurement.tobs), #Obtain the highest of temperature
            func.avg(measurement.tobs) #Obtain the average temperature
            )
        .filter(measurement.date >= start) #Filter based on date
        .all() #Show all
    )
    
    (min, max, mean) = temp_data[0] #Separate tuple into variables

    session.close()

    #Reture a JSON list
    return jsonify(f"Start date: {start}",f"Temperature (degrees Fahrenheit) High: {round(min,1)}, Low: {round(max,1)}, Average: {round(mean,1)}")

@app.route("/api/v1.0/<start>/<end>")
def dates(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Change the date in string format to datatime.date
    start = dt.datetime.strptime(start, '%Y-%m-%d').date()
    end = dt.datetime.strptime(end, '%Y-%m-%d').date()

    # Perform a query to retrieve the data and temperature scores
    temp_data = (
        session
        .query(
            func.min(measurement.tobs), #Obtain the lowest of temperature
            func.max(measurement.tobs), #Obtain the highest of temperature
            func.avg(measurement.tobs) #Obtain the average temperature
            )
        .filter(measurement.date >= start) #Filter based on start date
        .filter(measurement.date <= end) #Filter based on end date
        .all() #Show all
    )
    
    (min, max, mean) = temp_data[0] #Turn tuple into variables

    session.close()

    #Return a JSON list
    return jsonify(f"Start date: {start}, End date: {end}",f"Temperature (degrees Fahrenheit) High: {round(min,1)}, Low: {round(max,1)}, Average: {round(mean,1)}")

if __name__ == '__main__':
    app.run(debug=True)