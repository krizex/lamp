from lamp.app import app
from lamp.app.views.candidate import display_candidates_data
from lamp.app.views.grid import display_grids_data
from lamp.db.helpers import cli
from lamp.log import log


@app.route('/')
@app.route('/wave/')
def index():
    cli.update_candidates_from_file('data.json')
    log.debug('Candidate refreshed')
    return display_candidates_data()


@app.route('/grid/')
def grid():
    cli.update_grids_from_file('grid.json')
    log.debug('Grid refreshed')
    return display_grids_data()
