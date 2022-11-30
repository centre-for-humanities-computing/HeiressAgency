import os, csv, string
from collections import Counter
from pandas import DataFrame
from textblob import Word, TextBlob
from tqdm import tqdm

blacklist = ['\'t', 'man', 'woman', 'didn', 'don' 'isn', 'hadn',
        'd.', '\'p', 'o.', '\'d', '\'a', '\'it', '\'c', 'couldn',
        'w', 'n', '\'w', '\'n', '\'let', 'doesn', '\'l', '\'r',
        '\'who', 'am', '\'o', '\'f', 'wa', 'r', '\'h', '\'e', '\'g',
        '\'k', 't', 's', 'p', 'l', 'd', 'sir', 'k', 
        'o', 'a', 'id', 'c', 'g', 'e', 'yes', 'f',
        'they', 'their', 'them', 'he', 'him', 'his',
        'she', 'her', 'hers', 'you', 'yours']

# penn treebank noun labels
noun_labels = ['NN', 'NNS', 'NNP', 'NNPS']

# grouping "patients" and "adjuncts" in SRL lingo
benefactor_labels = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']

# honorific titles (and first names!)
# honorific titles
titles = ["King", "Queen", "Prince", "Princess", "Reverend", "Dr", "Dr.", "Doctor", "Professor", "Mr", "Mr.", "Mrs", "Mrs.", "Lord", "LORD", "Lady", "Sir", "Miss", "MISS", "Ms", "Count", "St", "st", "Signora", "Du", "Countess_of", "Count_of", "Lord_of", "Lady_of", "Baron", "Baroness", "Baron_of", "Baronness_of", "Sargenat", "Lietenant", "Captain", "Major", "General", "Madame", "Monsieur"]

def clean_string(w):
    return Word(w.strip().translate(
        str.maketrans('','',string.punctuation)))


dirs = []
for folder in os.listdir('corpus'):
    if folder.endswith('-chapters'):
        dirs.append('corpus/' + folder + '/')
# Parse the csv in sentence blocks which in our data are separated by blank
# lines. Go through each column clause and if you find A0 grab also all the
# A1+ in the same sentence block. Write results into a list of lists. Columns
# are necessary because A0 can be in any column and we have an arbitrary
# number of columns in senteces that have many clauses.
 
for path in tqdm(dirs):
    csv_blocks = []
    for filename in os.listdir(path):
        if filename.endswith(".srl"):
            with open(path + filename, 'r') as csvfile:
                
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

    for block in csv_blocks:
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
                            
                            if any(title in nb0 for title in titles) and nb0 is not nb1:
                                nounb = nb0 + '_' + nb1
                                labelb = srl_block_panda_df[1][index1].strip()
                            else:
                                nounb = nb0
                                labelb = srl_block_panda_df[1][index1].strip()
                            
                            if any(l in item1 for l in benefactor_labels) and labelb in noun_labels and nounb and nounb not in blacklist:
                                benefactors.append(nounb)
                                
                                srl_edge_list.append([actor, benefactors])

    final_edge_tuples = []

    for cluster in srl_edge_list:
        actor = cluster[0]
        if cluster[1]:
            for benefactor in cluster[1]:
                final_edge_tuples.append([actor, benefactor])
        else: # there are no benefactors, assume self referential action
            final_edge_tuples.append([actor, actor])

            
    with open(path + 'actor-benefactor-edge-list.csv', 'w') as write_file:
        csvwriter = csv.writer(write_file, delimiter=',',quoting=csv.QUOTE_MINIMAL)
        for t in final_edge_tuples:
            csvwriter.writerow(t)
