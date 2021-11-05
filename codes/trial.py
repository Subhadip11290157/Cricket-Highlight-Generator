
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


filename = 'C:/Users/sroy8/OneDrive/Desktop/IEDC/media/powerplay.wav'
x, sr = librosa.load(filename, sr=16000)

# duration of the audio clip in minutes
int(librosa.get_duration(x, sr)/60)

# break the audio into chunks of 5 seconds
max_slice = 5
window_length = max_slice * sr

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
i = 0
j = 0
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
sub_folder = os.path.join(cwd, "Subclips")
if os.path.exists(sub_folder):
    shutil.rmtree(sub_folder)
    path = os.mkdir(sub_folder)
else:
    path = os.mkdir(sub_folder)


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
    ffmpeg_extract_subclip("C:/Users/sroy8/OneDrive/Desktop/IEDC/media/powerplay.mp4", start_lim,
                           end_lim, targetname=filename)

# Merging:-


L = []

for root, dirs, files in os.walk("C:/Users/sroy8/OneDrive/Desktop/IEDC/test"):

    # files.sort()
    files = natsorted(files)
    for file in files:
        if os.path.splitext(file)[1] == '.mp4':
            filePath = os.path.join(root, file)
            video = VideoFileClip(filePath)
            L.append(video)

final_clip = concatenate_videoclips(L)
final_clip.to_videofile("output.mp4", fps=24, remove_temp=False)