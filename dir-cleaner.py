from path import Path
from tqdm import tqdm
import os
import sys
import argparse
import shutil
from send2trash import send2trash
from datetime import datetime

# TODO
# 1. have this script delete files of certain types, THEN
# detect if 1 folder or file is in another folder, if so, mv inner folder or file out,
# and delete parent folder
# 2. tqdm still isn't progressing per folder it is processing, need to fix this

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
    ".DS_Store",
    "Thumb.db",
    "*.url",
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
    "*.url",
]

parser = argparse.ArgumentParser(description="Clean directory of certain file types and empty folders.")

parser.add_argument(
    "-p",
    "--path",
    help=f"Path to directory for cleaning. Default is {os.environ.get('MUSIC_PATH')}.",
    default="MUSIC_PATH",
)

parser.add_argument(
    "-x",
	"--empty",
    help="Give value 't' to delete empty folders, 'f' to leave them alone. Defaults to 't'.",
    default='t',
)

args = parser.parse_args()
try:
    # check that the path key given for path argument is in os.environ
    dir_path = Path(os.environ.get(args.path))
except:
    print(f"{args.path} was not found in the env")
    sys.exit()
empty = args.empty

def dir_cleaner(dir, empty):
    # create a directory for the cleaned files w current date
    now = datetime.now()
    cleaned_dir = Path(f"cleaned-{now.year}-{now.month}-{now.day}")
    cleaned_dir.mkdir()

    if dir == "TRANSMISSION_DWLDS_PATH":
        patterns = transmission_dwlds_patterns
    else:
        patterns = default_patterns
	# walk files and remove files with an extension in patterns list
    for ext in tqdm(patterns):
        files = dir.walkfiles(ext)
        for file in files:
            # create a new directory for this file, named after its original directory
            new_dir = cleaned_dir / file.parent.name
            new_dir.mkdir()
            print(file, "moved to", new_dir)
            shutil.move(str(file), str(new_dir))
	# walk folders and delete any that are empty
    if empty == "t":
        folders = list(os.walk(dir))[1:]
        for folder in folders:
            if not folder[1] and not folder[2]:
                # create new directory for this folder, named after its original directory
                new_dir = cleaned_dir / Path(folder[0]).parent.name
                print(folder[0], "moved to", cleaned_dir)
                shutil.move(folder[0], str(cleaned_dir))
    if os.listdir(cleaned_dir):
        # move the cleaned dir to the Trash
        send2trash(str(cleaned_dir))

print("==options==")
print("path:", dir_path)
print("empty folders:", empty)

dir_cleaner(dir_path, empty)
