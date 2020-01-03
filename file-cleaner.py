from path import Path
import os

PATH = os.environ["FILE_CLEANER_DIR_PATH"]

default_dir = Path(PATH)

default_patterns = ['*.db', '*.pdf', '*.png', '*.jpg', '*.jpeg', '*.m3u', '*.nfo', '*.txt']

def file_cleaner(dir, patterns):
  for i in patterns:
    files = dir.walkfiles(i)
  for file in files:
    file.remove()
    print(file)

print('What is your file path?')
print('"default" for default, or enter a file path')
answer = input()
if answer == 'default':
  dir = default_dir
else:
  dir = Path(answer)
print('What file types do you want to delete?')
print('"default" for default, or enter comma separated extentions to delete')
answer2 = input()

patterns = []

if answer2 == 'default':
  patterns = default_patterns
else:
  extension_list = answer2.split(',')

  for item in extension_list:
    item.strip(' .')
    item = '*.' + item
    patterns.append(item)

file_cleaner(dir, patterns)