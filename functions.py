import os
import time
import sys
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


def cust_session(min, sec, part):
    """
    Timer with motivation image and list of activities
    """
    sec += min * 60
    ra()
    #signal.signal(signal.SIGTSTP, handler)
    temp_min=min-1
    try:

        while sec > 0:
            sec-=1
            time.sleep(1)    
            min = sec / 60
            seconds = sec-int(min)*60

            if temp_min > int(min) and part == 'work': 
                temp_min = int(min)
                if 'doing' in open(activities).read():
                    x=0
                    for value in get_value('stop_time','doing'):
                        for i in range(x, len(get_value('name','doing'))):
                                ud('stop_time', str(1+int(value[0])), str(get_value('name','doing')[i][0])) 
                                break
                        x+=1
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
            print("\t\t\t\t    \x1b[?25l \x1b[1;32m",int(min),":\033[K",seconds,"\x1b[0;0m", end="\r")
    except:
        os.system('clear')
        print("End session?\n(y or n)")
        if input() == 'y': return True
        os.system('clear')
        print("Continue:")
        return cust_session(0, sec, part)
    

    return False


def pomodoro_plus(min_work, min_relax, tomatos):
    """
    Pomodoro timer with working and relax sessions.
    """
    status = False
    tomato_count=0
    
    while tomato_count < tomatos :

       #working 
        part='work'
        os.system('clear')
        fileread(img_mot,True,False)
        print("\x1b[1;31m\n \t\t\t     You have ",tomato_count,"/",tomatos," tomatos.\x1b[0;0m")
        status = cust_session(min_work, 0, 'work')
        if status: break
        tomato_count+=1
        alert()

       #relaxing
        part='relax'
        os.system('clear')
        fileread(img_med,True,False)
        print("\x1b[1;31m\n \t\t\t   You have ",tomato_count,"/",tomatos," tomatos.\x1b[0;0m")
        status = cust_session(min_relax, 0, 'relax')
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


def printDaytomatos(date, dayname):
    """
    Print how much tomatos you did in this day
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
    printDaytomatos(d_string, "today")


def yesterday_tomatos():
    """
    Print yesterday tomatos
    """
    printDaytomatos(yesterday, "yesterday")


if __name__ == "__main__":
    pass

