#!/usr/bin/python3
# Author: Suzanna Sia
# Credits: Ayush Dalmia

# Standard imports
#import random
import numpy as np
#import pdb
import math
import os, sys

# argparser
import argparse
import pdb
#from distutils.util import str2bool

# Custom imports
import dataloader

def main():

    topic_words = dataloader.load_topic_words(args.topic_wordf)
    word_doc_counts = dataloader.load_word_docids(args.word_docf)

    if args.nfiles==0:
        total_docs = set()
        for word in word_doc_counts.keys():
            total_docs = total_docs.union(word_doc_counts[word])

        print("nfiles not provided - calculating from dataset:", len(total_docs))
        args.nfiles = len(total_docs)

    average_npmi_topics(topic_words, args.ntopics, word_doc_counts, args.nfiles)

def average_npmi_topics(topic_words, ntopics, word_doc_counts, nfiles):

    eps = 10**(-12)
    
    all_topics = []
    for k in range(ntopics):
        word_pair_counts = 0
        topic_score = []

        ntopw = len(topic_words[k])

        if ntopw<2:
            sys.exit("number of words in cluster less than 2.. fix your cluster..")

        for i in range(ntopw-1):
            for j in range(i+1, ntopw):
                w1 = topic_words[k][i]
                w2 = topic_words[k][j]

                w1w2_dc = len(word_doc_counts.get(w1, set()) & word_doc_counts.get(w2, set()))
                w1_dc = len(word_doc_counts.get(w1, set()))
                w2_dc = len(word_doc_counts.get(w2, set()))

                # what we had previously:
                #pmi_w1w2 = np.log(((w1w2_dc * nfiles) + eps) / ((w1_dc * w2_dc) + eps))

                # Correct eps:

                pmi_w1w2 = np.log((w1w2_dc * nfiles) / ((w1_dc * w2_dc) + eps) + eps)
                npmi_w1w2 = pmi_w1w2 / (- np.log( (w1w2_dc)/nfiles + eps))

                # Which is equivalent to this:
                #if w1w2_dc ==0: 
                #    npmi_w1w2 = -1
                #else:
                #    pmi_w1w2 = np.log( (w1w2_dc * nfiles)/ (w1_dc*w2_dc))
                #    npmi_w1w2 = pmi_w1w2 / (-np.log (w1w2_dc/nfiles))


                if npmi_w1w2>1 or npmi_w1w2<-1:
                    #print(f"warning: NPMI score not bounded for:{w1}, {w2}, \
                    #        score:{np.around(npmi_w1w2, 5)} ... rounding off")

                    if npmi_w1w2 > 1:
                        npmi_w1w2 = 1
                    elif npmi_w1w2 <-1:
                        npmi_w1w2 = -1

                topic_score.append(npmi_w1w2)

        all_topics.append(np.mean(topic_score))
    
    for k in range(ntopics):
        print(np.around(all_topics[k],5), " ".join(topic_words[k]))

    avg_score = np.around(np.mean(all_topics), 5)
    print(f"\nAverage NPMI for {ntopics} topics: {avg_score}")

    return avg_score


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--nfiles', type=int, default=0)
    parser.add_argument('--topic_wordf', type=str)
    parser.add_argument('--word_docf', type=str)
    parser.add_argument('--ntopics', type=int)
    args = parser.parse_args()


    main()
