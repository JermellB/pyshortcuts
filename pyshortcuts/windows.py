#!/usr/bin/env python
"""
Create desktop shortcuts for Windows
"""
from __future__ import print_function
import os
import sys

from .utils import get_homedir
from .shortcut import Shortcut


def get_exe_types():
    '''Return list of valid executable file extensions [.com, .exe, ...]'''
    exetypes = [ext.lower() for ext in os.environ['PATHEXT'].split(os.pathsep)]
    return exetypes

def make_shortcut(script, name=None, description=None, terminal=True,
                  folder=None, icon=None):
    """create windows shortcut

    Arguments
    ---------
    script      (str)  path to script to run.  This can include  command-line arguments
    name        (str or None) name to use for shortcut [defaults to script name]
    description (str or None) longer description of script [defaults to `name`]
    icon        (str or None) path to icon file [defaults to python icon]
    folder      (str or None) folder on Desktop to put shortcut [defaults to Desktop]
    terminal    (True or False) whether to run in a Terminal  [True]
    """
    from win32com.client import Dispatch

    scut = Shortcut(script, name=name, description=description,
                    folder=folder, icon=icon)

    homedir = get_homedir()

    pyexe = os.path.join(sys.prefix, 'pythonw.exe')
    if terminal:
        pyexe = os.path.join(sys.prefix, 'python.exe')

    # Check for other valid ways to run the script
    # try appending .exe if script itself not found
    if not os.path.exists(scut.full_script):
        tname = scut.full_script + '.exe'
        if os.path.exists(tname):
            pyexe = tname
            scut.full_script = ''

    # If script is already executable use it directly instead of via pyexe
    ext = os.path.splitext(scut.full_script)[1].lower()
    if  ext in get_exe_types():
        pyexe = scut.full_script
        scut.full_script = ''

    wscript = Dispatch('WScript.Shell').CreateShortCut(scut.target)
    wscript.Targetpath = '"%s"' % pyexe
    wscript.Arguments = '%s %s' % (scut.full_script, scut.args)
    wscript.WorkingDirectory = homedir
    wscript.WindowStyle = 0
    wscript.Description = scut.description
    wscript.IconLocation = scut.icon
    wscript.save()

    return scut
