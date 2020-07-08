import pynini 
import functools 
import re
import random

def generate(c):

    words = []
    
    for cluster in c:
        words.append(cluster + "ąc")
        words.append(cluster + "olek")
        words.append(cluster + "arek")
    #    words.append(cluster + 
    
    return words 
    
def randomize(c):
    
    f = open("acceptability.csv", "w")
    random.shuffle(c)
    
    for line in c:
        f.write(line + ",,\n")
        
    f.close()
    
def extract(results):
    
    f = open(results+".csv")
    key = open("key.csv")
    
    k = {}
    for line in key:
        x = re.split(r",|\n", line)
        k[x[1]] = x[0]
    
    neg = []
    for line in f:
        x = re.split(r",|\n", line)
        if x[1] == "0":
            neg.append(x[0])
            
    rejects = []
    rej = {}
    for item in neg:
        x = re.split(r"a|o|ą", item)
        if x[0] not in rejects:
            rejects.append(k[x[0]])
            rej[k[x[0]]] = 1
        else:
            rej[k[x[0]]] +=1

    r = open("rejects.csv", "w")
    for line in rej:
        r.write(line + "," + str(rej[line]) + "\n")
    #print(k)
    
    
f = open("pol.csv") 

clusters = []

for line in f:
    #print(line)
    x = re.split(r',', line)
    clusters.append(x[0])
    
clusters = clusters[2:]
back = []

single = ['b', 'd', 'f', 'g', 'j','k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'z']
 

a = ''
k = open("key.csv", "w")
for c in clusters:
    hold = False
    temp = ''
    for p in c:
        count = 1
        if not hold:
            if p in single:
                a += p
            elif p == '[':
                hold = True
            elif p == 'ɟ': a+='gi'
            elif p == 'x': a+='ch'
            elif p == 'c': a+='ki'
            elif p == 'w': a+='ł'
            elif p == 'ɲ': a+='ni'
            elif p == 'ʃ': a+='sz'
            elif p == 'ɕ' and count == len(c): a+='si'
            elif p == 'ɕ': a+='ś'
            elif p == 'v': a+='w'
            elif p == 'ʑ': a+='ź'
            elif p == 'ʒ': a+='ż'
            else: print(p)
        if hold:
            if p == "]":
                if temp == "tʃ" or temp == "[tʃ": a += "cz"
                elif temp == "dʑ" or temp == "[dʑ": a+= "dź"
                elif temp == "dʒ" or temp == "[dʒ": a+="dż"
                elif temp == "ts" or temp == "[ts": a+="c"
                elif temp == "dz" or temp == "[dz": a+="dz"
                else: print(temp, c)
                hold = False
                temp = ''
            else: 
                temp += p
        count+=1
    back.append(a)
    k.write(c + "," + a + "\n")
    a = ''
    
#generate(back) to create list of all 
#randomize(generate(back)) to randomize and save to file
