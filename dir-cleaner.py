from path import Path
from tqdm import tqdm
import os
import sys
import argparse

# TODO
# 1. have this script delete files of certain types, THEN
# detect if 1 folder or file is in another folder, if so, mv inner folder or file out,
# and delete parent folder

default_patterns = [
    "*.db",
    "*.pdf",
    "*.png",
    "*.jpg",
    "*.jpeg",
    "*.m3u",
    "*.nfo",
    "*.NFO",
    "*.txt",
    "*.sfv",
    "*.htm",
    "*.html",
    "*.ini",
]

transmission_dwlds_patterns = [
    "*.db",
    "*.png",
    "*.jpg",
    "*.jpeg",
    "*.m3u",
    "*.nfo",
    "*.NFO",
    "*.txt",
    "*.sfv",
    "*.htm",
    "*.html",
    "*.ini",
]

parser = argparse.ArgumentParser(description="Clean directory of certain file types and empty folders.")

parser.add_argument(
    "-p",
    "--path",
    help=f"Path to directory for cleaning. Default is {os.environ['MUSIC_PATH']}.",
    default="MUSIC_PATH",
)

parser.add_argument(
    "-x",
	"--empty",
    help="Give value 't' to delete empty folders, 'f' to leave them alone. Defaults to 't'.",
    default='t',
)

args = parser.parse_args()
dir_path = Path(os.environ[args.path])
empty = args.empty

def dir_cleaner(dir, empty):
    if dir == "TRANSMISSION_DWLDS_PATH":
        patterns = transmission_dwlds_patterns
    else:
        patterns = default_patterns
	# walk files and remove files with an extension in patterns list
    for ext in patterns:
        files = dir.walkfiles(ext)
        for file in tqdm(files):
            print(file, " removed")
            file.remove()
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

print("==options==")
print("path:", os.environ(dir_path))
print("empty folders:", empty)

dir_cleaner(dir_path, empty)
