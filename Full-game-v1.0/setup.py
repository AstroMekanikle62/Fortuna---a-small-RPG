import sys
import os
from cx_Freeze import setup, Executable
from Settings import *
base = None


if sys.platform == "win32":
    base = "Win32GUI"
exe=Executable(
     script="Main.py",
     base= base
     )
includefiles=["maps","dialogue","img","snd"]
includes=[]
excludes=['tcl','ttk','tkinter','Tkinter']
packages=["pygame"]
#os.environ['TCL_LIBRARY'] = r'C:\Program Files\Python36\tcl\tcl8.6'
#os.environ['TK_LIBRARY'] = r'C:\Program Files\Python36\tcl\tk8.6'
setup(

     version = "1.0",
     description = "No Description",
     author = "Jafar al hussain",
     name = "Fortuna",
     options = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}},
     executables = [exe]
     )