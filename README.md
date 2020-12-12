Program for cleaning a folder of empty folders and files with a certain extension.

To run:

python3 file-cleaner.py -p [dir path] -e [extensions] -x [t or f]

separate extensions by a space. ex). python3 file-cleaner -e .txt .md .jpg

-x is a toggle for deleting empty folders or not. 't' to do so, 'f' to leave them alone. Defaults to 't'. 
