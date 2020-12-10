import re 

def to_bigrams(lst):
    
    """
    For any given cluster (given in IPA), breaks down the cluster into its individual bigrams. 
    Notably, in clusters with affricates, which are made up of multiple characters here, it
    takes into account the affricate boundaries (noted by '[' and ']') to read it as a single 
    phone. 
    """
    bi = []
    lst = "#" + lst + "#"
    if '[' not in lst:
        for x in range(len(lst) - 1):
            if lst[x:x+2] not in bi:
                bi.append(lst[x:x+2])
                
    #In case the cluster has an affricate, extra care has to be had
    else:
        aff = False
        clus = ''
        temp = ''
        
        for x in range(len(lst)):
            if lst[x] == '[':
                aff = True
                temp = '['
            elif lst[x] == ']': 
                aff = False
                temp = temp + ']'
                
                if clus + temp not in bi:
                    bi.append(clus + temp)
                
                clus = temp
            elif aff:
                temp = temp + lst[x]
            else:
                temp = lst[x]
                
                if clus + temp not in bi and len(clus+temp) > 1:
                    bi.append(clus + temp)
                clus = temp
    return(bi)
    
def write_found(found, where):
    """
    Writes bigrams to file based on 1) whether they were found in the PWN or not,
    and 2) with the average acceptability score of words that included the bigram. 
    """
    f = open("data/speaker_" + where + "_pwn.csv", "w")
    
    for i in found.keys():
        #print(i, found[i])
        avg = sum(found[i]) / len(found[i])
        #for n in found[i]:
        #    f.write("," + str(n))
        f.write(i +"," + str(avg) + "\n")
        
    f.close()

#------------------------------------------

if __name__ == "__main__":
    
    #score - ortho : number
    #speaker_clusters - IPA : ortho
    #reverse_key - ortho:IPA
    #speaker_bigrams - IPA: list of bigrams
    
    #open acceptability master list, compile scores for clusters
    g = open("acceptability_master_PWN.csv", "r").readlines()
    score = {}
    for x in g:
        x = re.split(r",|\n", x)
        if x[0] != "WORD":
            if x[-2]:
                score[x[0]] = float(x[-2])
            else:
                print("else", x)
            
    #Open key to extract clusters used in data
    f = open("key.csv", "r").readlines()
    speaker_clusters = {}
            
    for x in f:
        x = re.split(r",|\n", x)
        #score[x[0]] = x[
        speaker_clusters[x[0]] = x[1]
       
    
    speaker_bigrams = {}
    for x in speaker_clusters.keys():
        #key = IPA cluster, value = list of present bigrams 
        speaker_bigrams[x] = to_bigrams(x)
    
            
    #Open pwn, get bigrams
    f = open("data/pwn_clusters.txt", "r").readlines()
    pwn_bigrams = []
    for x in f:
        x = re.sub(r"\n", r"", x)
        temp = to_bigrams(x)
        for y in temp:
            if y not in pwn_bigrams: 
                pwn_bigrams.append(y)
                
    ####################
    # compare clusters #
    ####################
    #in_pwn = open("data/speaker_in_pwn.txt", "w")
    #not_pwn = open("data/speaker_not_pwn.txt", "w")
    
    found_in = {}
    found_out= {}
    for x in speaker_bigrams: #cluster
        for bi in speaker_bigrams[x]: #list of bigrams
            if bi in pwn_bigrams:
                if bi in found_in.keys():
                    found_in[bi].append(score[speaker_clusters[x]])
                else:
                    try:
                        found_in[bi] = [score[speaker_clusters[x]]]
                        break
                    except KeyError:
                        print(speaker_clusters[x])
                    
            else:
                if bi in found_out.keys():
                    found_out[bi].append(score[speaker_clusters[x]])
                else:
                    found_out[bi] = [score[speaker_clusters[x]]]
                    
    write_found(found_in, "in")
    write_found(found_out, "out")
    
    ######################################################
    # write clusters & infractions & acceptability score #
    ######################################################
    
    ill = open("data/illegal_clusters.csv", "w")
    ill.write("CLUSTER, ILLEGAL, ACCEPT\n")
    # per cluster
    for x in speaker_clusters.keys():
        #check if bigrams are in PWN
        lst = to_bigrams(x)
        for y in lst:
            if y  in pwn_bigrams:
                lst.remove(y)


        txt = x + "," + str(len(lst)) + "," + str(score[speaker_clusters[x]]) + "\n"
        print(txt, end="")
        ill.write(txt)
    
    
    #-----------------------


    
            
