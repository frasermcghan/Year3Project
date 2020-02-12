import pandas as pd
import os
from sklearn.model_selection import train_test_split

path = "/Users/fraser/Uni/Year 3/Project/code/data"

files = []
labels = []

for afolder in os.listdir(path):
    if afolder != ".DS_Store":
        for afile in os.listdir(f"{path}/{afolder}/"):
            files.append(f"{afolder}/{afile}")
            labels.append(afolder)


d = {'file':files, 'label':labels}
df = pd.DataFrame(data=d)

train, test = train_test_split(df, test_size=0.2)

train.to_csv("/Users/fraser/Uni/Year 3/Project/code/thermal_only/train/labels.csv", index=False)
test.to_csv("/Users/fraser/Uni/Year 3/Project/code/thermal_only/test/labels.csv", index=False)