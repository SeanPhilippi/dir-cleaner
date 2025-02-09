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
    default="MUSIC_PATH",
    # default="TEST_PATH",
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
    print(os.getcwd())
    # create a directory for the cleaned files w current date
    now = datetime.now()
    cleaned_dir = Path(f"cleaned-{now.year}-{now.month}-{now.day}")
    if not cleaned_dir.exists():
        cleaned_dir.mkdir()

    # create a directory for duplicate dirs in the cleaned_dir folder
    dupe_dirs = cleaned_dir / "duplicate-dirs"
    if not dupe_dirs.exists():
        dupe_dirs.mkdir()

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
            if not new_dir.exists():
                try:
                    new_dir.mkdir()
                except OSError as e:
                    print(f"Error creating {new_dir}: {e}")
                    continue

            try:
                shutil.move(file, new_dir / file.name)
                print(file, "moved to", new_dir)
            except OSError as e:
                print(f"Error moving {file} to {new_dir}: {e}")

    # regular expression pattern for folder names to keep
    keep = re.compile(r".*\(\d{4}\)$")
    dirs_to_move = []

    # walk through the directories and remove any that are duplicates
    for root, dirs, files in os.walk(dir):
        # if the folder name doesn't match the pattern, check for a duplicate
        # sort the directories in alpha order
        dirs.sort()
        prev_name = None
        for i, name in enumerate(dirs):
            if prev_name is not None:
                dir_path = os.path.join(root, name)
                prev_dir_path = os.path.join(root, prev_name)
                dir_files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
                prev_dir_files = [f for f in os.listdir(prev_dir_path) if os.path.isfile(os.path.join(prev_dir_path, f))]
                if prev_name.lower() == name.lower() or name.lower().startswith(prev_name.lower()) or prev_name.lower().startswith(name.lower()):
                    # check if number of files is the same and there are no subdirectories
                    if len(dir_files) == len(prev_dir_files) and not any(os.path.isdir(os.path.join(dir_path, f)) for f in os.listdir(dir_path)):
                        # if both names are dupes but the years are the same
                        if keep.match(prev_name) and keep.match(name):
                            # print("==same but different casing, would move this:", name)
                            dirs_to_move.append(os.path.join(root, name))
                        elif keep.match(prev_name):
                            # print("==would move this dupe 1:", name, "vs this:", prev_name)
                            dirs_to_move.append(os.path.join(root, name))
                        elif keep.match(name):
                            # print("==would move this dupe 2:", prev_name, "vs this:", name)
                            dirs_to_move.append(os.path.join(root, prev_name))
                        else:
                            print("==would move this dupe but matches none of the cases:", prev_name, "vs this:", name)
            prev_name = name
    # move the duplicate directories to the duplicate-dirs folder
    for dir_path in dirs_to_move:
        # print('==moving to dupes folder:', dir_path)
        shutil.move(dir_path, dupe_dirs)
	# walk folders and delete any that are empty
    if empty == "t":
        folders = list(os.walk(dir))[1:]
        for folder in folders:
            # if list of subdirs and list of files are both empty
            if not folder[1] and not folder[2]:
                # create new directory for this folder, named after its original directory
                new_dir = cleaned_dir / Path(folder[0]).parent.name
                print(folder[0], "moved to", cleaned_dir)
                shutil.move(folder[0], str(cleaned_dir))
    cleaned_dir_contents = os.listdir(cleaned_dir)
    if cleaned_dir_contents:
        # if cleaned_dir isn't empty but it only has duplicate-dirs folder and that folder is empty
        print(f'==cleaned_dir {cleaned_dir}')
        print(f'list of cleaned_dir: {cleaned_dir_contents}')
        if len(cleaned_dir_contents) == 1 and 'duplicate-dirs' in cleaned_dir_contents and not os.listdir(dupe_dirs):
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
