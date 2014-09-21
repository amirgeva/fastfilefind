fastfilefind
============

Disk indexing and search utility
--------------------------------

This utility allows a fast search for files based on the meta-information:
* Name
* Extension
* Size
* Date
  
The original purpose was to allow to easily answer a queries such as:
  `Where is the .cpp file I edited last week?`
  `Where is the IMG* file that is larger than 1Mb?`
  
The utility works by building a database of files, using the fffbuild.py script
This script can either be run manually, or better yet, run as
a scheduled task (probably once a day).  Typical run time for indexing is around 
30 - 180 seconds, depending on machine and number of files.

The fffsearch.py opens a GUI for searching.  For fast access, setting up a keyboard
shortcut that starts this GUI is best.
The fields are relatively self explanatory.
Double clicking a result runs (opens) it.
