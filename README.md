Pythonlibs for Photon Therapy Analysis
========================================

Python 3 port of `phd_tools`. Scrapped old and long time unused functionality.

File organisation
-----------------

Files in the root are executable scripts, subdirectories are libraries and could be copied into your own projects or your `$PYTHONPATH`.

Why is this project not neatly separated and split over multiple task-specific repos? Because I am lazy, that's why. And also because just one `rsync` command is required to update all my tools on the clusters I use.

Usage
-----
Clone, and put the directory in your path (`export <CLONE_DIR>:$PATH`). You can get access to the libraries in any script by adding `export PYTHONPATH=<CLONE_DIR>:$PYTHONPATH` to your bashrc, or by putting this atop your scripts:

	import sys
	sys.path.append("<CLONE_DIR>")

Now, an incomplete list over the modules with a brief description:

MHD or ITK Images
-----------------

Provides a way to operate on images as outputted by Gate (and CLITK tools). Slicing, projections, mathematical operations, stuff like that. 

Plot
----

A set of function that ease life with Matplotlib. The Texify-function make them look good, and the tle.py functions provides many ways to compare data (depends on image). An older and unused and unmaintained rootplot component is kept around for the braindead.
