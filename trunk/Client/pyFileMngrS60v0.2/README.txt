
pyFileManager for S60

Copyright 2005 - 2006 by Lasse Huovinen

Contents
    1. Introduction
    2. Usage
    3. Release Notes
    4. ToDo List
    5. List of Files


1. Introduction

pyFileManager for S60 is a powerful file manager for Symbian S60 phones written in Python.

2. Usage

See build-in help (or file pyfilemans60help.txt).

3. Release Notes
0.2	   February 14, 2006
Official Symbian UID 0x10279730 assigned for pyFileManager for S60. New features: displaying of current directory, refreshing current directory, screen size switching, and jumping to top, middle or bottom of current listing. Some error case handling bugs fixed. Optimizations and enchancements to the code. Minor improvements to the documentation. This version works with PyS60 1.3.1 and later.
0.1.0	   March 8, 2005.
This is the initial release. In addition to basic operations, the file manager contains already quite a few useful features.

4. ToDo List
- Bookmarks
- Recursive directory removal.
- Save the 'find' results.
- Open the text documents using pyEditS60 if installed.
- Send a file via FTP / Email.

5. List of Files

The pyFileManager for S60 consist of the following files.

Python source files:
- pyFileManager.py		The main program of pyFileManager for S60.
- default.py			Used to launch the editor in the case it is
				run as a standalone application.

Text files:
- pyfilemans60about.txt		Content for the 'About' menu item.
- pyfilemans60help.txt		Content for the 'Help' menu item.
- README.txt			This file.
