import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect = True)

station = Base.classes.station
measurement = Base.classes.measurement

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Routes that are available:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"- Last 12 months of precipitation <br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"- The list of the stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"- Temperature observations of the most active station in the last 12 years<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f"- For given start date and end date (YYYY-MM-DD),the MIN/AVG/MAX temperature for all dates greater than and equal to the start date<br/>"
        f"<br/>"
        f"/api/v1.0/start/end<br/>"
        f"- For given start and and end date (YYYY-MM-DD),the MIN/AVG/MAX temperature for dates between the start and end date inclusive<br/>"
        )
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    rain = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date > last_year).\
        order_by(measurement.date).all()
        

    rain_results = []
    for result in rain:
        row = {}
        row["date"] = rain[0]
        row["prcp"] = rain[1]
        rain_results.append(row)

    return jsonify(rain_results)

@app.route("/api/v1.0/stations")
def stations():
    stations_query = session.query(station.name, station.station)
    stations = pd.read_sql(stations_query.statement, stations_query.session.bind)
    return jsonify(stations.to_dict())

@app.route("/api/v1.0/tobs")
def tobs():
    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temperature = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date > last_year).\
        order_by(measurement.date).all()
        
    temperature_results = []
    for result in temperature:
        row = {}
        row["date"] = temperature[0]
        row["tobs"] = temperature[1]
        temperature_results.append(row)

    return jsonify(temperature_results)

@app.route("/api/v1.0/<start>")
def trip1(start):   
    start_date= dt.datetime.strptime(start, "%Y-%m-%d")
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end =  dt.date(2017, 8, 23)
    trip_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)

@app.route("/api/v1.0/<start>/<end>")
def trip2(start,end):

  
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end = end_date-last_year
    trip_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)

if __name__ == "__main__":
    app.run(debug=True)
    
    
        
        
        
    
