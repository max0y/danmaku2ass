#!/usr/bin/env python3

# batch conversion of bilibili .xml files to .ass files

import os
import sys

def safe_chdir(directory):
    try:
        os.chdir(directory)
    except FileNotFoundError:
        print('\nFileNotFoundError: please input the right directory!')
        return False
    except NotADirectoryError:
        print('\nNotADirectoryError: please input the right directory!')
    except:
        print('\nUnexpected error:', sys.exc_info()[0])
        raise
    else:
        return True

# directory = r'D:\download\video\xml'
# size = '1920x1080'  # Stage size in pixels
form = 'autodetect' # Format of input file
fn = 'MS PGothic'   # Specify font face
fs = '30'           # Default font size
alpha = '1.0'       # Text opacity
dm = '8'            # Duration of scrolling comment display
ds = '5'            # Duration of still comment display
fit = ''            # Regular expression to filter comments
protect = '0'       # Reserve blank on the bottom of the stage
reduce = False      # Reduce the amount of comments if stage is full


if os.name == 'nt':
    py_name = '\"' + sys.executable + '\" '
    current_dir = os.path.abspath(sys.argv[0][:-8]) + '\\'
else:
    py_name = 'python3 '
    current_dir = os.path.abspath(sys.argv[0][:-8]) + '/'

directory = input('\nPlease input the directory of .xml files: ')
while not safe_chdir(directory):
    directory = input('\nPlease input the directory of .xml files: ')

size = input(r'Please input the resolution of videos(eg:1920x1080): ')
size = size.lower()

# list of .xml files in the directory
files =  [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.xml']

for file in files:
    # you-get download files, *.cmt.xml --> *.ass
    command = py_name + r'"' + current_dir + 'danmaku2ass.py' + r'"' \
              + ' -f ' + form \
              + ' -o ' + r'"' + file[:-8] + '.ass' + r'"' \
              + ' -s ' + size \
              + ' -fn ' + r'"' + fn + r'"' \
              + ' -fs ' + fs \
              + ' -a ' + alpha \
              + ' -dm ' + dm \
              + ' -ds ' + ds \
              + ' -p ' + protect
    if fit:
        command = command + ' -fl ' + fit
    if reduce:
        command = command + ' -r'

    command = command + r' "' + file + r'"'
    print('converting ', file)
    print(os.popen(command).read())

input('press Enter to exit...')
