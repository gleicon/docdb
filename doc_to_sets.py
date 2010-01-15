#!/usr/bin/env python


if __name__ == '__main__':
    from collections import defaultdict
    import nltk
    import sys

    STOPWORDS = nltk.corpus.stopwords.words('english')
    p=nltk.stem.PorterStemmer()

    hist=defaultdict(lambda : 1)

    if len(sys.argv) > 1:
        for f in sys.argv[1:]:
            infile = open(f, 'r')
            while 1:
                output = ''
                word = ''
                line = infile.readline()
                if line == '':
                    break
                for c in line:
                    if c.isalpha():
                        word += c.lower()
                    else:
                        if word:
                            w = p.stem(word)
                            if word not in STOPWORDS: 
                                hist[w] = hist[w]+1
                            #output += p.stem(word, 0,len(word)-1)
                            output += w
                            word = ''
                        output += c.lower()
                #print output,
            infile.close()
            print len(hist)

#    for word in hist.keys():
#        print "%s : %d" % (word, hist[word])
