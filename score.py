import re

def score(cluster, son_vectors, neg_vectors):
#Here we actually build the score for each cluster, using the sonority scaling, the negative vectors, and the subfactors 
    for c in cluster:
        sonority = son_vectors[c]
        negatives = neg_vectors[c]
        
        #scores????

def subfactor(cluster, all_clusters):
#Finds the frequency and sonority scores of all subfacters for a given cluster
#posibly will have to rewrite all_clusters as a dictionary with the tuple of n-gram and unimorph)
    x_loc = 0
    for x in cluster:
        y_loc = 0
        temp = x
        for y in cluster:
            if y_loc <= x_loc:
                temp += y
                
                #here is where we actually look up the frequencies of the subfactors in all_clusters, and any other vectors   
                if temp in all_clusters:
                    print(all_clusters[temp])
        
            y_loc+=1
            
        x_loc += 1
    
def decode():
    k = open("key.csv")
    key = {}
    
    for line in k:
        x = re.split(",|\n", line)
        #here is where the problem is occuring = key[cz] is writing as both [tS] and [ts]z 
        
        if x[1] in key:
            if isinstance(key[x[1]], list):
                key[x[1]].append(x[0])
            else: 
                key[x[1]] = [key[x[1]]]
        else:
            key[x[1]] = x[0]

    
    return key

def score_vector(cluster):

#A function that, for any given cluster, finds the sonority shift from consonant to consonant

    stop_score = 0
    affricate_score = .5
    fricative_score = 1
    nasal_score = 2
    liquid_score = 3
    glide_score = 4

    stop = ['p', 't', 'k', 'b', 'd', 'g', 'ɟ', 'c']
    fricative = ['s', 'z', 'ʃ', 'ʒ"', 'ɕ', 'ʑ', 'f', 'v', 'x']
    nasal = ['n', 'm', 'ɲ']
    liquid = ['l', 'r']
    glide = ['w', 'j']
 
    total = 0
    score_vector = []
    neg_vector = []
    
    cur = False
    cur_score = False
    affricate = False 
    neg = False 
    for x in cluster:
        if affricate and x==']':
        
            affricate = False
            
            if cur_score > .5 and not neg:
                neg = True
                neg_vector.append(-1)
            else: neg_vector.append(1)
            
            cur_score = .5
            score_vector.append(cur_score)
        
        if not affricate:
            if x == '[':
                affricate = True
            
            elif x in stop:
                if cur_score > 0 and not neg:
                #if cur_score is greater, then the sonority is falling
                    neg = True
                    neg_vector.append(-1)
                else: neg_vector.append(1)
                cur_score = 0
                score_vector.append(cur_score)
            
            elif x in fricative:
                if cur_score > 1 and not neg:
                    neg = True
                    neg_vector.append(-1)
                else: neg_vector.append(1)
                cur_score = 1
                score_vector.append(cur_score)
            
            elif x in nasal:
                if cur_score > 2 and not neg:
                    neg = True
                    neg_vector.append(-1)
                else: neg_vector.append(1)
                cur_score = 2
                score_vector.append(cur_score)
            
            elif x in liquid:
                if cur_score > 3 and not neg:
                    neg = True
                    neg_vector.append(-1)
                else: neg_vector.append(1)
                cur_score = 3
                score_vector.append(cur_score)
            
            elif x in glide:
                if cur_score > 4 and not neg:
                    neg = True
                    neg_vector.append(-1)
                else: neg_vector.append(1)
                cur_score = 4
                score_vector.append(cur_score)
            
        #total += cur 
        #if affricate == True: print(x)
        cur = x
     
    return (score_vector, neg_vector)
    
def build():
    
    #Re-translate nonse words into clusters to determine acceptability averages 
    key = decode()
    
    k = open("pol.csv")
    a = open("acceptability_master.csv")
    avgs = {}
    
    for line in a:
        x = re.split(r",|\n", line)
        if "WORD" not in x:
            cluster = re.split(r"a|ą|o", x[0])
            if isinstance(key[cluster[0]], list):
                avgs[key[cluster[0]][0]] = x[5]
            else:
                avgs[key[cluster[0]]] =  x[5]
        
    #Compile score files
    score = open("main_score.csv", "w+")
    shifts = open("sonority.csv", "w+")
    neg = open("sonority_neg.csv", "w+")
    
    for x in k:
        temp = re.split(r",|\n", x) 
        if "CLUSTER" not in temp and temp[0] != '' :
            score.write(temp[0] + "," + temp[1] + ",")
            shifts.write(temp[0])
            neg.write(temp[0])
            
            vec = score_vector(x)
            score.write(str(len(vec[0])))
            
            #SON_TOTAL is a score measure totalling all of the sonority shifts, without negative values
            son_total = 0
            for i in vec[0]:
                shifts.write("," + str(i))
                son_total += i
            for i in vec[1]:
                neg.write("," + str(i))
            
            if temp[0] in avgs:        
                score.write("," + str(son_total) + "," + avgs[temp[0]] + "\n")
            else:
                print(temp[0])
                score.write("," + str(son_total) + ",--\n")
            shifts.write("\n")
            neg.write("\n")
        
    score.close()
    shifts.close()
    neg.close()

build()
#score: any sonority fall automatically makes the score negative
#score: any sonority fall increases the score by an exponent 
