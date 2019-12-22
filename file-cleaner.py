from path import Path
import os

PATH = os.environ["FILE_CLEANER_DIR_PATH"]

dir = Path(PATH)

patterns = ['*.db', '*.pdf', '*.png', '*jpg', '*jpeg']

for i in patterns:
  files = dir.walkfiles(i)
  for file in files:
    file.remove()
    print(file)