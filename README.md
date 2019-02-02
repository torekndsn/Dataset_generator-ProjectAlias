# Dataset_generator-ProjectAlias
A few scripts to record and create training data for Project Alias

## Instructions
1. Use the sound-recorder.py to record 60 sec wav files.
the script takes one string paramater, which works at the name for the recording. The idea is record 60 sec samples of different settings and name them accordingly.
One example could be to make 3 recordings: Livingroom_causual_talk.wav, Livingroom_object_sounds.wav, tv_radio_sounds.wav.

2. Put all the .wav file into a folder called "recordings".

3. Launch the datacreater.py. It will take all .wav files in the "recordings" folder an process them through the same mfcc algorithm that Alias uses to create spectograms.
Remember that the FEED_DURATION value can be used to change the length of each spectogram in seconds. This should match the same duration in the Alias software.
After all wav files has been processed, the datacreater.py outputs two numpy arrays, one containing all the spectograms, being the training data. And another for corrosponding labels. 
This program is initially made to make background exampls, so all labels are '0'. It can be changed to '1' to label the recordings as wake-word examples. 

4. Load the files into the data folder in the Project Alias source code. The numpy arrays will be loaded in the ai.py line 37,38. 
Make sure to rename accordingly.
