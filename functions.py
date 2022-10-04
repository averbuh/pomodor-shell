import os
import time
import sys
import signal

from soundtest import soundplay as alert
from playsound import playsound
from datetime import date, timedelta, datetime


nowtime = datetime.now()
yestime = date.today() - timedelta(days=1)
t_string = nowtime.strftime("%H:%M:%S")
d_string = nowtime.strftime("%d.%m.%Y")
yesterday = yestime.strftime("%d.%m.%Y")


audio_link='/home/alex/database/scripts/python/flute.wav'
img_med='/home/alex/database/scripts/python/tomato_app/img/meditation.txt'
img_mot='/home/alex/database/scripts/python/tomato_app/img/motivation.txt'
daylogs='/home/alex/database/scripts/python/tomato_app/daylogs/'
activities='/home/alex/database/scripts/python/tomato_app/activities.txt'
activities_temp='/home/alex/database/scripts/python/tomato_app/activities_temp.txt'


#def handler(signum, frame):
#    if signum == signal.SIGTSTP:
#        signal.signal(signal.SIGTSTP, signal.SIGTSTP)
#        sys.stdout.write("\n\x1b[1;34m")
#        fileread(activities,True,True)
#        sys.stdout.write("\n\x1b[0;0m")
    

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


def restart_activities(first=False):
    linesf=fileread(activities, False)
    liness=fileread(activities_temp, False)
    if first:
        print("")
        fileread(activities,True,True)
        filewrite_fromfile(activities,activities_temp)
    elif not similar_files(activities,activities_temp) or linesf != liness:
        print("\x1b["+str(liness) + "A\x1b[0J\x1b[1A")
        fileread(activities,True,True)
        filewrite_fromfile(activities,activities_temp)
    elif not similar_files(activities,activities_temp) and linesf != liness:
        print("\n\x1b["+str(liness) + "A\x1b[0J\x1b[1A")
        fileread(activities,True,True)
        filewrite_fromfile(activities,activities_temp)
    
      
def cust_session(min, sec):
    """
    Timer with motivation image and list of activities
    """

    sec += min * 60
    first=True
    #signal.signal(signal.SIGTSTP, handler)
    try:
        while sec > 0:
            sec-=1
            time.sleep(1)    
            min = sec / 60
            seconds = sec-int(min)*60
            sys.stdout.write("\x1b[1;34m")
            restart_activities(first)
            first=False
            sys.stdout.write("\x1b[0;0m")
            print("\t\t\t\t    \x1b[?25l \x1b[1;32m",int(min),":\033[K",seconds,"\x1b[0;0m", end="\r")

    except:
        os.system('clear')
        print("End session?\n(y or n)")
        if input() == 'y': return True
        os.system('clear')
        print("Continue:")
        return cust_session(0, sec)
    

    return False


def pomodoro_plus(min_work, min_relax, tomatos):
    """
    Pomodoro timer with working and relax sessions.
    """
    status = False
    tomato_count=0
    
    while tomato_count < tomatos :

       #working 
        os.system('clear')
        fileread(img_mot,True,False)
        print("\x1b[1;31m\n \t\t\t     You have ",tomato_count,"/",tomatos," tomatos.\x1b[0;0m")
        status = cust_session(min_work, 0)
        if status: break
        tomato_count+=1
        #playsound(audio_link, block=False)
        alert()

       #relaxing
        os.system('clear')
        fileread(img_med,True,False)
        print("\x1b[1;31m\n \t\t\t   You have ",tomato_count,"/",tomatos," tomatos.\x1b[0;0m")
        status = cust_session(min_relax, 0)
        if status: break
        #playsound(audio_link, block=False)
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
    text_file.write(t_string + " " + str(add_tomato) + " tomatos" +"\n")
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

