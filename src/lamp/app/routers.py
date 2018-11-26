from lamp.app import app
from lamp.app.views.candidate import display_candidates_data
from lamp.app.views.grid import display_grids_data


@app.route('/')
@app.route('/wave/')
def index():
    return display_candidates_data()


@app.route('/grid/')
def grid():
    return display_grids_data()
