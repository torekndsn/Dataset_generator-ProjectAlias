import numpy as np
import scipy.io.wavfile as wav
import os

from python_speech_features import mfcc
from python_speech_features import logfbank
from python_speech_features import sigproc

RATE                = 16000
CHUNK_SAMPLES       = 1024
FEED_DURATION       = 1.5 # Duration of each sample in seconds 
FEED_LENGTH         = int(np.floor(RATE * FEED_DURATION / CHUNK_SAMPLES)) #number of chunks during the feed_duration
WIN_LEN             = 1/(RATE/CHUNK_SAMPLES) #IN SECONDS

row = 23
col = 13

soundFiles = os.listdir("recordings/")
print(soundFiles)

silence_threshhold = 700

# Divide the whole recording up into chunks with size of 1024
def divide_sound_file(data,chunk):
	for i in range(0,len(data), chunk): 
		yield data[i:i+chunk]


# Take the signal of 1,5 seconds and calculate mfcc. Return array. 
def return_mfcc(signal):
    new_signal = sigproc.preemphasis(np.asarray(signal), coeff=0.95)
    mfcc_feat = mfcc(new_signal, RATE, winlen=WIN_LEN, nfft=CHUNK_SAMPLES*2, winfunc=np.hamming)
    return mfcc_feat


# Iterate through signal chunks
def find_mic_triggers(signal):
    sampleStart = False
    all_samples = []

    # IF mic is triggered start calculating mfcc for the next 1,5 seconds and create a spectogram. 
    for i in range(len(signal)):
        if np.abs(signal[i]).mean() > silence_threshhold and not sampleStart:
            spectogram = []
            sampleStart = True

        if sampleStart:
            mfcc_from_chunk = return_mfcc(signal[i])
            spectogram.append(mfcc_from_chunk)

            # If 1,5 sec has run, store spectogram in array. 
            if len(spectogram) >= FEED_LENGTH:
                all_samples.append(spectogram)
                sampleStart = False
    return all_samples



# Main function 
def read_wav():
    TRAINING_DATA = np.empty([0, 1, row, col]) # XS Example array to be trained
    TRAINING_LABELS = np.empty([0, 2 ]) # YS Label array

    for file in soundFiles:
        if file.endswith('.wav'):
            print("file names:")
            print(file)
            #read the .wav file, store the signal, and divide into chunks 
            (rate,sig) = wav.read("recordings/"+file)
            new_sig = list(divide_sound_file(sig,CHUNK_SAMPLES))

            #Call function to mic trigger and mfcc
            samples_to_process = find_mic_triggers(np.asarray(new_sig))

            #turn the spectogram array into numphy and reshape to fit model 
            final_spectograms = np.asarray(samples_to_process)
            num_of_spec = len(final_spectograms)
            final_spectograms = np.reshape(final_spectograms,(num_of_spec,1,row,col))
            
            #Create training labels that match the data length
            labels = np.repeat(np.array([1., 0.])[None, :], num_of_spec, axis=0)
            print(final_spectograms.shape)
            print(labels.shape)

            TRAINING_LABELS = np.append(TRAINING_LABELS,labels,axis=0)
            TRAINING_DATA = np.append(TRAINING_DATA,final_spectograms,axis=0)

        else:
            print("not .wav file")
        #get name and save single file as numphy arrays with the right name 
        #sound_file_name = os.path.splitext(file)
        #np.save("training_examples/"+sound_file_name[0]+"_data", final_spectograms)
        #np.save("training_examples/"+sound_file_name[0]+"_labels", labels)
    print(TRAINING_LABELS.shape)
    print(TRAINING_DATA.shape)
    #Save as one file
    np.save("training_examples/background_sound_examples", TRAINING_DATA)
    np.save("training_examples/background_sound_labels", TRAINING_LABELS)

#Start program
read_wav()
