import re

def bigrams(pwn, lex):
    temp = [] 
    
    for c in lex:
        c = re.sub(r"\n", r"", c)
        if c in pwn:
            temp.append(c)
            
    return temp
    
def make_data(bi, f):
    for b in bi:
        f.write(b + "\n")

pol_in_pwn = open("in_pwn/pol_in_pwn.csv", "w")
unipol_in_pwn = open("in_pwn/unipol_in_pwn.csv", "w")
unipwn_in_pwn = open("in_pwn/unipwn_in_pwn.csv", "w")

#Make the list of clusters that do exist in PWN
pwn_f = open("pwn_clusters.txt", "r").readlines()
pwn = []
for c in pwn_f:
    if re.sub(r"\n", r"", c) not in pwn:
        pwn.append(re.sub(r"\n", r"", c))

file1 = open("pol_bigrams.txt", "r").readlines()
file2 = open("uni_POL_intersection.txt", "r").readlines()
file3 = open("uni_PWN_intersection.txt", "r").readlines()


make_data(bigrams(pwn, file1), pol_in_pwn)
make_data(bigrams(pwn, file2), unipol_in_pwn)
make_data(bigrams(pwn, file3), unipwn_in_pwn)

