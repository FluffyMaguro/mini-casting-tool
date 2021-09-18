"""
A script for compiling the app with nuitka

"""

import os
import shutil
from zipfile import ZIP_BZIP2, ZipFile

from App import VERSION

NAME = 'Minimal Casting Tool'

# Run nuitka
os.system('cmd /c "python -m nuitka'
          ' --plugin-enable=pyqt5'
          ' --standalone'
          ' --windows-disable-console'
          ' --windows-icon-from-ico=src/icon.ico'
          ' --include-data-dir=src=src'
          ' --include-data-dir=layout=layout'
          ' App.py')

shutil.move('App.dist', NAME)

# Zip
file_name = f"{NAME} ({VERSION}).zip"

to_zip = []
for root, directories, files in os.walk(NAME):
    for file in files:
        to_zip.append(os.path.join(root, file))

print('Compressing files...')
with ZipFile(file_name, 'w', compression=ZIP_BZIP2) as zip:
    for file in to_zip:
        zip.write(file)

# Cleanup
for item in [NAME]:
    if os.path.isdir(item):
        shutil.rmtree(item)
