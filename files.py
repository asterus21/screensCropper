import datetime
import os
import sys
from pathlib import Path


def get_time():
    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time


def process_input(user_input: str) -> str:
    p = Path(user_input)
    # print(p)    
    try: 
        p.exists() and p.is_dir()
    except:
        print('No valid path is provided.')
        sys.exit(1)


def get_input() -> str:
    files = lambda folder: [file for file in os.listdir(folder) if file.lower().endswith('.png')]
    def is_empty(files_list):
        if not files_list:
            print(get_time(), 'The list of files to process is empty. The program is about to close.')
            sys.exit(1)        
        else: return files_list
    user_input = input('Enter a path to the PNG files to crop (e.g. D:/screens) or press Enter to use a current directory (type exit to quit): ')
    print()
    if user_input.endswith(':'): user_input = user_input + '/'
    match user_input:
        case 'exit':
            print(get_time(), 'The program is about to close.')
            sys.exit(0)
        case '':
            print(get_time(), 'Current directory is being used.')
            return is_empty(files(os.getcwd()))
        case _:
            process_input(user_input)
            return is_empty(files(user_input))
    return user_input
