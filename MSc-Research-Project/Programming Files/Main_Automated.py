import os
import numpy as np
import pandas as pd
import mne
from mne.decoding import SPoC
from mne.preprocessing import (ICA, create_eog_epochs, create_ecg_epochs,corrmap)
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from mne.time_frequency import psd_multitaper, tfr_multitaper, tfr_morlet
import warnings
from sklearn.model_selection import ShuffleSplit
from mne.preprocessing import Xdawn
from operator import itemgetter
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import KFold, cross_val_predict
from mne.decoding import CSP, cross_val_multiscore
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
from Channel_Selector import order_channels
from Start_And_Finish_Markers import Start_And_Finish_Markers
from pyriemann.estimation import Covariances
from pyriemann.tangentspace import TangentSpace
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

Dataset = ["3TM_01-100.set","4EB_01-100.set","5LL_01-100.set","6DJ_01-100.set","7IG_01-100.set","8ES_01-100.set","10OS_01-100.set","11TP_01-100.set","12JM_merg_01-100.set","13MT_01-100.set","14JR_01-100.set","15DM_01-100.set","16ET_01-100.set","17RP_01-100.set","18EB_01-100.set","19HB_01-100.set","20JC_01-100.set","22NL_01-100.set","23HH_2_01-100.set","24AH_01-100.set","25DE_01-100.set","27KA_01-100.set","28KC_01-100.set","29BE_01-100.set","30CK_01-100.set","31JV_01-100.set","32AC_01-100.set","33IG_01-100.set","34GL_01-100.set","35JH_01-100.set","36MS_01-100.set","37DG_01-100.set","38JC_01-100.set","39MF_01-100.set","40SL_01-100.set","41IA_01-100.set"]
Artifacts_For_Removal = [[2,3],[2,3,4,8],[5, 9, 10],"Skip",[1, 2],"Skip",[1, 3],[1],"Skip",[0, 2, 3],[0, 2],[2, 4],[0, 1],[0, 1, 2],[0,3,4],[0,1,5],[0,2,4,5],[0, 1, 2],"Skip","Skip",[1, 3, 4],[0, 1, 2],[],"Skip",[0, 1, 2, 3],[4],[0, 1],[0, 1, 2],[0, 1, 2],[],[0, 1, 2],[],[1,2],[1],[0,1],[]]
print(len(Dataset))
print(len(Artifacts_For_Removal))
EO_Accuracies = []
WW_Accuracies = []
Skips = [3,5,8,18,19,23]
for h in range(len(Dataset)):
    if h in Skips:
        continue
    # Load a sample of the folder 
    #(fdt files are detected and read automatically when .set is inferenced)
    sample_data_raw_file = Dataset[h]
    raw = mne.io.read_raw_eeglab(sample_data_raw_file)
    
    # Filter slow drifts. Removing low-frequency drifts can negatively affect quality of an ICA fit
    filt_raw = raw.load_data().copy().filter(l_freq=1., h_freq=None)

    ica = ICA(n_components=30, max_iter='auto', random_state=97)
    ica.fit(filt_raw)

    ica.exclude = Artifacts_For_Removal[h]

    raw.drop_channels(["PO5", "M2", "PO6"])

    WarmWaterStart, WarmWaterEnd, HotWaterStart, HotwaterEnd, SoundStimuliStart, SoundStimuliEnd, EyesOpenStart, EyesOpenStartFin, EyesClosedStart, EyesClosedStartFin, EyesOpenEnd, EyesOpenEndFin, EyesClosedEnd, EyesClosedEndFin = Start_And_Finish_Markers(raw)

    # Cropping our experimental events based on the first and last event times 
    WarmWaterEmersion = raw.copy().crop(tmin=WarmWaterStart, tmax=WarmWaterEnd)
    SoundStimuli = raw.copy().crop(tmin=SoundStimuliStart, tmax=SoundStimuliEnd)
    HotWaterEmersion = raw.copy().crop(tmin=HotWaterStart, tmax=HotwaterEnd)
    EyesOpenStart = raw.copy().crop(tmin=EyesOpenStart, tmax=EyesOpenStartFin)
    EyesClosedStart = raw.copy().crop(tmin=EyesClosedStart, tmax=EyesClosedStartFin)
    EyesOpenEnd = raw.copy().crop(tmin=EyesOpenEnd, tmax=EyesOpenEndFin)
    EyesClosedEnd = raw.copy().crop(tmin=EyesClosedEnd, tmax=EyesClosedEndFin)

    HW_Epochs = mne.make_fixed_length_epochs(HotWaterEmersion, duration=10, preload=True)
    WW_Epochs = mne.make_fixed_length_epochs(WarmWaterEmersion, duration=10, preload=True)
    SS_Epochs = mne.make_fixed_length_epochs(SoundStimuli, duration=10, preload=True)
    EO_Start_Epochs = mne.make_fixed_length_epochs(EyesOpenStart, duration=10, preload=True)
    EC_Start_Epochs = mne.make_fixed_length_epochs(EyesClosedStart, duration=10, preload=True)
    EO_End_Epochs = mne.make_fixed_length_epochs(EyesOpenEnd, duration=10, preload=True)
    EC_End_Epochs = mne.make_fixed_length_epochs(EyesClosedEnd, duration=10, preload=True)

    # Our end goal here is a numpy array that is trials x channels x frequencies 
    # So we loop through our conditions, then loop through each trial in each 
    # Condition. Then we calculate the psds for that trial in the form (channels x frequencies)
    # Then we concatenate a label to the end so we can keep track of where it comes
    # from. Then we add it to our global list. 
    Conditions = [[EO_Start_Epochs, EC_Start_Epochs], [HW_Epochs, WW_Epochs]]

    Condition_Counter = 0
    for EE in Conditions:
        Global_List_Of_Data_Delta = []
        Global_List_Of_Data_Theta = []
        Global_List_Of_Data_Alpha = []
        Global_List_Of_Data_Beta = []
        Global_List_Of_Data_Gamma = []
        for condition in EE:
            for trial_number in range(len(condition)):
                psds_Delta, freqs_Delta = psd_multitaper(condition[trial_number], fmin=0.5, fmax=4, n_jobs=1)
                psds_Theta, freqs_Theta = psd_multitaper(condition[trial_number], fmin=4, fmax=8, n_jobs=1)
                psds_Alpha, freqs_Alpha = psd_multitaper(condition[trial_number], fmin=8, fmax=12, n_jobs=1)
                psds_Beta, freqs_Beta = psd_multitaper(condition[trial_number], fmin=12, fmax=30, n_jobs=1)
                psds_Gamma, freqs_Gamma = psd_multitaper(condition[trial_number], fmin=35, fmax=45, n_jobs=1)
                Current_Delta = list(psds_Delta[0])
                Current_Theta = list(psds_Theta[0])
                Current_Alpha = list(psds_Alpha[0])
                Current_Beta = list(psds_Beta[0])
                Current_Gamma = list(psds_Gamma[0])
                if condition == HW_Epochs:
                    Current_Delta.append(0)
                    Current_Theta.append(0)
                    Current_Alpha.append(0)
                    Current_Beta.append(0)
                    Current_Gamma.append(0)
                elif condition == WW_Epochs:
                    Current_Delta.append(1)
                    Current_Theta.append(1)
                    Current_Alpha.append(1)
                    Current_Beta.append(1)
                    Current_Gamma.append(1)
                elif condition == EO_Start_Epochs:
                    Current_Delta.append(2)
                    Current_Theta.append(2)
                    Current_Alpha.append(2)
                    Current_Beta.append(2)
                    Current_Gamma.append(2)
                elif condition == EC_Start_Epochs:
                    Current_Delta.append(3)
                    Current_Theta.append(3)
                    Current_Alpha.append(3)
                    Current_Beta.append(3)
                    Current_Gamma.append(3)
                elif condition == SS_Epochs:
                    Current_Delta.append(4)
                    Current_Theta.append(4)
                    Current_Alpha.append(4)
                    Current_Beta.append(4)
                    Current_Gamma.append(4)
                elif condition == EO_End_Epochs:
                    Current_Delta.append(5)
                    Current_Theta.append(5)
                    Current_Alpha.append(5)
                    Current_Beta.append(5)
                    Current_Gamma.append(5)
                elif condition == EC_End_Epochs:
                    Current_Delta.append(6)
                    Current_Theta.append(6)
                    Current_Alpha.append(6)
                    Current_Beta.append(6)
                    Current_Gamma.append(6)
                Global_List_Of_Data_Delta.append(Current_Delta)
                Global_List_Of_Data_Theta.append(Current_Theta)
                Global_List_Of_Data_Alpha.append(Current_Alpha)
                Global_List_Of_Data_Beta.append(Current_Beta)
                Global_List_Of_Data_Gamma.append(Current_Gamma)

    
        np.random.shuffle(Global_List_Of_Data_Delta)
        np.random.shuffle(Global_List_Of_Data_Theta)
        np.random.shuffle(Global_List_Of_Data_Alpha)
        np.random.shuffle(Global_List_Of_Data_Beta)
        np.random.shuffle(Global_List_Of_Data_Gamma)
        Labels_Delta = []
        Labels_Theta = []
        Labels_Alpha = []
        Labels_Beta = []
        Labels_Gamma = []

        for i in range(len(Global_List_Of_Data_Delta)):
            Labels_Delta.append(Global_List_Of_Data_Delta[i][-1])
            Global_List_Of_Data_Delta[i] = Global_List_Of_Data_Delta[i][:-1]

        for i in range(len(Global_List_Of_Data_Theta)):
            Labels_Theta.append(Global_List_Of_Data_Theta[i][-1])
            Global_List_Of_Data_Theta[i] = Global_List_Of_Data_Theta[i][:-1]

        for i in range(len(Global_List_Of_Data_Alpha)):
            Labels_Alpha.append(Global_List_Of_Data_Alpha[i][-1])
            Global_List_Of_Data_Alpha[i] = Global_List_Of_Data_Alpha[i][:-1]

        for i in range(len(Global_List_Of_Data_Beta)):
            Labels_Beta.append(Global_List_Of_Data_Beta[i][-1])
            Global_List_Of_Data_Beta[i] = Global_List_Of_Data_Beta[i][:-1]
            
        for i in range(len(Global_List_Of_Data_Gamma)):
            Labels_Gamma.append(Global_List_Of_Data_Gamma[i][-1])
            Global_List_Of_Data_Gamma[i] = Global_List_Of_Data_Gamma[i][:-1]

        X_Delta = np.asarray(Global_List_Of_Data_Delta)
        y_Delta = np.asarray(Labels_Delta)

        X_Theta = np.asarray(Global_List_Of_Data_Theta)
        y_Theta = np.asarray(Labels_Theta)

        X_Alpha = np.asarray(Global_List_Of_Data_Alpha)
        y_Alpha = np.asarray(Labels_Alpha)

        X_Beta = np.asarray(Global_List_Of_Data_Beta)
        y_Beta = np.asarray(Labels_Beta)
        
        X_Gamma = np.asarray(Global_List_Of_Data_Gamma)
        y_Gamma = np.asarray(Labels_Gamma)

        Global_Data_List = [(X_Delta, y_Delta),(X_Theta, y_Theta),(X_Alpha, y_Alpha),(X_Beta, y_Beta),(X_Gamma, y_Gamma)]
        Delta_Results = []
        Theta_Results = []
        Alpha_Results = []
        Beta_Results = []
        Gamma_Results = []
        
        Secondary_Counter = 0
        for data in Global_Data_List:
            # CSPS
            clf = SVC(kernel='linear') # Linear Kernel
            csp = CSP(n_components=4)
            classifier_pipeline_CSP = make_pipeline(csp,clf)
            cv = StratifiedKFold(n_splits=10, shuffle=True)
            scores_CSP = cross_val_score(classifier_pipeline_CSP, data[0], data[1], cv=cv)
            CSP_Accuracy = np.mean(scores_CSP)

            #RIE
            clf = SVC(kernel='linear') # Linear Kernel
            covest = Covariances('oas')
            ts = TangentSpace()
            cv = StratifiedKFold(n_splits=10, shuffle=True)
            classifier_pipeline_Riemannian = make_pipeline(covest, ts, clf)
            scores_RIE = cross_val_score(classifier_pipeline_Riemannian, data[0], data[1], cv=cv)
            RIE_Accuracy = np.mean(scores_RIE)

            #SPoC
            clf = SVC(kernel='linear') # Linear Kernel
            spoc = SPoC()
            classifier_pipeline_spoc = make_pipeline(spoc, clf)
            cv = KFold(n_splits=2, shuffle=False)
            y_preds_spoc = cross_val_predict(classifier_pipeline_spoc, data[0], data[1], cv=cv)
            counter = 0
            for i in range(len(data[1])):
                if data[1][i] == y_preds_spoc[i]:
                    counter+=1 
            SPoC_Accuracy = counter / len(data[1])

            #print(round(CSP_Accuracy, 3), round(RIE_Accuracy, 3),round(SPoC_Accuracy, 3))

            if Secondary_Counter == 0:
                Delta_Results.append(["Delta", round(CSP_Accuracy, 3), round(RIE_Accuracy, 3), round(SPoC_Accuracy, 3)])
            if Secondary_Counter == 1:
                Theta_Results.append(["Theta", round(CSP_Accuracy, 3), round(RIE_Accuracy, 3), round(SPoC_Accuracy, 3)])
            if Secondary_Counter == 2:
                Alpha_Results.append(["Alpha", round(CSP_Accuracy, 3), round(RIE_Accuracy, 3), round(SPoC_Accuracy, 3)])
            if Secondary_Counter == 3:
                Beta_Results.append(["Beta", round(CSP_Accuracy, 3), round(RIE_Accuracy, 3), round(SPoC_Accuracy, 3)])
            if Secondary_Counter == 4:
                Gamma_Results.append(["Gamma", round(CSP_Accuracy, 3), round(RIE_Accuracy, 3), round(SPoC_Accuracy, 3)])

            Secondary_Counter +=1

        if Condition_Counter == 0:
            EO_Accuracies.append(Delta_Results[0])
            EO_Accuracies.append(Theta_Results[0])
            EO_Accuracies.append(Alpha_Results[0])
            EO_Accuracies.append(Beta_Results[0])
            EO_Accuracies.append(Gamma_Results[0])
            Condition_Counter += 1
        else:
            WW_Accuracies.append(Delta_Results[0])
            WW_Accuracies.append(Theta_Results[0])
            WW_Accuracies.append(Alpha_Results[0])
            WW_Accuracies.append(Beta_Results[0])
            WW_Accuracies.append(Gamma_Results[0])


with open('Results_EO_Delta.txt', 'w') as fp:
    for item in EO_Accuracies:
        if item[0] == "Delta":
            fp.write("%s\n" % item)
        else:
            continue
    print("Done")

with open('Results_EO_Theta.txt', 'w') as fp:
    for item in EO_Accuracies:
        if item[0] == "Theta":
            fp.write("%s\n" % item)
        else:
            continue
    print("Done")

with open('Results_EO_Alpha.txt', 'w') as fp:
    for item in EO_Accuracies:
        if item[0] == "Alpha":
            fp.write("%s\n" % item)
        else:
            continue
    print("Done")

with open('Results_EO_Beta.txt', 'w') as fp:
    for item in EO_Accuracies:
        if item[0] == "Beta":
            fp.write("%s\n" % item)
        else:
            continue
    print("Done")

with open('Results_EO_Gamma.txt', 'w') as fp:
    for item in EO_Accuracies:
        if item[0] == "Gamma":
            fp.write("%s\n" % item)
        else:
            continue
    print("Done")

with open('Results_WW_Delta.txt', 'w') as fp:
    for item in WW_Accuracies:
        if item[0] == "Delta":
            fp.write("%s\n" % item)
        else:
            continue
    print("Done")

with open('Results_WW_Theta.txt', 'w') as fp:
    for item in WW_Accuracies:
        if item[0] == "Theta":
            fp.write("%s\n" % item)
        else:
            continue
    print("Done")

with open('Results_WW_Alpha.txt', 'w') as fp:
    for item in WW_Accuracies:
        if item[0] == "Alpha":
            fp.write("%s\n" % item)
        else:
            continue
    print("Done")

with open('Results_WW_Beta.txt', 'w') as fp:
    for item in WW_Accuracies:
        if item[0] == "Beta":
            fp.write("%s\n" % item)
        else:
            continue
    print("Done")

with open('Results_WW_Gamma.txt', 'w') as fp:
    for item in WW_Accuracies:
        if item[0] == "Gamma":
            fp.write("%s\n" % item)
        else:
            continue
    print("Done")


                
