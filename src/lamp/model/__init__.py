from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models here
from lamp.model.candidate import Candidate
from lamp.model.grid import Grid
