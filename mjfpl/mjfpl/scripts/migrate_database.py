"""
Script for migrate data from old database to new database
"""

import sys
import pathlib

from mjfpl.mjfpl.model.words_model import WordsModel

if not len(sys.argv) == 3:

    sys.exit()

old_database = pathlib.Path.cwd().parent.joinpath(sys.argv[1])
new_database = pathlib.Path.cwd().parent.joinpath(sys.argv[2])

if not old_database.is_file():
    print("Not exist old database")
    sys.exit()
if not new_database.is_file():
    print("Not exist new database")
    sys.exit()

wm = WordsModel
