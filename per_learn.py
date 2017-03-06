import os
import sys
from collections import Counter

nl = '\n'
skip = {'cmds'}
wt={}
bias=0
asd=sys.argv[1]

#Creates dictionary of all files and their constituent words as well as initialize the weights dictionary for the words
def filelist(path):

    fileslist={}
    global wt

    for root, dir, files in os.walk(path):

        for file in files:

            if file not in skip and file.endswith('.txt'):

                fp = os.path.join(root, file)

                if os.path.isfile(fp):

                    past_header, lines = False, []
                    f = open(fp, encoding="latin-1")

                    for line in f:
                        lines.append(line)

                    f.close()
                    stuff = nl.join(lines)
                    words=stuff.split()
                    fileslist[file]=words

                    for item in words:

                        if item not in wt:

                            wt[item]=0

    return(fileslist)

unitstep = lambda x: 0 if x<0 else 1

#Iterate through training data and update weights
def perlearn(files):

    global wt, bias

    for i in range(20):

        for key, value in files.items():

            sum = 0

            if 'spam' in key:

                y = 0
                bias -= 1

            if 'ham' in key:

                y = 1
                bias += 1

            wlist=Counter(value)

            for item, val in wlist.items():
                sum+=wt[item]*val

            error=y-unitstep(sum)

            if error!=0:

                for item, val in wlist.items():

                    wt[item]+=error*val

    wt[' ']=unitstep(bias)

files=filelist(asd)

#The following commented code is for selecting 10% of the training data
'''
files2={}
j=0
k=0

for key in files:

    if 'spam' in key:

        if j <= 0.05 * len(files):

            files2[key]=files[key]

        j+=1

    if 'ham' in key:

        if k <= 0.05 * len(files):

            files2[key]=files[key]

        k+=1

    if j > 0.05 * len(files) and k > 0.05 * len(files):

        break

perlearn(files2)
'''

perlearn(files)
f=open('per_model.txt', 'w')
f.write(str(wt))
f.close()