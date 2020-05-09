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
    return '''
    Welcome to the index page. \n
    The following routes are available:
    <br>
    <a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a>
    <br>
    <a href="/api/v1.0/stations">/api/v1.0/stations</a>
    <br>
    <a href="/api/v1.0/tobs">/api/v1.0/tobs</a>
    <br>
    '''
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

    year_data = []
    for date, precip in year_results:
        precip_dict = {}
        precip_dict[date] = precip
        # precip_dict['Date'] = date
        # precip_dict['Precipitation'] = precip
        year_data.append(precip_dict)
        
    print('Server received request for precipitation page')
    return jsonify(year_data)
    

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
    print('Server received request for tobs page')
    return '''
    <a href="../../">Home</a>
    '''

# # Create the start date route
# @app.route('/api/v1.0/<start>')
# def start_date():
#     print('Server received request for start_date page')
#     return '''
#     <a href="../../"><Home</a>
#     '''





if __name__ == "__main__":
    app.run(debug=True)
