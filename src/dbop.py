#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
import os
from lamp.app import app
from lamp.db.helpers import cli
from lamp.model import ALL_TABLES
from lamp import config
import json

def confirm(cfm_str):
    """
    Ask user to enter Y or N (case-insensitive).
    :return: True if the answer is Y.
    :rtype: bool
    """
    answer = ""
    while answer not in ["y", "n"]:
        answer = raw_input(cfm_str + ' [Y/N]').lower()
    return answer == "y"

def refresh_data(args):
    if not confirm('OK refresh data?'):
        print 'Canceled'
        exit(0)

    with app.app_context():
        data_folder = config.data_node
        for tbl in ALL_TABLES.iterkeys():
            tbl_cls = cli.tbl_name2cls(tbl)
            cli.update_from_file(os.path.join(data_folder, tbl+'.json'), tbl_cls)


def init_db(args):
    if not confirm('OK to reset the database?'):
        print 'Canceled'
        exit(0)

    from lamp.app import db
    with app.app_context():
        db.drop_all()
        db.create_all()


def dump_table(args):
    with app.app_context():
        dmp = cli.dump_table(args.tbl)
        print json.dumps(dmp, indent=4)

def dump_all(args):
    outd = args.outfolder
    if not os.path.exists(outd):
        os.makedirs(outd)

    with app.app_context():
        for tbl in ALL_TABLES.iterkeys():
            dmp = cli.dump_table(tbl)
            outf = os.path.join(outd, tbl + '.json')
            print 'dumping %s' % outf
            with open(outf, 'w') as f:
                json.dump(dmp, f, indent=4)


def build_parser():
    parser = argparse.ArgumentParser(description='Database ops')
    subparsers = parser.add_subparsers()
    refresh_parser = subparsers.add_parser('refresh', help='refresh data')
    refresh_parser.set_defaults(cmd=refresh_data)


    initdb_parser = subparsers.add_parser('init', help='init database')
    initdb_parser.set_defaults(cmd=init_db)

    dump_parser = subparsers.add_parser('dump', help='dump database')
    dump_parser.set_defaults(cmd=dump_table)
    dump_parser.add_argument('tbl', help='table name')

    dump_parser = subparsers.add_parser('dumpall', help='dump database')
    dump_parser.set_defaults(cmd=dump_all)
    dump_parser.add_argument('outfolder', nargs='?', help='table name', default='dbdumps')

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args(sys.argv[1:])
    args.cmd(args)


if __name__ == '__main__':
    main()
