import pandas as pd
import os

"""
There's a much smarter way to do this, I just can't remember right now!
"""

# Get paths minus file extensions
dirs = []
for folders in os.listdir("meta"):
    for files in os.listdir("meta/" + folders):
        dirs.append(folders+"/"+files)

dirs = [s.replace('.xlsx', '') for s in dirs]
dirs = [s.replace('.csv', '') for s in dirs]

# loop through and merge my tables with Julie's
for path in dirs:
    if not os.path.isdir("joined/" + path.split("/")[0]):
        os.mkdir("joined/" + path.split("/")[0])
    if "Actors" in path:
        try:
            meta = pd.read_excel("meta/" + path + ".xlsx")
            data = pd.read_csv("out/" + path + ".csv", header=None)
            print(meta.columns)
            #meta.columns = map(str.lower, meta.columns)
            joined = pd.merge(data, meta, left_on=0, right_on="character", how="left")
            del joined["percentage"]
            del joined["character"]
            joined.columns = ["name", "percentage", "role", "author"]
            joined.to_csv("joined/" + path + "-joined-actors.csv", header=True, sep=",", index=False)
        except (FileNotFoundError,KeyError) as e:
            print(e)
            continue


    elif "Benefactors" in path:
        try:
            print(path)
            meta = pd.read_excel("meta/" + path + ".xlsx")
            data = pd.read_csv("out/" + path + ".csv", header=None)
            print(meta.columns)
            meta.columns = map(str.lower, meta.columns)
            joined = pd.merge(data, meta, left_on=0, right_on="character", how="left")
            del joined["percentage"]
            del joined["character"]
            joined.columns = ["name", "percentage", "role", "author"]
            joined.to_csv("joined/" + path + "-joined-benefactors.csv", header=True, sep=",", index=False)
        except (FileNotFoundError,KeyError) as e:
            print(e)
            continue

