#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lamp.app import app
from lamp.db.helpers import cli

def confirm():
    """
    Ask user to enter Y or N (case-insensitive).
    :return: True if the answer is Y.
    :rtype: bool
    """
    answer = ""
    while answer not in ["y", "n"]:
        answer = raw_input("OK refresh data [Y/N]? ").lower()
    return answer == "y"

def main():
    if not confirm():
        print 'Canceled'
        return

    with app.app_context():
        cli.update_candidates_from_file('data.json')
        cli.update_grids_from_file('grid.json')


if __name__ == '__main__':
    main()
