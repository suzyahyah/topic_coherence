#!/usr/bin/python3
# Author: Suzanna Sia

# Standard imports
#import random
#import numpy as np
#import pdb
#import math
#import os, sys

# argparser
#import argparse
#from distutils.util import str2bool
#argparser = argparser.ArgumentParser()
#argparser.add_argument('--x', type=float, default=0)
import pdb
# Custom imports

def load_topic_words(topic_wordf):
    DELIM = ","

    with open(topic_wordf, 'r') as f:
        topic_words = f.readlines()

    topic_words = [tw.strip().replace(DELIM,'').split() for tw in topic_words]

    return topic_words


def load_word_docids(word_dcf):
    DELIM1 = "\t"
    DELIM2 = ";"

    word_dc = {}
    with open(word_dcf, 'r') as f:
        data = f.readlines()

    for line in data:
        word, docids = line.split(DELIM1)
        word_dc[word] = set(docids.strip().split(DELIM2))
    
    return word_dc



