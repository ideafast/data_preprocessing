# Exploratory Data Analysis (EDA)

EDA to examine datafiles for each manufacturer. 

## Vitals file:

1. File format is ‘timestamp’ + ‘patch id’ + ‘vitals or ECG’ 


## Initial set up for VitalPatch

1. You need python version 3.7: sudo apt install python3.7
2. Go to vitalPatch folder directory by terminal/ command window
3. Within the same folder location create 2 additional folders called ‘input and ‘output’
4. Within the ‘input’ folder place all the raw csv files from the data platform.
5. Be sure you are in the vitalPatch directory again
6. Run the script: pip install glob3
7. Run the script: python process_files.py
8. Once you have run the script go to the directory on your PC where you created the ‘output’ folder. Within
this folder you will find the combined raw data csv files for combined vitals and combined ECG (ie
VC2D008CF_00DF4C_vitals.csv)


## Initial set up for Axivity

1. You need R for running the process file.
2. Install RStudio: https://www.statmethods.net/r-tutorial/index.html
3. Go to axivity folder directory.
4. Within the same folder location create 2 additional folders called 'input' and 'output'.
5. Within the ‘input’ folder place all the raw file as a cwa format.
6. Be sure you are in the axivity directory again.
7. Run the process-Axivity-File.R file by using RStudio.
8. You shuld install (GGIR) package: install.packages("GGIR")
9. Note: Be sure the datadir and outputdir have been adjusted inside the process-Axivity-File.R.
10. The outputs produced will contain several files including illustrations for presenting the wearing and sleeping patterns and csv files summarising such patterns.
