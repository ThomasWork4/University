import numpy as np
from mne.time_frequency import psd_multitaper

def order_channels(Data, Data2, Details=True):
    # List of frequency upper and lower bands which is looped through in the main part of our code
    Frequency_Band_Lower_Bound = [0.5, 4, 8, 12, 35]
    Frequency_Band_Upper_Bound = [4, 8, 12, 30, 45,]

    # Lists to store our results respective of their frequency band
    Channels_Delta = [] 
    Channels_Theta = []
    Channels_Alpha = []
    Channels_Beta = []
    Channels_Gamma = []

    # Loop through every channel that we have in our data as shown in the cell above
    for x in range(len(Data.ch_names)):
        if Data.ch_names[x] == 'T7':
            continue
        Differences = []
        
        # Loop through each freqency band 
        for i in range(len(Frequency_Band_Lower_Bound)):
            
            # Obtain the mean power spectral densities of a particular channel in a particular frequency band (based on the current loop)
            # FOR EYES OPEN
            psds, freqs = psd_multitaper(Data, fmin=Frequency_Band_Lower_Bound[i], fmax=Frequency_Band_Upper_Bound[i], n_jobs=1, picks=Data.ch_names[x])
            psds = 10 * np.log10(psds)  # convert to dB
            psds_mean = psds.mean(0).mean(0)

            # Obtain the mean power spectral densities of a particular channel in a particular frequency band (based on the current loop)
            # FOR EYES CLOSED
            psds2, freqs2 = psd_multitaper(Data2, fmin=Frequency_Band_Lower_Bound[i], fmax=Frequency_Band_Upper_Bound[i], n_jobs=1, picks=Data.ch_names[x])
            psds2 = 10 * np.log10(psds2)  # convert to dB
            psds_mean2 = psds2.mean(0).mean(0)
            
            # Subtract one list of psds from the other, to find the difference between the two 
            # Make sure to abs the each value, and large negative still indicate a large difference. 
            zip_object = zip(psds_mean, psds_mean2)
            for psds_mean_i, psds_mean2_i in zip_object:
                Differences.append((abs(psds_mean_i - psds_mean2_i))) 
            
            # Sort the list and find the first quartile and third quartile
            Sort = sorted(Differences)
            q1, q3 = np.percentile(Differences, [25, 75])
            # interquartile range = third - first quartile
            iqr = q3 - q1
            # if any value lies iqr * 1.5 outside of the first and third quartiles
            # it should be considered an outlier and removed
            lower_bound = q1 - (1.5 * iqr)
            upper_bound = q3 + (1.5 * iqr)
            for v in Differences:
                if v < lower_bound:
                    Differences.remove(v)
                elif v > upper_bound:
                    Differences.remove(v)
            
            # Calculate the average difference for the above list of differences
            Average_Difference = sum(Differences) / len(Differences)
            
            # Place the result in it's respective list based on whichever frequency band we are currently working on.
            if Details == True:
                if Frequency_Band_Lower_Bound[i] == 0.5:
                    Channels_Delta.append([Data.ch_names[x], 'Delta', Average_Difference])
                elif Frequency_Band_Lower_Bound[i] == 4:
                    Channels_Theta.append([Data.ch_names[x], 'Theta', Average_Difference])
                elif Frequency_Band_Lower_Bound[i] == 8:
                    Channels_Alpha.append([Data.ch_names[x], 'Alpha', Average_Difference])
                elif Frequency_Band_Lower_Bound[i] == 12:
                    Channels_Beta.append([Data.ch_names[x], 'Beta', Average_Difference])
                elif Frequency_Band_Lower_Bound[i] == 35:
                    Channels_Gamma.append([Data.ch_names[x], 'Gamma', Average_Difference])
            else:
                if Frequency_Band_Lower_Bound[i] == 0.5:
                    Channels_Delta.append(Data.ch_names[x])
                elif Frequency_Band_Lower_Bound[i] == 4:
                    Channels_Theta.append(Data.ch_names[x])
                elif Frequency_Band_Lower_Bound[i] == 8:
                    Channels_Alpha.append(Data.ch_names[x])
                elif Frequency_Band_Lower_Bound[i] == 12:
                    Channels_Beta.append(Data.ch_names[x])
                elif Frequency_Band_Lower_Bound[i] == 35:
                    Channels_Gamma.append(Data.ch_names[x])

    return Channels_Delta, Channels_Theta, Channels_Alpha, Channels_Beta, Channels_Gamma
        
