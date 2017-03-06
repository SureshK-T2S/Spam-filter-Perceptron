import os
import sys
from collections import Counter

asd=sys.argv[1]
nl = '\n'
skip = {'cmds'}
wt={}
bias=0
b=0
wt2={}

#Creates dictionary of all files and their constituent words as well as initialize the weights dictionary for the words
def filelist(path):

    fileslist={}
    global wt, wt2

    for root, dir, files in os.walk(path):

        for file in files:

            if file not in skip and file.endswith('.txt'):

                fp = os.path.join(root, file)

                if os.path.isfile(fp):

                    f = open(fp, encoding="latin-1")
                    lines=[line for line in f]
                    f.close()
                    stuff = nl.join(lines)
                    words=stuff.split()
                    fileslist[file] = words

                    for item in words:

                        if item not in wt:

                            wt[item]=0

    return(fileslist)

unitstep = lambda x: 0 if x<0 else 1

#Iterate through training data and update weights
def avgperlearn(files):

    global wt, bias, b, wt2
    c=1

    for i in range(30):

        for key, value in files.items():

            sum = 0

            if 'spam' in key:

                y = 0
                bias -= 1
                b -= c
            if 'ham' in key:

                y = 1
                bias += 1
                b += c

            wlist=Counter(value)

            for item, val in wlist.items():

                sum+=wt[item]*val

            error=y-unitstep(sum)

            if error!=0:

                for item, val in wlist.items():

                    wt[item]+=error*val
                    wt2[item]+=error*val*c

            c+=1

    for item in wt:

        wt[item]-=wt2[item]/c

    wt[' ']=unitstep(bias-b/c)

files=filelist(asd)

wt2=wt

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

avgperlearn(files2)
'''

avgperlearn(files)

f=open('per_model.txt', 'w')
f.write(str(wt))
f.close()