import subprocess
import os
"""
command = "ffmpeg -i C:/Users/sroy8/OneDrive/Desktop/IEDC/test/powerplay.mp4 -ab 160k -ac 2 -ar 44100 -vn audio.wav"

subprocess.call(command, shell=True)
"""

# mp4 to wav

path = 'C:/Users/sroy8/OneDrive/Desktop/IEDC/media/'
for filename in os.listdir(path):
    if (filename == "powerplay.mp4"):  # or .avi, .mpeg, whatever.
        tmp = os.path.join(path, filename)
        os.system(
            "ffmpeg -i {0} -ab 160k -ac 2 -ar 44100 -vn audio.wav".format(tmp))
    else:
        continue
