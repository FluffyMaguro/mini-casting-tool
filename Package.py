import os
import shutil

os.system(
    'cmd /c "pyinstaller.exe'
    ' --noconsole'
    #   ' -i=src/OverlayIcon.ico'
    #   ' --add-data venv\Lib\site-packages\s2protocol;s2protocol'
    #   ' --add-data src;src'
    #   ' --add-data SCOFunctions\SC2Dictionaries\*.csv;SCOFunctions\SC2Dictionaries'
    #   ' --add-data SCOFunctions\SC2Dictionaries\*.txt;SCOFunctions\SC2Dictionaries'
    ' App.py"')

shutil.move('dist/App.exe', 'App.exe')

for item in ('build', 'dist'):
    shutil.rmtree(item)
