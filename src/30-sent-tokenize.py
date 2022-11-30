from textblob import TextBlob
import os
import multiprocessing

def tokenize(text):
    blob = TextBlob(text)
    return blob.sentences

def write_file (filename, toke_text):
    with open(filename + '.sents', 'w') as write_file:
        for item in toke_text:
            write_file.write("{}\n".format(item.string))

def process(text):
        with open(text, 'r') as myreadfile:
            write_file(text, tokenize(myreadfile.read()))

dirs = []
for folder in os.listdir('corpus'):
    if folder.endswith("-chapters"):
        print(folder)
        dirs.append('corpus/' + folder + '/')

print(dirs)

chapters = []
for path in dirs:
    for filename in os.listdir(path):
        if filename.endswith('.resolved'):
            chapters.append(path + filename)

print(chapters)

p = multiprocessing.Pool()
p.map(process, chapters)
p.close()
p.join()
