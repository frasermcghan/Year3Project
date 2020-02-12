import os
from shutil import copy
import pandas as pd
from sklearn.model_selection import train_test_split


data_path = "/Users/fraser/Uni/Year 3/Project/code"

speed = []
files = []
labels = []

for afolder in os.listdir(f"{data_path}/data/"):
	if afolder != ".DS_Store":
		
		for aspeed in os.listdir(f"{data_path}/data/{afolder}/"):
			if aspeed != ".DS_Store":	

				for afile in os.listdir(f"{data_path}/data/{afolder}/{aspeed}"):
					if afile != ".DS_Store" and afile.endswith('.png'):
						speed.append(aspeed)
						files.append(afile)
						labels.append(afolder)

d = {'speed':speed, 'file':files, 'label':labels}
df = pd.DataFrame(data=d)


df_train, df_test = train_test_split(df, test_size=0.2)


for speed, file, label in zip(df_train['speed'], df_train['file'], df_train['label']):
	current_dir = f"{data_path}/data/{label}/{speed}/{file}"
	dest_dir = f"{data_path}/thermal_only/train/{label}/{file}"
	copy(current_dir, dest_dir)

for speed, file, label in zip(df_test['speed'], df_test['file'], df_test['label']):
	current_dir = f"{data_path}/data/{label}/{speed}/{file}"
	dest_dir = f"{data_path}/thermal_only/test/{label}/{file}"
	copy(current_dir, dest_dir)			
	