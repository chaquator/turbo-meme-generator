'''
Setup
	Requirements
		py2exe
		
	Notes
		If you get an "Access is denied." error, run the command again lol.
'''

from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
    options = {
		"py2exe": {
			"bundle_files": 0,
			"compressed": 1,
			"optimize": 2,
			"dist_dir": ".",
			"includes": ["PIL.Image",
							"PIL.ImageOps"],
			"excludes": ["tkinter"]
			}
		},
    console = ["turbomeme.py"],
	zipfile = None,
)