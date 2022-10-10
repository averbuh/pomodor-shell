import os
import time
import sys
import subprocess
import threading
import tkinter
import keyboard


from settings import * 
from soundtest import soundplay as alert
from datetime import date, timedelta, datetime
from create_activity import copy_activity, return_activities as ra
from create_activity import return_for_file as rff
from create_activity import get_value
from update_data import update_data as ud
from delete_activity import delete_activity as da

nowtime = datetime.now()
yestime = date.today() - timedelta(days=1)
time_string = nowtime.strftime("%H:%M:%S")
d_string = nowtime.strftime("%d.%m.%Y")
yesterday = yestime.strftime("%d.%m.%Y")

img_med=dir_path+'img/meditation.txt'
img_mot=dir_path+'img/motivation.txt'
daylogs=dir_path+'daylogs/'
activities=dir_path+'activities.txt'
activities_temp=dir_path+'activities_temp.txt'


def fileread(link, print_status=True, tab=False):
    lines = 0
    with open(link) as f:
        for line in f:
            if tab==True:
                sys.stdout.write("\t\t\t         ") 
            if print_status!=False:
                print(line.strip())
            lines+=1
    return lines


def filewrite_fromfile(fromlink,tolink):
    with open(fromlink,'r') as firstfile, open(tolink,'w') as secondfile:
        for line in firstfile:
            secondfile.write(line)


def similar_files(fromlink,tolink):
    with open(fromlink,'r') as firstfile, open(tolink, 'r') as secondfile:
        for linef in firstfile:
            flag=False
            for lines in secondfile:
                if linef == lines:
                    flag = True
                    break 
            if flag == False: return flag
    return True

      
def restart_activities_sql():
    lines = ra(False)
    print("\n\x1b["+str(lines) + "A\x1b[0J\x1b[1A")
    open(activities_temp, 'w').write(str(rff()))
    ra()


def interactive_mod(table):
    '''
    Interactive visual edit mode 
    '''
    user = 'ls'
    try:
        while True:
            subprocess.run(['clear'], check=True)
            pathtotomato = 'python3 '+ dir_path + 'final_pomodoro.py'
            subprocess.run(table, check=True)
            print('\nInput command: ([q] for exit)\n')
            input()
            if user == 'q':
                os.system('clear')
                break
            elif user == 'ls -c':
                table =  ['python3', dir_path+'final_pomodoro.py', 'ls', '-c']
                continue
            elif user == 'ls':
                table = ['python3', dir_path+'final_pomodoro.py', 'ls']
                continue
            elif user == '-h' or user == '--help' or user == 'help' or user == 'h':
                table = ['python3', dir_path+'final_pomodoro.py', '-h']
                continue
            command = pathtotomato + ' ' + user 
            subprocess.run(command.split(' '), check=True) 
            if user.split(' ')[1] == '-h':
                table = ['python3', dir_path+'final_pomodoro.py', user.split(' ')[0], '-h']
                
    except:
        interactive_mod(table)

def increase_time(status):
    '''
    Increase time depending on the status.
    '''
    for item in status:
        if item in open(activities).read():
            x=0
            for value in get_value('stop_time', item):
                for i in range(x, len(get_value('name',item))):
                        ud('stop_time', str(1+int(value[0])), str(get_value('name',item)[i][0])) 
                        break
                x+=1


def timer_activities(min, sec, part):
    """
    Timer with list of activities
    """
    if min == 0:
        min = sec / 60
    else:
        sec += min * 60
    ra()
    #signal.signal(signal.SIGTSTP, handler)
    temp_min=min
    
    try:
            while sec > 0: 
                sec-=1
                time.sleep(SPEED)    
                min = sec / 60
                seconds = sec-int(min)*60
                if temp_min > int(min): 
                    temp_min = int(min)
                    if part == 'work':
                        increase_time(RUN_STATUS_WORK)
                    if part == 'relax':
                        increase_time(RUN_STATUS_RELAX)
                if 'completed' in open(activities).read():
                    x=0 
                    for value in get_value('stop_time','completed'):
                        for i in range(x,len(get_value('name','completed'))):
                            ud('completed_time',value[0], str(get_value('name','completed')[i][0])) 
                            break
                        x+=1
                    copy_activity('completed')
                    da('completed') 

                open(activities, 'w').write(str(rff()))
                if similar_files(activities, activities_temp) == False:
                    restart_activities_sql()
                print("\t\t\t\t   \x1b[?25l \x1b[1;32m",int(min),":\033[K",seconds,"\x1b[0;0m", end="\r")
    except:
        os.system('clear')
        while True:
            print("\x1b[?25h\nExit - [q]\nEdit mode - [e]\nContinue\n")
            command=str(input())
            if command == 'q': return True
            elif command == '': break
            elif command == 'e':
                interactive_mod(['python3', dir_path+'final_pomodoro.py', 'ls'])
                break
        os.system('clear')
        return timer_activities(0, sec, part)

    return False


def pomodoro_plus(min_work, min_relax, tomatos):
    """
    Sessions with timer_activities function inside.  
    """
    status = False
    tomato_count=0
    
    while tomato_count < tomatos :

       #working 
        part='work'
        os.system('clear')
        if DEFAULT_IMG == 'text':
            os.system("echo '  DO IT!' | figlet -c -f lean | tr ' _/' ' ##'")
        if DEFAULT_IMG == 'img':
            fileread(img_mot,True,False)
        print("\x1b[1;31m\n \t\t\t     You have ",tomato_count,"/",tomatos," tomatos.\x1b[0;0m")
        status = timer_activities(min_work, 0, part)
        if status: break
        tomato_count+=1
        alert()

       #relaxing
        part='relax'
        os.system('clear')
        if DEFAULT_IMG == 'text':
            os.system("echo '  RELAX' | figlet -c -f lean | tr ' _/' ' ()'")
        if DEFAULT_IMG == 'img':
            fileread(img_med,True,False)
        print("\x1b[1;31m\n \t\t\t   You have ",tomato_count,"/",tomatos," tomatos.\x1b[0;0m")
        status = timer_activities(min_relax, 0, part)
        if status: break
        alert()

    os.system('clear')
    if tomato_count == tomatos:
        print("You have ",tomato_count,"/",tomatos," tomatos.\n It's unbelievable!")
    elif tomato_count == 0:
        print("You have ",tomato_count,"/",tomatos," tomatos.\nWhy you did nothing?")
    else: print("You have ",tomato_count,"/",tomatos," tomatos.\nGood job!")

    return tomato_count  


def daysession(add_tomato):
    """
    Append day log file with number of tomatos per session.
    """ 

    os.system('touch ' + daylogs + d_string)
    text_file = open(daylogs + d_string,"a")
    text_file.write(time_string + " " + str(add_tomato) + " tomatos" +"\n")
    text_file.close()


def day_tomatos(date, dayname):
    """
    Print tomatos you did in specific day.
    """
    sum = 0
    try:
        text=open(daylogs + date, "r")
        with text as f:
            for line in f:
                split_string = line.split(" ")
                sum += int(split_string[1])
        print("\nYou have ", sum, " tomatos " + dayname + ".")
        text.close()
    
    except:
        print("You didn't create sessions today!")


def today_tomatos():
    """
    Print today tomatos
    """
    day_tomatos(d_string, "today")


def yesterday_tomatos():
    """
    Print yesterday tomatos
    """
    day_tomatos(yesterday, "yesterday")


if __name__ == "__main__":
    pass

