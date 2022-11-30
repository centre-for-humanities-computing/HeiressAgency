import os, subprocess
import glob
import multiprocessing

files = glob.glob('corpus/*/*.sents')

def process(text):
    with open(text, 'r') as myreadfile:
        incant = '~/senna/senna-linux64 -path ~/senna/senna < ' + text + ' > ' + text + '.srl'
        subprocess.call(incant, shell=True)

p = multiprocessing.Pool()
p.map(process, files)
p.close()
p.join()
