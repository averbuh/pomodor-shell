import functions as fun
import os
import argparse
import atexit
from create_activity import create_activity as ca
from delete_activity import delete_activity as da
from create_activity import return_activities as ra

from settings import *


def exit_handler():
    print ('\x1b[?25h')


def final_app(*args):
    
    parser = argparse.ArgumentParser(description='MyApp')
    parser.add_argument(
            'list',
            help='Return activities',
            required=False
            )
    parser.add_argument('start',help='Start session',required=False)
    args = parser.parse_args() 
    if args.list:
        ra()
    elif args.start:
        fun.daysession(fun.pomodoro_plus(DEFAULT_WORK_TIME, DEFAULT_RELAX_TIME, DEFAULT_SESSIONS))
    else:
        fun.daysession(fun.pomodoro_plus(DEFAULT_WORK_TIME, DEFAULT_RELAX_TIME, DEFAULT_SESSIONS))


final_app()

atexit.register(exit_handler)
