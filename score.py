import re

def s_score(score_vector, neg_vector):

    """s_score takes the score_vector and neg_vector - vectors that 
        track the sonority score of each phone and the orientation 
        of sonority shift respectively - and uses both to average
        a sonority score over an entire cluster.
    """
    
    s = 0
    
    #for 'clusters' of length =1 - ?
    if len(score_vector) == 1:
        return s
    #for clusters of length >1 - avg adjacent integers, multiply by neg
    else:
        
        for x in range(len(score_vector)):
            #print("LENGTH:",x+1, len(neg_vector))
            if (x+1) < len(neg_vector):
                s += (score_vector[x] + score_vector[x+1]) / 2 * neg_vector[x+1]
        
    return s

def subfactor(clusters):
    """sub_factor takes the list of extant clusters and determines
        all subfactor clusters that appear in the lexicon. Then,
        it scores these subfactor clusters and saves the scores
        to the subfactors CSV.
    """
    
    subfactors = open("subfactors.csv", "w+")
    
    #clusters = avgs.keys()
    affricate = False
    
    #for all clusters
    for x in clusters:
        subfactors.write(x + ",")
        
        #y and z are both position pointers within the cluster to determine possible subfactors 
        #adjust y so it cannot point to elements of an affricate, only the full affricate
        affricate_outer = False
        for y in range(len(x)):
            
            #print(x[y])
            if x[y] == '[':
                affricate_outer = True
                aff_buffer = '['
            elif x[y] ==']':
                affricate_outer = False
                temp = aff_buffer + ']'
                #print("BUFFER", aff_buffer + ']')
                aff_buffer = ''
            elif affricate_outer:
                #print("OUTPUT", x[y])
                aff_buffer += x[y]
            else:
                temp = x[y]
                aff = ''
            
            if not affricate_outer:
                
                #check if y as unigram is a subfactor
                if temp in clusters:
                    s = score_vector(temp)
                    s2 = s_score(s[0], s[1])
                    #subfactors.write(temp + ",")
                    subfactors.write(str(s2) + ",")
            
                for z in range(len(x)):
                    if z > y:
                        #check to see if z is an affricate boundary. if end boundary, add to our temporary cluster 
                        if x[z] == '[':
                            affricate = True
                            aff = '['
                        elif x[z] == ']':
                            affricate = False
                            temp += aff + ']'
                            #aff = ''
                        #if in affricate mode but not an affricate boundary, add to temp affricate buffer
                        elif affricate:
                            aff += x[z]
                        #if no affricate period, add to temp normally 
                        else:
                            temp += x[z]
                
                
                        #if not in affricate mode but temp is not identical to cluster, check if subfactor
                        #print(x, temp)
                        if len(temp) != len(x) and not affricate:
                        
                            if temp in clusters:
                                #change print to log subfactor score in 
                                s = score_vector(temp)
                                s2 = s_score(s[0], s[1])
                                #subfactors.write(temp + ",")
                                subfactors.write(str(s2) + ",")
        subfactors.write("\n")
            
    
def decode():
    
    """decode takes the key CSV, which logs the IPA and orthographic 
        equivalents, and creates a decoding dictionary so that all
        nonse words can be translated back into IPA.
    """
    k = open("key.csv")
    key = {}
    
    for line in k:
        x = re.split(",|\n", line)
        #here is where the problem is occuring : key[cz] is writing as both [tS] and [ts]z 
        
        if x[1] in key:
            if isinstance(key[x[1]], list):
                key[x[1]].append(x[0])
            else: 
                key[x[1]] = [key[x[1]]]
        else:
            key[x[1]] = x[0]

    return key

def score_vector(cluster):

    """score_vector takes any cluster and returns two vectors, which:
        1) logs the individual sonority score of each phone in a cluster, and
        2) logs whether the sonority is increasing or decreasing from the
            previous character.
    """

    stop_score = 0
    affricate_score = .5
    fricative_score = 1
    nasal_score = 2
    liquid_score = 3
    glide_score = 4

    stop = ['p', 't', 'k', 'b', 'd', 'g', 'ɟ', 'c']
    fricative = ['s', 'z', 'ʃ', 'ʒ', 'ɕ', 'ʑ', 'f', 'v', 'x']
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
    
    """build is the main method, with these key parts:
        1) creating the decoder in decode, then back-translating acceptability scores
        2) building CSVs for
            a. a cluster with its frequency, averaged sonority score, length, and averaged acceptability,
            b. the individual sonority scores, determined by score_vector
            c. the increasing/decreasing sonority values, determined by score_vector
        3) uses s_score to record the sonority score to the main file, while copying score_vector 
            output to the other two files
    """
    
    #Re-translate nonse words into clusters to determine acceptability averages 
    key = decode()
    #print(key)
    
    k = open("pol.csv")
    a = open("acceptability_master.csv")
    avgs = {}
    
    for line in a:
        x = re.split(r",|\n", line)
        if "WORD" not in x:
            cluster = re.split(r"a|ą|o", x[0])
            if isinstance(key[cluster[0]], list):
                if key[cluster[0]][0] in avgs:
                    avgs[key[cluster[0]][0]] += float(x[5])
                else:
                    avgs[key[cluster[0]][0]] = float(x[5])
            else:
                if key[cluster[0]] in avgs:
                    avgs[key[cluster[0]]] +=  float(x[5])
                else:
                    avgs[key[cluster[0]]] =  float(x[5])
                    
                    
    #After avgs is built, pass into subfactors to build subfactor sonority list 
    subfactor(avgs.keys())
        
    #Compile score files
    score = open("main_score.csv", "w+")
    shifts = open("sonority.csv", "w+")
    neg = open("sonority_neg.csv", "w+")
    
    score.write("CLUSTER, FREQUENCY, LENGTH, SONORITY, ACCEPTABILITY\n")
    
    for x in k:
        temp = re.split(r",|\n", x) 
        if "CLUSTER" not in temp and temp[0] != '' and temp[0] != "[ts]z" and temp[0] != "dʒ" :
            #score.write(temp[0] + "," + temp[1] + ",")
            #write cluster + frequency (5-gram)
            score.write(temp[0] + "," + temp[1] + ",")
            shifts.write(temp[0])
            neg.write(temp[0])
            
            #calculate sonority score
            vec = score_vector(x)
            s = s_score(vec[0], vec[1])
            
            #write sonority (measure 1) + length
            #score.write(str(s) + ",")
            score.write(str(len(vec[0])))
            
            #SON_TOTAL is a score measure totalling all of the sonority shifts, without negative values
            son_total = 0
            for i in vec[0]:
                shifts.write("," + str(i))
                son_total += i
            for i in vec[1]:
                neg.write("," + str(i))
            
            if temp[0] in avgs:
                #[tS] is doubling the acceptability because of the confusion between 'cz' as a cluster and as an affricate. So, we halve it.
                if temp[0] == '[tʃ]' or temp[0] == '[dʒ]':
                    score.write("," + str(son_total) + "," + str((avgs[temp[0]]/3)/2) + "\n")
                else:
                    score.write("," + str(son_total) + "," + str(avgs[temp[0]]/3) + "\n")
                #if str(avgs[temp[0]]/3) == "2.0":
                #    print("ALERT", avgs[temp[0]], temp[0])
            else:
                print("EXCLUDE: " + temp[0])
                score.write("," + str(son_total) + ",-1\n")
            shifts.write("\n")
            neg.write("\n")
        
    score.close()
    shifts.close()
    neg.close()
    
    return avgs

avgs = build()
#score: any sonority fall automatically makes the score negative
#score: any sonority fall increases the score by an exponent 
