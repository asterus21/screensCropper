import os
import sys


def get_user_input() -> str:
    user_input = input('Enter a valid path to the PNG files to crop (e.g. D:/screens): ')
    match user_input:
        case 'exit':
            print('The program is about to close.')
            sys.exit(0)
        case '':
            print('No valid path is provided. The program is about to close.')
            sys.exit(1)
    if not os.path.isdir(user_input):
        print('Folder does not exist. The program is about to close.')
        sys.exit(1)        
    return user_input


def get_files_list(path=False) -> list:
    files = lambda folder: [file for file in os.listdir(folder) if file.lower().endswith('.png')]
    def is_empty(files_list):
        if not files_list: 
            print('The list of files to process is empty. The program is about to close.')
            sys.exit(0)
        else:
            return files_list
    return is_empty(files(get_user_input())) if path else is_empty(files(os.getcwd()))


# def main(path):
#     x = get_files_list(path)
#     print(x)
# 
# 
# if __name__ == '__main__':
#     main(path=False)
