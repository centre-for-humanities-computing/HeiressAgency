import os
# run from top level directory in corpus/
# assumes chapterization


# processing pipeline
# wrap > coref > sent-token > semantic role label
# make sure the lines are wrapped properly
# as the wrapping affects the sentence tokenizer later
dirs = []
for folder in os.listdir('corpus'):
    if folder.endswith('chapters'):
        dirs.append('corpus/' + folder + '/')

for path in dirs:
    for filename in os.listdir(path):
        wrapped = ""
        with open(path + filename, 'r') as myreadfile:
            for line in myreadfile.readlines():
                wrapped = wrapped + line.replace('\n', ' ')

        with open(path + filename + '.wrap', 'w', encoding="utf-8") as write_file:
            write_file.write(wrapped)
