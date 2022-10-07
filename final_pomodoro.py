import functions as fun
import os
import argparse
import atexit
from create_activity import create_activity as ca
from delete_activity import delete_activity as da
from create_activity import return_activities as ra
from update_data import update_data as ud

from settings import *


def exit_handler():
    print ('\x1b[?25h')


def final_app(*args):

    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--run', help='Run pomodoro session', action='store_true')
    parser.add_argument("-s", dest="session", help="Run custom pomodoro session", nargs=3, metavar=('MW','MR','SESSIONS'), type=int)
    parser.add_argument("-t", "--today", help="Get tomatos for today", dest="today", action='store_true')
    parser.add_argument("-y", "--yesterday", help="Get tomatos for yesterday", dest="yesterday", action='store_true' )
    parser.add_argument("-v", "--defaults", help="Open default variables", dest="defaults", action='store_true')
    parser.add_argument('-n', "--new", help="Add activity", nargs=2, metavar=('STATUS','TIME'))
    parser.add_argument('-l', '--list', help='Return activities', action='store_true')
    parser.add_argument('-d', '--delete', help="Delete activity", nargs=1)
    parser.add_argument('-u', dest='update', help='Update data', nargs=3, metavar=('KEY','VALUE','NAME'))

    args=parser.parse_args()
    if args.session:
        fun.daysession(fun.pomodoro_plus(args.session[0],args.session[1],args.session[2]))
    elif args.today:
        fun.today_tomatos()
    elif args.yesterday:
        fun.yesterday_tomatos()
    elif args.defaults:
            os.system('$EDITOR '+dir_path+'/settings.py')
    if args.new:
        ca(input(), args.new[0], args.new[1])
    elif args.list:
        ra()
    if args.delete:
        da(args.delete[0])
    if args.update:
        ud(args.update[0], args.update[1], args.update[2])
    if args.run:
        fun.daysession(fun.pomodoro_plus(DEFAULT_WORK_TIME, DEFAULT_RELAX_TIME, DEFAULT_SESSIONS))

final_app()

atexit.register(exit_handler)
