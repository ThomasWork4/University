import os
import numpy as np
import mne
from mne.preprocessing import (ICA, create_eog_epochs, create_ecg_epochs,corrmap)

def Start_And_Finish_Markers(raw):
    # Add the times of all stopping criterias for each experimental event to a list 
    Stopping_Criteras = []

    # Some EEG systems generate files where events are sorted in a seperate data array rather than pulses on STIM channels
    # Usualy this is stored in the .set file. When reading these files, Python converts the events to annotations.
    # The code below converts the annotations read from the raw signal data to an event array
    events_from_annot, event_dict = mne.events_from_annotations(raw)
    for i in events_from_annot:
        if i[2] == 1:
            Stopping_Criteras.append(i[0] / 500)


    #Sampling rate is 500 (There are approximately 500 samples per second)
    #To convert event sample time to seconds we can do Time in seconds = Sample time of event / Sample frequency
    #For our first first eyes closed event at 89602 
    #We can calculate that it is around 89602 / 500 = 179.204 seconds 
    #Cross referencing this with our graph, we can see that it's approximately correct
    # Another example, our first warm water emersion 332564 / 500 = 665.128 seconds (again looks correct from our graph)
    sfreq = raw.info['sfreq']


    # We need to find the time at which each experimental event starts and finishes, so we can crop it from our raw data 
    # We loop through the event array, and using the event_id, lookup the equivalent EEG marker from the event dictionary. 
    # Then we can cross reference it, with the list provided to find which experimental event it falls under i.e. is the current
    # event warm water emersion? or is it sound stimuli? etc 
    # Once we have: 1. EyesOpenStart 2. EyesClosedStart, 3. WarmWaterStart, 4. WarmWaterEnd, 5. HotWaterStart, 6. HotwaterEnd, 
    # 7. SoundStart, 8. SoundEnd, 9. EyesOpenEnd, 10. EyesClosedEnd
    # We can then calculate the time in the experiment at which they happened using Sample time of event / 500
    WarmWaterStart = None
    WarmWaterEnd = None
    HotWaterStart = None
    HotwaterEnd = None
    SoundStimuliStart = None
    SoundStimuliEnd = None

    for current_event in events_from_annot:
        # Cycle through our event dictionary and find the corresponding EEG marker to depict which experimental event 
        # We are currently looking at
        experimental_event = float(dict((new_val, new_k) for new_k, new_val in event_dict.items()).get(current_event[2]))

    
        # Eyes opening and closing don't need a start and finish time as the act uses only one event to represent it 
        if experimental_event == 5:
            EyesOpenStart = current_event[0] / sfreq
        elif experimental_event == 4:
            EyesClosedStart = current_event[0] / sfreq
        elif experimental_event == 7:
            EyesOpenEnd = current_event[0] / sfreq
        elif experimental_event == 6:
            EyesClosedEnd = current_event[0] / sfreq
        
        # If the event is Hot water emersion and its the first occurence, then set it to our Hot water emersion start time 
        # Otherwise, keep looping through each event and changing our Hot water emersion end time until we have iterated over
        # our final Hot water event
        elif experimental_event > 10 and experimental_event < 41:
            if HotWaterStart == None:
                HotWaterStart = current_event[0] / sfreq
            else:
                HotwaterEnd = current_event[0] / sfreq
        
        # If the event is warm water emersion and its the first occurence, then set it to our warm water emersion start time 
        # Otherwise, keep looping through each event and changing our warm water emersion end time until we have iterated over
        # our final warm water event
        elif experimental_event > 40 and experimental_event < 71:
            if WarmWaterStart == None:
                WarmWaterStart = current_event[0] / sfreq
            else:
                WarmWaterEnd = current_event[0] / sfreq
        
        # Same as above with our sound stimuli events
        elif experimental_event > 70 and experimental_event < 96:
            if SoundStimuliStart == None:
                SoundStimuliStart = current_event[0] / sfreq
            else:
                SoundStimuliEnd = current_event[0] / sfreq

    Order = {'EyesOpenStart': EyesOpenStart,'EyesClosedStart':EyesClosedStart,'EyesOpenEnd': EyesOpenEnd,'EyesClosedEnd': EyesClosedEnd,'HotWaterStart': HotWaterStart,'WarmWaterStart': WarmWaterStart,'SoundStimuliStart': SoundStimuliStart}
    Order = dict(sorted(Order.items(), key=lambda item: item[1]))
    keys = list(Order.keys())
    for i in range(len(keys)):
        if keys[i] == 'EyesOpenStart':
            EyesOpenStartFin = Stopping_Criteras[i]
        elif keys[i] == 'EyesClosedStart':
            EyesClosedStartFin = Stopping_Criteras[i]
        elif keys[i] == 'EyesOpenEnd':
            EyesOpenEndFin = Stopping_Criteras[i]
        elif keys[i] == 'EyesClosedEnd':
            EyesClosedEndFin = Stopping_Criteras[i]
        

    return WarmWaterStart, WarmWaterEnd, HotWaterStart, HotwaterEnd, SoundStimuliStart, SoundStimuliEnd, EyesOpenStart, EyesOpenStartFin, EyesClosedStart, EyesClosedStartFin, EyesOpenEnd, EyesOpenEndFin, EyesClosedEnd, EyesClosedEndFin

