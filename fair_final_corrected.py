
# loading the audio file in librosa

from natsort import natsorted
import os
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import librosa
import pandas as pd
import numpy as np
import shutil
from moviepy.editor import VideoFileClip, concatenate_videoclips
from multiprocessing import Process
import subprocess

# to convert mp4 to wav without asking the wav
# formatted file from the user
cwd = os.getcwd()
path = os.path.join(cwd, "media")
tmp = None
for filename in os.listdir(path):
    if (filename == "powerplay.mp4"):  # or .avi, .mpeg, whatever.
        tmp = os.path.join(path, filename)
        os.system(
            "ffmpeg -i {0} -ab 160k -ac 2 -ar 44100 -vn audio.wav".format(tmp))
    else:
        continue
if tmp == None:
    print('No video file found')
# one way transfer the generated .wav file to media folder
# rather delete the audio.wav after use (as done ahead(scroll down))

print("Upto this Good")

tmp = os.path.join(cwd, "audio.wav")
# filename = 'C:/Users/sroy8/OneDrive/Desktop/IEDC/audio.wav'
filename = tmp
x, sr = librosa.load(filename, sr=16000)
"""x = audio time series of the audio file, sr = sampling rate"""
# duration of the audio clip in minutes
int(librosa.get_duration(x, sr)/60)

# break the audio into chunks of 5 seconds
max_slice = 5
window_length = max_slice * sr

"""The sampling rate(sr) refers to the number of samples of audio recorded every second. 
It is measured in samples per second or Hertz"""

# compute the Short Time Energy for every chunk
energy = np.array([sum(abs(x[i:i+window_length]**2))
                  for i in range(0, len(x), window_length)])

# Let's consider the threshold to be 12,000 as it lies on the tail of the distribution (see the notebook)
df = pd.DataFrame(columns=['energy', 'start', 'end'])
thresh = 12000
row_index = 0
for i in range(len(energy)):
    value = energy[i]
    if(value >= thresh):
        i = np.where(energy == value)[0]
        df.loc[row_index, 'energy'] = value
        df.loc[row_index, 'start'] = i[0] * 5
        df.loc[row_index, 'end'] = (i[0]+1) * 5
        row_index = row_index + 1

# Merge consecutive time intervals of audio clips into one
temp = []
i, j = 0, 0
n = len(df) - 2
m = len(df) - 1
while(i <= n):
    j = i+1
    while(j <= m):
        if(df['end'][i] == df['start'][j]):
            df.loc[i, 'end'] = df.loc[j, 'end']
            temp.append(j)
            j = j+1
        else:
            i = j
            break
df.drop(temp, axis=0, inplace=True)


# Create temporary folder for storing subclips generated. This folder will be deleted later after highlights are generated.
cwd = os.getcwd()
sub_folder = os.path.join(cwd, "clips")
if os.path.exists(sub_folder):
    shutil.rmtree(sub_folder)
    os.mkdir(sub_folder)
else:
    os.mkdir(sub_folder)

# Extract the video within a particular time interval to form highlights
# Let's consider only five seconds post every excitement clip
start = np.array(df['start'])
end = np.array(df['end'])
for i in range(len(df)):
    if(i != 0):
        start_lim = start[i] - 5
    else:
        start_lim = start[i]
    end_lim = end[i]
    filename = "highlight" + str(i+1) + ".mp4"
    cwd = os.getcwd()
    link = os.path.join(cwd, "media/powerplay.mp4")
    ffmpeg_extract_subclip(link, start_lim, end_lim, targetname=filename)
    # move generated clips to a folder
    clip_source = os.path.join(cwd, filename)
    shutil.move(clip_source, sub_folder)

print('Upto this Better')

# remove the audio file:-
pathh = os.path.join(cwd, "audio.wav")
os.remove(pathh)  # removes the generated audio.wav file

# Merging:-

L = []


def func():
    for root, dirs, files in os.walk(sub_folder):
        # files.sort()
        files = natsorted(files)
        for file in files:
            if os.path.splitext(file)[1] == '.mp4':
                filePath = os.path.join(root, file)
                video = VideoFileClip(filePath)
                L.append(video)

    final_clip = concatenate_videoclips(L)
    # final_clip.to_videofile("output.mp4", fps=24, remove_temp=False)
    final_clip.to_videofile("output.mp4", fps=24, remove_temp=True)

# remove the clips folder
# shutil.rmtree(sub_folder)     #ERROR: Conflicts with running processes involving files of this directory


if __name__ == '__main__':
    converter = Process(target=func)
    converter.start()
    converter.join()  # Waits until the function has finished executed before continuing
    # the above line prevents conflict, error: process is still in use hence can't be deleted
    # courtesy: https://github.com/Zulko/moviepy/issues/810
    for files in os.listdir(sub_folder):
        f = os.path.join(sub_folder, files)
        os.remove(f)
    shutil.rmtree(sub_folder)
    """
    pathh = None
    pathh = os.path.join(cwd, "audio.wav")
    if pathh != None:
        os.remove(pathh)  # removes the generated audio.wav file
    """
    # moving output file to target:

    frm = os.path.join(cwd, "output.mp4")
    to = os.path.join(cwd, "target")
    shutil.move(frm, to)
    os.remove(frm)
