import os
import shutil

cwd = os.getcwd()
sub_folder = os.path.join(cwd, "clips")
if os.path.exists(sub_folder):
    shutil.rmtree(sub_folder)
    os.mkdir(sub_folder)
else:
    os.mkdir(sub_folder)
