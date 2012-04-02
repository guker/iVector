'''
Created on Jan 31, 2012

@author: Tokminator
'''
import os
import math

#Setup
languages = [ 'ARABIC_EGYPT', 'ENG_GENRL', 'ENG_SOUTH', 'FARSI', 'FRENCH_CAN', 'GERMAN', 'HINDI', 'JAPANESE', 'KOREAN', 'MANDARIN_M', 'MANDARIN_T', 'SPANISH', 'SPANISH_CAR', 'TAMIL', 'VIETNAMESE' ]
inbasedir = './CallFriend/?/Splitted30/'
setdir = ['train_raw/', 'devtest_raw/', 'evltest_raw/']
outbasedir = './CallFriend/?/docnumvectors30/'
unigramlistin = './other/unigramList.txt'
#unigramlistin = './other/fullUnigramList.txt'
outfilelistnames = ['./other/train_list.txt', './other/devtest_list.txt', './other/evltest_list.txt']
onlyTrigrams = 0


#Parameter initialization
allunigrams = {}
numofunigrams = 0

class DocInfo:
    def __init__(self, fname, lang):
        self.lang = lang
        self.fname = fname

def isSilence(symbol):
    return symbol == 'sil' or symbol == 'pau'

def isNoise(symbol):
    return symbol == 'spk' or symbol == 'int'

#To avoid feature ending with \n
def normalizeFeature(feature):
    return feature.rstrip()

'''#1 to 1 maps feature strings to ints
def calc_feature_num(trigram):
    num = 0
    for i in range(3):
        num += allunigrams[trigram[i]]*math.pow(numofunigrams, 2-i)
    return int(num)
'''
def insert_feature_num(num, vector):
    if vector.has_key(num):
        vector[num] += 1
    else:
        vector[num] = 1

def insert_features(ngram, vector):
    lastnum = 0
    for i in range(len(ngram)):
        num = allunigrams[trigram[i]]*math.pow(numofunigrams, i)
        if i > 0:
            num += lastnum+math.pow(numofunigrams, i)
        insert_feature_num(num, vector)
        lastnum = num
            
def insert_feature(trigram, vector):
    if len(trigram) == 3:
        num = 0
        for i in range(3):
            num += allunigrams[trigram[i]]*math.pow(numofunigrams, 2-i)
        insert_feature_num(num, vector)


#Read list of possible unigrams
unigramfile = open(unigramlistin, 'r')
for line in unigramfile:
    splitline = line.split(' ')
    for splits in splitline:
        allunigrams[normalizeFeature(splits)] = numofunigrams
    numofunigrams += 1


for i in range(len(setdir)):
    alldocs = []
    for language in languages:
        outdir = outbasedir.replace('?', language)+setdir[i]
        indir = inbasedir.replace('?', language)+setdir[i]
        os.system('mkdir -p '+outdir)
        for filename in os.listdir(indir):
            tranfile = open(indir+filename, 'r')
            lastphones = []
            docvector = {}
            for line in tranfile:
                splitline = line.split(' ')
                if len(splitline) > 3:
                    phone = normalizeFeature(splitline[2])
                    
                    if isNoise(phone) or (isSilence(phone) and len(lastphones) > 0 and isSilence(lastphones[0])):
                        continue
                    
                    lastphones.insert(0, phone)
                    if len(lastphones) > 3:
                        lastphones.pop(3)
                    
                    if onlyTrigrams:
                        insert_feature(lastphones, docvector)
                    else:
                        insert_features(lastphones, docvector)
            outfile = open(outdir+filename, 'w')
            for key, value in docvector.items():
                outfile.write(str(key)+' '+str(value)+' '+str(math.sqrt(value))+'\n')
            
            alldocs.append(DocInfo(outdir+filename, language))
            
            print 'Finished with file '+outdir+filename
    outfile = open(outfilelistnames[i], 'w')
    for doc in alldocs:
        outfile.write(doc.lang+' '+doc.fname+'\n')

print str(allunigrams)
print 'Finished, total number of unigrams: '+str(numofunigrams)+', trigrams: '+str(math.pow(numofunigrams, 3))
if not onlyTrigrams:
    print 'Total: '+str(numofunigrams+math.pow(numofunigrams, 2)+math.pow(numofunigrams, 3))