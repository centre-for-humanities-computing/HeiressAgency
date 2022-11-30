import os, csv
import string
from glob import iglob
from collections import Counter
from pandas import DataFrame
from tqdm import tqdm
from textblob import Word
from textblob import TextBlob

path = os.getcwd() + '/'
#path = '/home/denten/Documents/papers/projects-academic/workbench/lit-mod-viz/char-agent/corpus/airport/'

# filter out what, that, this, and other junk etc.
# better do this with parts of speech NN and NNP
# need to parse the full report for this
# todo: add noun phrase chunker to differentiate betwen mr. x and mrs. x

blacklist = ['\'t', 'man', 'woman', 'mrs', 'mr', 'didn', 'isn', 'hadn',
        'd.', '\'p', 'o.', '\'d', '\'a', '\'it', '\'c', 'couldn',
        'w', 'n', '\'w', '\'n', '\'i', '\'let', 'doesn', '\'l', '\'r',
        '\'who', 'am', '\'o', '\'f', 'wa', 'r', '\'h', '\'e', '\'g',
        '\'k', 't', 'mr', 'mrs', 's', 'p', 'l', 'i', 'd', 'sir', 'k',
        'o', 'a', 'id', 'c', 'g', 'e', 'yes', 'f']

# penn treebank noun labels
noun_labels = ['NN', 'NNS', 'NNP', 'NNPS']

# grouping "patients" and "adjuncts" in SRL lingo
benefactor_labels = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']

titles = ["Dr", "Doctor", "Professor", "Mr", "Mrs", "Lord", "Lady", "Sir",
          "Miss", "Ms", "Count", "Madame", "Countess", "St", "Don",
          "Tom", "Molly", "George", "Sophia"]


# honorific titles
"""
titles = ["Dr", "Doctor", "Professor", "Mr", "Mrs", "Lord", "Lady", "Sir",
          "Miss", "Ms", "Count", "Madame", "Countess", "St",
          "Laura", "Marian", "Percival", "Anne", "Augusta"]
"""

def clean_string(w):
    return Word(w.strip().translate(
        str.maketrans('','',string.punctuation))).lemmatize()

# Parse the csv in sentence blocks which in our data are separated by blank
# lines. Go through each column clause and if you find A0 grab also all the
# A1+ in the same sentence block. Write results into a list of lists. Columns
# are necessary because A0 can be in any column and we have an arbitrary
# number of columns in senteces that have many clauses.

csv_blocks = []
for filename in sorted(iglob("tom_jones/split/**", recursive=True)):
    if os.path.isfile(filename):
        if filename.endswith(".srl"):
            with open(filename, 'r') as csvfile:

                #csv_blocks = []
                srlreader = csv.reader(csvfile, delimiter="\t")
                block = []
                for row in srlreader:
                    if len(row) > 0:
                        block.append(row)
                    else:
                        csv_blocks.append(block)
                        block = []

# process each black as dataframe
srl_edge_list = []

for block in tqdm(csv_blocks):
    srl_block_panda_df = DataFrame.from_records(block)

    for column in srl_block_panda_df:
        for index0, item0 in srl_block_panda_df[column].iteritems():
            if 'A0' in item0:
                n0 = clean_string(srl_block_panda_df[0][index0])
                try:
                    n1 = clean_string(srl_block_panda_df[0][index0+1])
                except Exception:
                    pass

                if any(title in n0 for title in titles) and n0 is not n1:
                    nouna = n0 + '_' + n1
                    labela = srl_block_panda_df[1][index0].strip()
                else:
                    nouna = n0
                    labela = srl_block_panda_df[1][index0].strip()

                if labela in noun_labels and nouna and nouna not in blacklist:

                    actor = nouna
                    benefactors = []

                    for index1, item1 in srl_block_panda_df[column].iteritems():
                        nb0 = clean_string(srl_block_panda_df[0][index1])

                        try:
                            nb1 = clean_string(srl_block_panda_df[0][index1+1])
                        except Exception:
                            pass

                        if any(title in n0 for title in titles) and nb0 is not nb1:
                            nounb = nb0 + '_' + nb1
                            labelb = srl_block_panda_df[1][index1].strip()
                        else:
                            nounb = nb0
                            labelb = srl_block_panda_df[1][index1].strip()

                        if any(l in item1 for l in benefactor_labels) and labelb in noun_labels and nounb and nounb not in blacklist:
                            benefactors.append(nounb)

                        srl_edge_list.append([actor, benefactors])

final_edge_tuples = []

for cluster in tqdm(srl_edge_list):
    #if any(name in cluster for name in list_of_names):
    actor = cluster[0]
    if cluster[1]:
     #       if any(name in cluster for name in list_of_names):
        for benefactor in cluster[1]:
            final_edge_tuples.append([actor, benefactor])
        else: # there are no benefactors, assume self referential action
            final_edge_tuples.append([actor, actor])

with open('tom_jones/out/06-actor-benefactor-edge-list.csv', 'w') as write_file:
    csvwriter = csv.writer(write_file, delimiter=',',quoting=csv.QUOTE_MINIMAL)
    for t in final_edge_tuples:
        csvwriter.writerow(t)
