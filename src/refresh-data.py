#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lamp.app import app
from lamp.db.helpers import cli

def main():
    with app.app_context():
        cli.update_candidates_from_file('data.json')
        cli.update_grids_from_file('grid.json')


if __name__ == '__main__':
    main()
