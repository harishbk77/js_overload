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

app = Flask(__name__)

#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/js_overload.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

Survey = Base.classes.jso


# Save references to each table
# @TODO create variables to hold the table ashshnames

@app.route("/")
def index():

    """Return the homepage."""
    return render_template("index.html")


@app.route("/columns")
def names():
    """Return a list of columns from 300 rows from the original dataset."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(Survey).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (sample names)
    return jsonify(list(df.columns))


if __name__ == "__main__":
    app.run()
