import os, csv
from collections import Counter
from tqdm import tqdm

dirs = []
for folder in os.listdir('corpus'):
    if folder.endswith('-chapters'):
        dirs.append('corpus/' + folder + '/')

for path in tqdm(dirs):
    final_edge_tuples = []

    with open(path + 'CORRECTED.actor-benefactor-edge-list.csv', 'r') as csvfile:
        srlreader = csv.reader(csvfile, delimiter=',')

        for row in srlreader:
            final_edge_tuples.append(row)

    actors = [a[0] for a in final_edge_tuples]
    benefactors = [b[1] for b in final_edge_tuples]

    # count total actors for overall share
    total_actor_i = []
    for item in Counter(actors).most_common():
        if item[1] > 2:
            total_actor_i.append(item[1])

    # count total benefactors for overall share
    # skip empties
    total_benefactor_i = []
    for item in Counter(benefactors).most_common():
        if item[1] > 2:
            total_benefactor_i.append(item[1])

    # write out actors
    with open(path + 'actor-counts.csv', 'w') as write_file:

        csvwriter = csv.writer(write_file, delimiter=',',quoting=csv.QUOTE_MINIMAL)

        for item in Counter(actors).most_common():
            csvwriter.writerow([item[0], item[1], round(item[1]/sum(total_actor_i)*100, 6)])

    # write out benefactors
    with open(path + 'benefactor-counts.csv', 'w') as write_file:

        csvwriter = csv.writer(write_file, delimiter=',',quoting=csv.QUOTE_MINIMAL)

        for item in Counter(benefactors).most_common():
            csvwriter.writerow([item[0], item[1], round(item[1]/sum(total_benefactor_i)*100, 6)])
