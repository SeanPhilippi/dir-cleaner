from path import Path
import os

PATH = os.getenv['DIR_PATH']

dir = Path(PATH)
dir.walkfiles('*')
list(dir.walkfiles())

# files = dir.walkfiles('*.jpg')
# files = dir.walkfiles('*.png')
# files = dir.walkfiles('*.pdf')
files = dir.walkfiles('*.db')
for file in files:
  file.remove()
  print(files)
