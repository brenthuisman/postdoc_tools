Pythonlibs for Particle/Photon Therapy Analysis
===============================================

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

Image
-----

Supports r/w MetoImage (MHD,ITK) and r/w AVSField (.xdr) images. A thin wrapper around typed numpy array objects (the `imdata` member) such that you can easily work with images in these data formats. Slicing, projections, mathematical operations, stuff like that is very easy with numpy, so you can easily extend things to what you need.

Plot
----

A set of function that ease life with Matplotlib. Makes heavy use of Seaborn. The optional Texify-function make them look good TeX-y, and the tle.py functions provides many ways to compare data (depends on image).

Geo
---

Some (spatial) vector functions. In particular, a function to convert Euler angles to matrix angles.

Mac
---

Operate on Gate macro files. Also with extremely basic support for the conversion of a phantom macro to an Image, which you may save to .mhx or .xdr. Requires CLITK tools

RTPlan
---

Some tools for processing dumped RTplans for Gate.

NKI
---

Some custom tools for my postdoc work. Unlikely to be interesting to you.
