import os
import shutil

os.system('cmd /c "pyinstaller.exe'
          ' --name Minimal_Casting_Tool'
          ' --noconsole'
          ' -i=src/icon.ico'
          ' --add-data src;src'
          ' --add-data layout;layout'
          ' App.py"')
