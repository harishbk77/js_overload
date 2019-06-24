# FLASK_APP=dash_app/app.py flask run
import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

import sqlite3
import re

app = Flask(__name__)

#################################################
# Database Setup SQLAlchemy
#################################################

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/js_overload.sqlite"
# db = SQLAlchemy(app)

# # reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(db.engine, reflect=True)

# Survey = Base.classes.jso11k
#################################################


############# sqlite3 ##########################
@app.route("/")
def index():

    """Return the homepage."""
    return render_template("index.html")


@app.route("/columns")
def names():
    """Return a list of columns from 11000 rows from the original dataset."""

    conn = sqlite3.connect("dash_app/db/js_overload.sqlite")
    cur = conn.cursor()
    cols = '''SELECT sql FROM sqlite_master
    WHERE tbl_name = `jso11k` AND type = `table`'''

    cur.execute(cols)
    rows = cur.fetchall()
    col_string = rows[0][1]
    pattern = r'`([A-Za-z0-9]*)`'
    column_names = re.findall(pattern, col_string)[:-1]
    return jsonify(column_names)

    # column names using sqlalchemy:

    # Use Pandas to perform the sql query
    # stmt = db.session.query(Survey).statement
    # df = pd.read_sql_query(stmt, db.session.bind)

    # # Return a list of the column names 
    # return jsonify(list(df.columns))


@app.route("/countries")
def countries():
    """
     Return a list of number of survey respondents by country
    """
    conn = sqlite3.connect("dash_app/db/js_overload.sqlite")
    cur = conn.cursor()

    query_string = '''
        SELECT Country, count(country) FROM jso11k
        GROUP BY Country
        ORDER BY COUNT(Country) DESC
    '''

    cur.execute(query_string)
    rows = cur.fetchall()

    country_data = []

    for row in rows:
        tempDict = {}
        tempDict[row[0]] = int(row[1])
        country_data.append(tempDict)


    return jsonify(country_data)

if __name__ == "__main__":
    app.run()
