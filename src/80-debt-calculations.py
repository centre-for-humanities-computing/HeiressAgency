import os, csv
from operator import itemgetter
from tqdm import tqdm

dirs = []
for folder in os.listdir('corpus'):
    if folder.endswith('-chapters'):
        dirs.append('corpus/' + folder + '/')

for path in tqdm(dirs):
    actor_array = []
    benefactor_array = []

    with open(path + 'actor-counts.csv', 'r') as csvfile:
        srlreader = csv.reader(csvfile, delimiter=',')

        for row in srlreader:
            actor_array.append(row)

    with open(path + 'benefactor-counts.csv', 'r') as csvfile:
        srlreader = csv.reader(csvfile, delimiter=',')

        for row in srlreader:
            benefactor_array.append(row)

    ratio = []

    """ The second metric I propose to explore is *volitional debt ratio*,
    representing a ratio of action to benefit. A debt ratio of one would mean the
    character acts and benefits from action in equal measure. A debt ratio of more
    than one indicates *volitional excess*: the character acts in greater
    proportion to the derived benefit from the total action of the plot. A debt
    ratio less than one indicates debt, in which case the entity benefits in
    greater share than its action.  """

    for li in actor_array:
        name = li[0]
        share = li[2]

        for il in benefactor_array:
            if name == il[0]:
                ratio.append([name, (float(share)/float(il[2]))-1])
                #ratio.append([name, float(il[2])/float(share)])

    sorted_ratio = sorted(ratio, key=itemgetter(1), reverse=True)

    with open(path + 'volitional-debt-ratios.csv', 'w') as write_file:

        csvwriter = csv.writer(write_file, delimiter=',',quoting=csv.QUOTE_MINIMAL)

        for item in sorted_ratio:
            csvwriter.writerow(item)
