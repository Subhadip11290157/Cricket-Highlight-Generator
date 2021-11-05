import subprocess
import os
"""
command = "ffmpeg -i C:/Users/sroy8/OneDrive/Desktop/IEDC/test/powerplay.mp4 -ab 160k -ac 2 -ar 44100 -vn audio.wav"

subprocess.call(command, shell=True)
"""

path = 'C:/Users/sroy8/OneDrive/Desktop/IEDC/media/'
for filename in os.listdir(path):
    print(filename)
    if (filename == "powerplay.mp4"):  # or .avi, .mpeg, whatever.
        os.system(
            "ffmpeg -i {0} -ab 160k -ac 2 -ar 44100 -vn audio.wav".format(filename))
    else:
        continue
print('\n-----------------\n')
print(path)
