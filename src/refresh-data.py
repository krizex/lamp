#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lamp.db.helpers import cli

def main():
    cli.update_candidates_from_file('data.json')


if __name__ == '__main__':
    main()