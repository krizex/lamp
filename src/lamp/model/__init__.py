from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models here
from lamp.model.candidate import Candidate
from lamp.model.grid import Grid
from lamp.model.trend import Trend
from lamp.model.rebound import Rebound

ALL_TABLES = {
    'candidate': Candidate,
    'grid': Grid,
    'trend': Trend,
    'rebound': Rebound
}
