import datetime
import os
import sys


def get_time():
    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time


def get_input() -> str:
    files = lambda folder: [file for file in os.listdir(folder) if file.lower().endswith('.png')]
    is_empty = lambda files_list: print('The list of files to process is empty. The program is about to close.') and sys.exit(0) if not files_list else files_list
    user_input = input('Enter a path to the PNG files to crop (e.g. D:/screens) or press Enter to use a current directory (type exit to quit): \n')
    match user_input:
        case 'exit':
            print(get_time(), 'The program is about to close.')
            sys.exit(0)
        case '':
            print(get_time(), 'Current directory is being used.')
            return is_empty(files(user_input)) if user_input else is_empty(files(os.getcwd()))
    if not os.path.isdir(user_input):
        print(get_time(), 'Folder does not exist. The program is about to close.')
        sys.exit(0)    
    return user_input
