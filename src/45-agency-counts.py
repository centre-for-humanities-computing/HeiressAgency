import os, csv, re, string
from collections import Counter
from pandas import DataFrame
from textblob import Word, TextBlob
from tqdm import tqdm
import multiprocessing

def clean_string(w):
    return Word(w.strip().translate(
        str.maketrans('','',string.punctuation)))

blacklist = ['\'t', 'man', 'woman', 'didn', 'don' 'isn', 'hadn',
                'd.', '\'p', 'o.', '\'d', '\'a', '\'it', '\'c', 'couldn',
                        'w', 'n', '\'w', '\'n', '\'let', 'doesn', '\'l', '\'r',
                                '\'who', 'am', '\'o', '\'f', 'wa', 'r', '\'h', '\'e', '\'g',
                                        '\'k', 't', 's', 'p', 'l', 'd', 'sir', 'k', 
                                                'o', 'a', 'id', 'c', 'g', 'e', 'yes', 'f',
                                                        'they', 'their', 'them', 'he', 'him', 'his',
                                                                'she', 'her', 'hers', 'you', 'yours']

# penn treebank noun labels
noun_labels = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP']

# grouping "patients" and "adjuncts" in SRL lingo
benefactor_labels = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']

# only grabbing the boundary-defining semantic roles related to location
factor_labels = ['AM-DIR', 'AM-EXT', 'AM-LOC']

#pronouns = ["I", "we", "us", "our", "she", "he", "her", "him"]
# honorific titles
titles = ["King", "Queen", "Prince", "Princess", "Reverend", "Dr", "Dr.", "Doctor", "Professor", "Mr", "Mr.", "Mrs", "Mrs.", "Lord", "LORD", "Lady", "Sir", "Miss", "MISS", "Ms", "Count", "St", "st", "Signora", "Du", "Countess_of", "Count_of", "Lord_of", "Lady_of", "Baron", "Baroness", "Baron_of", "Baronness_of", "Sargenat", "Lietenant", "Captain", "Major", "General", "Madame", "Monsieur"]

# set path
dirs = []
for folder in os.listdir('corpus'):
    if folder.endswith('-chapters'):
        dirs.append('corpus/' + folder + '/')


# process csv blocks
# REMEMBER TO SET FOR SUB-FOLDERS - VOLUMES, ETC.
for path in tqdm(dirs):
    csv_blocks = []
    for filename in os.listdir(path):
        if filename.endswith(".srl"):
            with open(path + filename, 'r') as csvfile:
                srlreader = csv.reader(csvfile, delimiter="\t")

                block = []
                for row in srlreader:
                    if len(row) > 0:
                        block.append(row)
                    else:
                        csv_blocks.append(block)
                        block = []

    ############################################
    """
    Extract A0 agents
    """
    ############################################

    # process each black as dataframe
    agent_list = []

    for block in csv_blocks:
        srl_block_panda_df = DataFrame.from_records(block)
        for column in srl_block_panda_df:
            for index, item in srl_block_panda_df[column].iteritems():
                if 'A0' in item:
                    nouna = clean_string(srl_block_panda_df[0][index])
                    labela = srl_block_panda_df[1][index].strip()
                    if labela in noun_labels and nouna and nouna not in blacklist:
                        agent = nouna
                        agent_list.append(agent)


    # join up names with titles - eg Mr + Rochdale
    joined_up = []
    all_indices = []
    for idx, agent in enumerate(agent_list):
        agent = re.sub(r'[^\w\s]','',agent) 
        if any(title in agent for title in set(titles)):
            try:
                indices = idx, idx+1
                all_indices.append(indices)
                name = (agent_list[idx], agent_list[idx+1])
                joined_up.append(' '.join(name))
            except IndexError:
                pass

    # delete the unconnected entities and extend joined_up list
    for i in sorted([item for t in all_indices for item in t], reverse=True):
        try:
            del agent_list[i]
        except:
            pass
    joined_up.extend(agent_list)

    # count number of occurrences per character
    counts = Counter(joined_up).most_common()

    # write to csv
    with open(path + "agents_A0.csv", 'a') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['name','num'])
        for entry in counts:
            csv_out.writerow(entry)

    ##############################################
    """
    Extract A1-A5 benefactors
    """
    ##############################################

    # process each black as dataframe
    benefactor_list = []

    for block in csv_blocks:
        srl_block_panda_df = DataFrame.from_records(block)
        for column in srl_block_panda_df:
            for index, item in srl_block_panda_df[column].iteritems():
                if any(label in item for label in benefactor_labels):
                    nouna = clean_string(srl_block_panda_df[0][index])
                    labela = srl_block_panda_df[1][index].strip()
                    if labela in noun_labels and nouna and nouna not in blacklist:
                        benefactor = nouna
                        benefactor_list.append(benefactor)


    # join up names with titles - eg Mr + Rochdale
    joined_up = []
    all_indices = []
    for idx, benefactor in enumerate(benefactor_list):
        benefactor = re.sub(r'[^\w\s]','',benefactor)
        if any(title in benefactor for title in set(titles)):
            try:
                indices = idx, idx+1
                all_indices.append(indices)
                name = (benefactor_list[idx], benefactor_list[idx+1])
                joined_up.append(' '.join(name))
            except:
                pass

    # delete the unconnected entities and extend joined_up list
    for i in sorted([item for t in all_indices for item in t], reverse=True):
        try:
            del benefactor_list[i]
        except:
            pass
    joined_up.extend(benefactor_list)

    # count number of occurrences per character
    counts = Counter(joined_up).most_common()

    # write to csv
    with open(path + "benefactors_A1-A5.csv", 'a') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['name','num'])
        for entry in counts:
            csv_out.writerow(entry)

