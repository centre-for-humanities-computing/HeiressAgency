import spacy
import neuralcoref
import os
import multiprocessing

spacy.prefer_gpu()
nlp = spacy.load('en')
neuralcoref.add_to_pipe(nlp)


def run_coref(text):
    doc = nlp(text)
    return doc._.coref_resolved

def write_file (filename, resolved_text):
    with open(filename + '.resolved', 'w') as write_file:
        for item in resolved_text:
            # write_file.write("{}\n".format(item))
            write_file.write(item)

def process(text):
    with open(text, 'r') as myreadfile:    
        write_file(text, run_coref(myreadfile.read()))

dirs = []
for folder in os.listdir('corpus'):
    if folder.endswith('chapters'):
        dirs.append('corpus/' + folder + '/')

chapters = []
for path in dirs:
    for filename in os.listdir(path):
        if filename.endswith(".wrap"):
            chapters.append(path + filename)
        
p = multiprocessing.Pool()
p.map(process, chapters)
p.close()

