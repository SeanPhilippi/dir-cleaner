from path import Path
from tqdm import tqdm
import os
import sys

PATH = os.environ['FILE_CLEANER_DIR_PATH']

default_dir = Path(PATH)

default_patterns = [
  '*.db',
  '*.pdf',
  '*.png',
  '*.jpg',
  '*.jpeg',
  '*.m3u',
  '*.nfo',
  '*.txt',
  '*.sfv'
]

def file_cleaner(dir, patterns):
  for i in patterns:
    files = dir.walkfiles(i)
    for file in tqdm(files):
      print(file + ' removed')
      file.remove()

print('What is your file path?')
print('type * for default, or enter a file path')
file_path = input()

if file_path == '*':
  dir = default_dir
else:
  dir = Path(file_path)

print(f'Your file path is {dir}. Is this correct?')
print('type "y" for "yes" or "n" for "no"')
answer = input()

if answer != 'y':
  sys.exit()

print('What file types do you want to delete?')
print('type * for default, or enter comma separated extensions to delete')
file_types = input()

patterns = []
if file_types == '*':
  patterns = default_patterns
else:
  extension_list = file_types.split(',')

  for item in extension_list:
    item.strip(' .')
    item = '*.' + item
    patterns.append(item)

file_cleaner(dir, patterns)