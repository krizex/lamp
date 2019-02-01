from lamp.app import app
from lamp.app.views.candidate import display_candidates_data
from lamp.app.views.grid import get_grids_data
from lamp.app.views.trend import get_trends_data
from lamp.db.helpers import cli
from lamp.log import log
from flask import render_template


@app.route('/')
@app.route('/wave/')
def index():
    # cli.update_candidates_from_file('data.json')
    # log.debug('Candidate refreshed')
    return display_candidates_data()


@app.route('/grid/')
def grid():
    # cli.update_grids_from_file('grid.json')
    # log.debug('Grid refreshed')
    grid_recs = get_grids_data()
    trend_recs = get_trends_data()
    return render_template('grids_data.html', grid_recs=grid_recs, trend_recs=trend_recs)
