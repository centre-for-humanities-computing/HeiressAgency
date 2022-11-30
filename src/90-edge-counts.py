import os, csv
from collections import Counter
from tqdm import tqdm


dirs = []
for folder in os.listdir('corpus'):
    if folder.endswith('-chapters'):
        dirs.append('corpus/' + folder + '/')

for path in tqdm(dirs):
    # read in the csv edge list
    edge_tuples = []
    with open(path + 'CORRECTED.actor-benefactor-edge-list.csv', 'r') as csvfile:
        srlreader = csv.reader(csvfile, delimiter=',')

        for row in srlreader:
            edge_tuples.append(row)

    # get edge counts
    d = Counter(tuple(e) for e in edge_tuples)

    edge_counts = d.most_common()

    with open(path + 'edge-counts.csv', 'w') as write_file:

        csvwriter = csv.writer(write_file, delimiter=',',quoting=csv.QUOTE_MINIMAL)

        for item in edge_counts:
            csvwriter.writerow([list(item[0])[0], list(item[0])[1], item[1]])
