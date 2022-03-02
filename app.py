import numpy as np
import re
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.sql import exists  

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes

# Home Route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitations<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )
# Precipitation route    
@app.route("/api/v1.0/precipitations")
def precipitation():
    """Query for the dates and temperature observations from the last year.
       Convert the query results to a Dictionary using date as the key and tobs as the value.
       Return the JSON representation of your dictionary."""
    
    # Calculate the date 1 year ago from today (today being 2017-08-23)
    today = dt.date(2017, 8, 23)
    year_ago = today - dt.timedelta(days=365)

    # Perform a query to retrieve the date and precipitation scores
    results = session.query(Measurement.prcp, Measurement.date)\
                                        .filter(Measurement.date >= year_ago)\
                                        .filter(Measurement.date < today).all()

    # Creating a dictionary from the row data and appending it to a all_precipitation
    all_precipitation = []
    for precipitation in results:
        precipitation_dict = {}
        precipitation_dict[precipitation.date] = precipitation.prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)