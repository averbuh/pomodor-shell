import functions as fun
import os
import argparse
import atexit


from create_activity import create_activity as ca
from delete_activity import delete_activity as da
from delete_activity import delete_completed_activity as dca
from create_activity import return_activities as ra
from create_activity import print_completed_activities as pca
from create_activity import copy_activity_from_complete as cafc 
from update_data import update_data as ud
from update_data import update_status as us
from update_data import update_name as un
from update_data import update_time as ut
from settings import *


def exit_handler():
    print ('\x1b[?25h')


def main(args):
    if args.command == 'run': 
        if args.edit:
            fun.daysession(fun.pomodoro_plus(args.edit[0],args.edit[1],args.edit[2]))
        else:
            fun.daysession(fun.pomodoro_plus(DEFAULT_WORK_TIME, DEFAULT_RELAX_TIME, DEFAULT_SESSIONS))

    if args.command == 'today':
        fun.today_tomatos()

    if args.command == 'yesterday':
        fun.yesterday_tomatos()

    if args.command == 'def':
        os.system('$EDITOR '+dir_path+'/settings.py')

    if args.command == 'new':
        if args.edit:
            ca(input(), args.edit[0], args.edit[1])
        elif args.completed:
            cafc(args.completed[0]) 
            dca(args.completed[0])
            ud('stop_time', '0', 'completed') 
            us('doing', 'completed')
        else:
            ca(input(), DEFAULT_STATUS, DEFAUTL_PLANNING_TIME)

    if args.command == 'ls':
        if args.completed:
            pca()
        else:
            ra()

    if args.command == 'del':
        if args.completed:
           dca(args.name) 
        else:
            da(args.name)

    if args.command == 'up':
        if args.status:
            us(args.value,args.name)
        if args.name_flag:
            un(args.value,args.name)
        if args.time:
            ut(args.value,args.name)

    if args.command == 'int':
       fun.interactive_mod(['python3', dir_path+'final_pomodoro.py', 'ls'])
        

def parser_cli():

    parser = argparse.ArgumentParser()
    subparsers= parser.add_subparsers(dest='command',help='sub-command help',required=True)

    parser_new = subparsers.add_parser('new', help='Add new activity')
    parser_new.add_argument("-e", dest="edit", help="Edit command", nargs=2, type=str)
    parser_new.add_argument('-c', '--completed', dest='completed', help="Print completed", nargs=1) 

    parser_delete = subparsers.add_parser('del',help='Delete activity')
    parser_delete.add_argument('name', help='Name')
    parser_delete.add_argument('-c', '--completed', dest='completed', help="Print completed", action='store_true')

    parser_ls = subparsers.add_parser('ls', help='List of activities')
    parser_ls.add_argument('-c', '--completed', dest='completed', help="Print completed", action='store_true')

    parser_update = subparsers.add_parser('up', help='Update')
    parser_update.add_argument('value')
    parser_update.add_argument('name')
    parser_update.add_argument('-s', '--status', help='Status', action='store_true') 
    parser_update.add_argument('-n', '--name', dest='name_flag', help='Name', action='store_true') 
    parser_update.add_argument('-t', '--time',  help='Time', action='store_true') 

    parser_run = subparsers.add_parser('run', help='Run default session')
    parser_run.add_argument('-e', '--edit', help='Custom session', nargs=3, type=int)

    parser_today = subparsers.add_parser('today', help='Print today')

    parser_yesterday = subparsers.add_parser('yesterday', help='Print yesterday')
    
    parser_default = subparsers.add_parser('def', help='Open default variables file')

    parser_interactive = subparsers.add_parser('int', help='Interactive mode')

    args=parser.parse_args()
    main(args)


parser_cli()
atexit.register(exit_handler)
