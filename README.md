# LcTerminalPdb
TerminalPdb class modification to better handle list comprehensions at breakpoints

Problem:
LcTerminalPdb updates the default() method from TerminalPdb (which uses Pdb's
method). default() is called when code is run from the prompt, and uses exec()
to evaluate the code with the frame's local and global variables. When this code
is a list comprehension (or other closure) that requires local variables to be
bound, exec() fails with a NameError. This is because closures using exec() can
apparently only access globals.

Solution:
Here, when a NameError occurs, LcTerminalPdb.default attempts to rerun the code,
but by first updating the global dictionary passed to exec to include all the
local variables. The dictionary is first copied to avoid any weird updates to
frame globals, and the code is written such that processing of any other
commands happens as normal.

Requirements:
This assumes ipython is installed, as it extends TerminalPdb, but I believe that
comes with most python distributions. Nevertheless, the code could be changed to
inherit from Pdb directly, but using TerminalPdb adds nice things
like autocompletion to your debugging session, so why wouldn't you use it?

Implementing:
NOTE: In all cases, you must make sure that LcTerminalPdb is in your Python path
1) To directly use this class in code:

import LcTerminalPdb

<your code>
LcTerminalPdb.set_trace() # code will break into the debugger here

2) To use this class with the breakpoint() built-in function, change the
environment variable PYTHONBREAKPOINT to point to this class's set_trace.
Specifically, before running code (in a *nix terminal):

> export PYTHONBREAKPOINT=LcTerminalPdb.set_trace

Or, in Python directly (either in your code before it reaches a breakpoint or
from the prompt before you run your code):

import os
os.environ['PYTHONBREAKPOINT'] = 'LcTerminalPdb.set_trace

Then in your code:

<your code>
breakpoint() # code will break into the debugger here
