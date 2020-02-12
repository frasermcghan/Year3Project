import pandas as pd
from shutil import copy
import os

df_test = pd.read_csv("/Users/fraser/Uni/Year 3/Project/code/thermal_only/test/labels.csv")

for test_image_file, label in zip(df_test['file'], df_test['label']):
	if test_image_file.endswith('.png'):
		
		test_image_dir = f"/Users/fraser/Uni/Year 3/Project/code/thermal_only/{label}"
		test_image_path = f"/Users/fraser/Uni/Year 3/Project/code/thermal_only/{label}/{test_image_file}"
		
		df_test_dest = f"/Users/fraser/Uni/Year 3/Project/code/thermal_only/test/{label}/{test_image_file}"
		
		copy(test_image_path, df_test_dest)