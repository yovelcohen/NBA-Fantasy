import os
import glob
# export it to csv
import pandas as pd

os.chdir('/home/yovel/PycharmProjects/fantasy')
# The glob module generates lists of files matching given pattern.
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

# combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames], sort=False, axis=1)
combined_csv.to_csv("statsmerger.csv", index=True, encoding='utf-8-sig')
# without the encoding it won't export in english.

