from lamp.app import app
from lamp.app.views.candidate import display_candidates_data
from lamp.app.views.grid import get_grids_data
from lamp.app.views.trend import get_trends_data
from lamp.app.views.rebound import get_rebounds_data
from lamp.db.helpers import cli
from lamp.log import log
from flask import render_template
from multiprocessing.pool import ThreadPool
from lamp.app.controllers.trend_candidate import get_trend_candidate




@app.route('/')
@app.route('/wave/')
def wave():
    def apply_f(f, name):
        with app.app_context():
            recs = f()
            return name, recs

    funcs = {
        'grid_recs': get_grids_data,
        'trend_recs': get_trends_data,
        'rebound_recs': get_rebounds_data,
    }
    pool = ThreadPool(processes=len(funcs))
    async_results = [pool.apply_async(apply_f, (f, name)) for name, f in funcs.items()]
    recs_map = {name: result for name, result in [ret.get() for ret in async_results]}

    timestamp, duration, recs = get_trend_candidate()

    return render_template('wave_page.j2', **recs_map, timestamp=timestamp, duration=duration, trend_candidate_recs=recs)


@app.route('/grid/')
def grid():
    grid_recs = get_grids_data()
    return render_template('grid_page.j2', grid_recs=grid_recs)


@app.route('/trend/')
def trend():
    trend_recs = get_trends_data()
    return render_template('trend_page.j2', trend_recs=trend_recs)


@app.route('/rebound/')
def rebound():
    rebound_recs = get_rebounds_data()
    return render_template('rebound_page.j2', rebound_recs=rebound_recs)



@app.route('/trend_candidate/')
def trend_candidate():
    timestamp, duration, recs = get_trend_candidate()
    return render_template('trend_candidate_page.j2', trend_candidate_recs=recs, timestamp=timestamp, duration=duration)
