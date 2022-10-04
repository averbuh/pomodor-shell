import functions as fun
import os
import argparse
import atexit

from settings import *


def exit_handler():
    print ('\x1b[?25h')


def final_app():

    parser = argparse.ArgumentParser()
    parser.add_argument(
            "-s",
            dest="session",
            help="Run pomodoro session", 
            nargs=3,
            metavar=('MW','MR','SESSIONS'),
            type=int
            )
    parser.add_argument(
            "-t",
            "--today",
            help="Get tomatos for today",
            dest="today",
            action='store_true'
            )
    parser.add_argument(
            "-y",
            "--yesterday",
            help="Get tomatos for yesterday",
            dest="yesterday",
            action='store_true'
            )
    parser.add_argument(
            "-d",
            "--defaults",
            help="Open default variables",
            dest="defaults",
            action='store_true'
            )
    parser.add_argument(
            "-a",
            "--activities",
            help="Open activities",
            action='store_true'
            )
    parser.add_argument(
            "-r",
            help="",
            dest='read',
            action='store_true'
            )
    parser.add_argument(
            "-w",
            help="",
            dest='write',
            action='store_true'
            )
    args=parser.parse_args()
    if args.session:
        fun.daysession(fun.pomodoro_plus(args.session[0],args.session[1],args.session[2]))
    elif args.today:
        fun.today_tomatos()
    elif args.yesterday:
        fun.yesterday_tomatos()
    elif args.defaults:
        if args.write:
            os.system('$EDITOR ~/database/scripts/python/tomato_app/settings.py')
        else:
            os.system('cat ~/database/scripts/python/tomato_app/settings.py')
    elif args.activities:
        if args.write:
            os.system('$EDITOR ~/database/scripts/python/tomato_app/activities.txt')
        else:
            os.system('cat ~/database/scripts/python/tomato_app/activities.txt')
    else: 
        fun.daysession(fun.pomodoro_plus(DEFAULT_WORK_TIME, DEFAULT_RELAX_TIME, DEFAULT_SESSIONS))
 
    



final_app()

atexit.register(exit_handler)
