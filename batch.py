#!/usr/bin/env python3

# batch conversion of danmaku files to .ass files

import os
import sys
try:
    import threading
except ImportError:
    import dummy_threading as threading
import time

def safe_chdir(directory):
    try:
        os.chdir(directory)
    except FileNotFoundError:
        print('\nFileNotFoundError: please input the right directory!')
        return False
    except NotADirectoryError:
        print('\nNotADirectoryError: please input the right directory!')
    except:
        print('\nUnexpected error:', sys.exc_info()[0], 'please input the right directory!')
        return False
    else:
        return True


def cmdlist(script_dir, danmaku_dir, size, form = 'autodetect', fn = 'sans-serif', fs = '25', alpha = '1.0', dm = '5', ds = '5', fit = '', protect = '0', reduce = False, ex_extension = 0):
    # script_dir: dircectory of danmaku2ass.py
    # danmaku_dir: dircectory of the original danmaku files
    # form: format of input file (autodetect|Bilibili|Tudou2|MioMio|Acfun|Niconico|Tudou) [default: autodetect]
    # size: stage size in pixels, eg: 1920x1080
    # fn: specify font face [default: sans-serif]
    # fs: font size [default: 25]
    # alpha: Text opacity [default: 1.0]
    # dm: duration of scrolling comment display [default: 5]
    # ds: duration of still comment display [default: 5]
    # fit: regular expression to filter comments
    # protect: reserve blank on the bottom of the stage [default: 0]
    # reduce: reduce the amount of comments if stage is full [default: False]

    # ex_extension: extra extension in the danmaku files [default: 0]
    # (eg: when converting *.cmt.xml to *.ass, the extra extension is .cmt, so ex_extension = 4)

    if os.name == 'nt':
        py_name = '\"' + sys.executable + '\" '
        script_dir = script_dir + '\\'
        danmaku_dir = danmaku_dir + '\\'
    else:
        py_name = 'python3 '
        script_dir = script_dir + '/'
        danmaku_dir = danmaku_dir + '/'
    
    files =  [x for x in os.listdir(danmaku_dir) if os.path.isfile(danmaku_dir + x) and os.path.splitext(danmaku_dir + x)[1] in ['.xml', '.json']]
    command_list = []
    for file in files:
        file_extension = len(file.split('.')[-1]) + 1 + ex_extension           # file extension length
        command = py_name + r'"' + script_dir + 'danmaku2ass.py' + r'"' \
                + ' -f ' + form \
                + ' -o ' + r'"' + danmaku_dir + file[:-file_extension] + '.ass' + r'"' \
                + ' -s ' + size \
                + ' -fn ' + r'"' + fn + r'"' \
                + ' -fs ' + fs \
                + ' -a ' + alpha \
                + ' -dm ' + dm \
                + ' -ds ' + ds \
                + ' -p ' + protect
        if fit:
            command = command + ' -fl ' + '\"' + fit + '\"'
        if reduce:
            command = command + ' -r'
        command = command + ' \"' + danmaku_dir + file + '\"'
        command_list.append(command)

    return command_list


def excommad(cmd):
    print('converting ' + cmd.split('\"')[-2] + os.popen(cmd).read())


def timer():
    if sys.platform == 'win32':
        return time.clock()
    else:
        return time.time()


def main():
    script_dir = os.path.abspath(sys.argv[0][:-8])

    danmaku_dir = input('\nPlease input the directory of your danmaku files: ')
    while not safe_chdir(danmaku_dir):
        danmaku_dir = input('\nPlease input the directory of your danmaku files: ')
    danmaku_dir = os.getcwd()

    size = input('\nPlease input your stage size in pixels(eg:1920x1080): ')
    size = size.lower()
    
    print('\nstart converting...\n')
    start = timer()

    # you-get downloaded files, *.cmt.xml | *.cmt.json --> *.ass
    # if you want to convert *.xml and *.json to *.ass, set  ex_extension to 0
    command_list = cmdlist(script_dir, danmaku_dir, size, fn ='MS PGothic', dm = '8', ex_extension = 4)

    thread_list = []
    for cmd in command_list:
        thread_list.append(threading.Thread(target = excommad, args = (cmd,)))

    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()

    count = timer() - start
    print("Time used: %.2f seconds" %count)
    
    input('\npress Enter to exit...')


main()
