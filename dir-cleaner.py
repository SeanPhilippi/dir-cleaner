from path import Path
from tqdm import tqdm
import os
import sys
import argparse

# TODO
# 1. add new bash alisas that clean different folders, Downloads vs Music for instance
# 2. have this script delete files of a certain types, THEN
# detect if 1 folder or file is in another folder, if so, mv inner folder or file out,
# and delete parent folder

PATH = os.environ["FILE_CLEANER_DIR_PATH"]

default_dir = Path(PATH)

default_patterns = [
    "*.db",
    "*.pdf",
    "*.png",
    "*.jpg",
    "*.jpeg",
    "*.m3u",
    "*.nfo",
    "*.txt",
    "*.sfv",
    "*.htm",
    "*.ini",
]


parser = argparse.ArgumentParser(description="Clean directory of certain file types and empty folders.")

parser.add_argument(
    "-p",
    "--path",
    help=f"Path to directory for cleaning. Default is {default_dir}.",
    default=default_dir,
)

parser.add_argument(
    "-e",
    "--extensions",
    nargs="+",
    help="Space separated list of extentions to match for deletion. ex). python3 file-cleaner.py -e .db .pdf .txt Default is "
    + " ".join(default_patterns),
    default=default_patterns,
)

parser.add_argument(
    "-x",
	"--empty",
    help="Give value 't' to delete empty folders, 'f' to leave them alone. Defaults to 't'.",
    default='t',
)

args = parser.parse_args()
dir_path = args.path
extensions = args.extensions
empty = args.empty


def dir_cleaner(dir, patterns, empty):
	# walk folders and delete any that are empty
	if empty == 't':
		folders = list(os.walk(dir))[1:]
		for folder in folders:
			if not folder[1] and not folder[2]:
				# index = folder[0].rfind('/')
				# folder_name = folder[0][index + 1:]
				# print(folder_name, 'removed')
				print(folder[0], 'removed')
				os.rmdir(folder[0])
	# walk files and remove files with an extension in patterns list
	for i in patterns:
		files = dir.walkfiles(i)
		for file in tqdm(files):
			print(file, " removed")
			file.remove()


patterns = []
for item in extensions:
    item = item.strip(" *.,")
    item = "*." + item
    patterns.append(item)

print("==options==")
print("path:", dir_path)
print("patterns:", patterns)
print("empty folders:", empty)

dir_cleaner(dir_path, patterns, empty)
