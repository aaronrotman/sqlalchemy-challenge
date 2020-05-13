# Dependencies  and set-up
import numpy as np
import pandas as pd
import datetime as dt
from flask import Flask, jsonify
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

# Database set-up
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Reflect the database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Instantiate Flask
app = Flask(__name__)

# Create the index route
@app.route('/')
def index():
    print('Server received request for index page')
    return (
    '''
    Welcome to the index page.
    The following routes are available:
    <br><br>
    STATIC ROUTES:
    <br>
    <a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a>
    <br>
    <a href="/api/v1.0/stations">/api/v1.0/stations</a>
    <br>
    <a href="/api/v1.0/tobs">/api/v1.0/tobs</a>
    <br><br>
    DYNAMIC ROUTES:
    <br>
    Start date:
    <br>
    <a href="/api/v1.0/<start_date>">/api/v1.0/start_date</a>
    <br>
    Example: <a href="/api/v1.0/2016-08-01">/api/v1.0/2016-08-01</a>
    <br><br>
    Start and end date:
    <br>
    <a href="/api/v1.0/<start_date>/<end_date>">/api/v1.0/start_date/end_date</a>
    <br>
     Example: <a href="/api/v1.0/2016-08-01/2017-08-01">/api/v1.0/2016-08-01/2017-08-01</a>
    ''')
# Create the precipitation route
@app.route('/api/v1.0/precipitation')
def precipitation():
    # Create session link to the database
    session = Session(engine)
    # Calculate the date one year before the last measurement date
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Select all date and prcp values within one year of the most recent date
    year_results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > year_ago).\
        order_by(Measurement.date).all()
    
    # Close the session
    session.close()
    
    # Create a dictionary from the query results
    precip_dict = {}
    for date, precip in year_results:
        precip_dict[date] = precip
       
    print('Server received request for precipitation page')
    return jsonify(precip_dict)

# Create the stations route
@app.route('/api/v1.0/stations')
def stations():
    # Create session link to the database
    session = Session(engine)

    # Query database
    station_results = session.query(Station.station).all()

    # Close the session
    session.close()

    # Convert the results from list of tuples to list
    all_stations = list(np.ravel(station_results))

    print('Server received request for stations page')
    return jsonify(all_stations)

# Create the temperature observations route
@app.route('/api/v1.0/tobs')
def tobs():
    # Create session link to the database
    session = Session(engine)
    # Calculate the date one year prior to the last temperature observation date
    one_year_ago = dt.date(2017, 8, 18) - dt.timedelta(days=365)

    # Query database
    tobs_results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station=='USC00519281').\
        filter(Measurement.date >= one_year_ago).\
        order_by(Measurement.date).all()

    # Close the session
    session.close()

    # Create a list of query results
    tobs_list = []
    
    for date, tobs in tobs_results:
        tobs_dict = {}
        tobs_dict[date] = tobs
        tobs_list.append(tobs_dict)


    print('Server received request for tobs page')
    return jsonify(tobs_list)
    
# Create the start date route
@app.route('/api/v1.0/<start_date>')
def calc_temps_start(start_date):
    # Create session link to the database
    session = Session(engine)
    
    # Query the database
    tobs_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    
    # Close the session
    session.close()
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    return jsonify(tobs_results)

# Create the start/end date route
@app.route('/api/v1.0/<start_date>/<end_date>')
def calc_temps(start_date, end_date):
    # Create session link to the database
    session = Session(engine)
    
    # Query the database
    tobs_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    # Close the session
    session.close()
 
    return jsonify(tobs_results)


if __name__ == "__main__":
    app.run(debug=True)
