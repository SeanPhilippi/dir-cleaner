from path import Path
from tqdm import tqdm
import os
import sys
import argparse
import re
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
    # default="MUSIC_PATH",
    default="TEST_PATH",
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

    # create a directory for duplicate dirs
    dupe_dirs = cleaned_dir / "duplicate-dirs"
    dupe_dirs.mkdir()

    if dir == "TRANSMISSION_DWLDS_PATH":
        patterns = transmission_dwlds_patterns
    else:
        patterns = default_patterns

    # regular expression pattern for folder names to keep
    keep = re.compile(r".*\(\d{4}\)$")

    # walk through the directories and remove any that are duplicates
    for root, dirs, files in os.walk(dir):
        # if the folder name doesn't match the pattern, check for a duplicate
        # sort the directories in alpha order
        dirs.sort()
        prev_name = None
        for i, name in enumerate(dirs):
            if prev_name is not None:
                print(prev_name)
                print(name, '\n')
                dir_path = os.path.join(root, name)
                prev_dir_path = os.path.join(root, prev_name)
                dir_files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
                prev_dir_files = [f for f in os.listdir(prev_dir_path) if os.path.isfile(os.path.join(prev_dir_path, f))]
                if prev_name.lower() == name.lower() or name.lower().startswith(prev_name.lower()) or prev_name.lower().startswith(name.lower()):
                    # check if number of files is the same and there are no subdirectories
                    if len(dir_files) == len(prev_dir_files) and not any(os.path.isdir(os.path.join(dir_path, f)) for f in os.listdir(dir_path)):
                        # if both names are dupes but the years are the same
                        # ! think I have to check that the years are not equal still
                        if keep.match(prev_name) and keep.match(name):
                            print("==would leave this alone 0:", prev_name, name)
                            print(f"Error: Both '{prev_name}' and '{name}' are duplicates but the years are different")
                        elif keep.match(prev_name):
                            print("==would move this dupe 1:", os.path.join(root, name), "vs this:", os.path.join(root, prev_name))
                            # shutil.move(os.path.join(root, name), dupe_dirs)
                        elif keep.match(name):
                            print("==would move this dupe 2:", os.path.join(root, prev_name), "vs this:", os.path.join(root, name))
                            # shutil.move(os.path.join(root, prev_name), dupe_dirs)
            prev_name = name

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
        # if cleaned_dir isn't empty but it only has duplicate-dirs folder and that folder is empty
        if len(os.listdir(cleaned_dir)) == 1 and 'duplicate-dirs' in os.listdir(cleaned_dir) and not os.listdir(dupe_dirs):
            dupe_dirs.rmdir()
            cleaned_dir.rmdir()
        else:
            # move the cleaned dir to the Trash
            send2trash(str(cleaned_dir))
    # if cleaned_dir is empty, delete it
    else:
        cleaned_dir.rmdir()

print("==options==")
print("path:", dir_path)
print("empty folders:", empty)

dir_cleaner(dir_path, empty)
