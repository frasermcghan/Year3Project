# Year 3 Project
Code developed during 3rd year deep learning project.

## data_collection.py
Python script that establishes connection to an oscilloscope, a NIDAQ card, and a FLIR infrared camera - all of which are connected to the computer via USB.
After establishing a connection, the script will send commands to the equipment at given intervals to collect samples of data.
After each sample is collected, it is written to a local directory on the computer.

## Results.ipynb 
Jupyter Notebook containing results from experiments. Models were trained on Google Colab.