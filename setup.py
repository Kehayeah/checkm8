import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
additional_modules = []

build_exe_options = {"includes": additional_modules,
                     "optimize": 2,
                     "packages": ["sys", "requests", "re", "json", "xlrd", "xlwt", "os", "PyQt5"],
                     "include_files": ['view.qml']}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="Check M8",
      version="0.1",
      description="Job Tools For Lazy Boys",
      options={"build_exe": build_exe_options},
      executables=[Executable(script="checkm8.py", base=base)])
