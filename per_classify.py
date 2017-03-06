import os
import sys


#All the commented code can be used to print performance information (prescision, recall and f1 score)
asd=sys.argv[1]
asd2=sys.argv[2]
nl = '\n'
skip = {'cmds'}
f=open('per_model.txt', 'r')
wt=eval(f.read())
f.close()

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
                    fileslist[fp]=stuff

    return(fileslist)

unitstep = lambda x: 0 if x<0 else 1

def perclassify(files):
    '''
    w = 0
    TPH = 0
    TNH = 0
    FPH = 0
    FNH = 0
    TPS = 0
    TNS = 0
    FPS = 0
    FNS = 0
    acc = 0
    '''
    global wt
    f = open(asd2, 'w')

    for key in files:

        #w+=1
        sum = 0
        wlist = {}

        if 'spam' in key:
            y = 0

        if 'ham' in key:
            y = 1

        words = files[key].split()

        for item in words:

            if item not in wlist:

                wlist[item] = 0

            wlist[item] += 1

        for item in wlist:

            sum += wt.get(item, 0) * wlist[item]

        sum+=wt[' ']

        if unitstep(sum)==1:

            f.write('HAM '+key+'\n')
            '''
            if y==0:

                FPH += 1
                FNS += 1

            if y==1:

                acc += 1
                TPH += 1
                TNS += 1
            '''
        if unitstep(sum) == 0:

            f.write('SPAM '+key+'\n')
            '''
            if y == 1:

                FNH += 1
                FPS += 1

            if y==0:

                acc += 1
                TPS += 1
                TNH += 1
            '''
    f.close()
    '''
    sprec = TPS / float(TPS + FPS)
    hprec = TPH / float(TPH + FPH)
    sreca = TPS / float(TPS + FNS)
    hreca = TPH / float(TPH + FNH)
    sfone = 2 * sprec * sreca / float(sprec + sreca)
    hfone = 2 * hprec * hreca / float(hprec + hreca)
    acc /= w
    print("Accuracy-", acc)
    print("SPAM:")
    print("Precision-", sprec)
    print("Recall-", sreca)
    print("F-score-", sfone)
    print("HAM:")
    print("Precision-", hprec)
    print("Recall-", hreca)
    print("F-score-", hfone)
    '''
perclassify(filelist(asd))