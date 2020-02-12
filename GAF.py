import matplotlib.pyplot as plt 
import pandas as pd 

from pyts.image import GramianAngularField

# Import time-series
bar_vib_path = "/Users/fraser/Uni/Year 3/Project/code/data/1bar/full_load/full_load_current_data_1bar_full_load.csv"
bar_vib = pd.read_csv(bar_vib_path)
bar_X = [bar_vib['# time'], bar_vib[' phase1']]

healthy_vib_path = "/Users/fraser/Uni/Year 3/Project/code/data/healthy/full_load/full_load_current_data_healthy_full_load.csv"
healthy_vib = pd.read_csv(healthy_vib_path)
healthy_X = [healthy_vib['# time'], healthy_vib[' phase1']]

# Transform the time series into Gramian Angular Fields
gasf = GramianAngularField(image_size=24, method='difference')

bar_X_gasf = gasf.fit_transform(bar_X)
healthy_X_gasf = gasf.fit_transform(healthy_X)

fig = plt.figure('Vibration')

ax1 = fig.add_subplot(1,2,1)
ax1.imshow(bar_X_gasf[1])
ax1.set_title('1bar')

ax2 = fig.add_subplot(1,2,2)
ax2.imshow(healthy_X_gasf[1])
ax2.set_title('healthy')


plt.show()


