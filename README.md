# Year 3 Project
Code developed during 3rd year deep learning project.

## data_collection.py
Python script that establishes connection to an oscilloscope, a NIDAQ card, and a FLIR infrared camera - all of which are connected to the computer via USB.
After establishing a connection, the script will send commands to the equipment at given intervals to collect samples of data.
After each sample is collected, it is written to a local directory on the computer.

## Create Samples From Raw Data.ipynb
Jupyter Notebook that splits raw measurement into 120 samples (10s/sample), then saves each sample into a directory corresponding to the fault condition.

## GASF Vibration.ipynb
Creates a GASF image from each vibration sample. 
Splits the samples into training, validation, and test sets.

## GADF Vibration.ipynb
Creates a GADF image from each vibration sample. 
Splits the samples into training, validation, and test sets.

## GASF Current.ipynb
Creates a GASF image from each current sample. 
Splits the samples into training, validation, and test sets.

## GADF Current.ipynb
Creates a GADF image from each current sample. 
Splits the samples into training, validation, and test sets.

## Thermal.ipynb
Splits the thermal images samples into training, validation, and test sets.

## Results.ipynb 
Jupyter Notebook that contains results from experiments. Models were trained on Google Colab.
