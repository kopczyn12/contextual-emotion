# BIOSIGNALS

## Description

This folder contains script to gather, plot and process ecg data from the examined user. If you want to start using it, install libraries from the *requirements.txt* <br>

## Scripts

**ecg_examination.py** - it is used to gather the ecg data using Aidmed device with 250 Hz sampling rate <br>
**plot_raw_ecg.py** - using matplotlib it's plotting raw gathered signal <br>
**processing_signals.py** - it is used to process raw signal and also plot the signal with detected R-Peaks <br>

## Usage
1. python3 **ecg_examination.py** *email of user that we want to record the ecg* *date of examination in format for example (2023_05_06)*<br>
2. python3 **plot_raw_ecg.py** *email of user we want to render the recorded ecg* *date of examination in format for example (2023_05_06)* <br>
3. python3 **processing_signals** *email of user that we want to process ecg, detect r-peaks and render it* *date of examination in format for example (2023_05_06)* <br>
4. python3 **review_database.py** *email of user that we want to list ecg examinations (dates)* <br>
