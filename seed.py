import pandas as pd
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import Column, Integer, String, Numeric, Text, Float, Date
import os
import json


# initialize database
db_uri = os.getenv("DATABASE_URI", "sqlite:///budgetapp.sqlite")
