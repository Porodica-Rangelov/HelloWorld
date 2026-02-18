# This is a script to upload files to GitHub

import os
import sys

def upload_file(file_path):
    if os.path.exists(file_path):
        print(f'Uploading {file_path}...')
        # Code to upload file to GitHub would go here
    else:
        print('File does not exist.')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        upload_file(sys.argv[1])
    else:
        print('Please provide a file path to upload.'),

# updates