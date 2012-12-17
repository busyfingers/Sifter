#!/usr/bin/python -tt

'''
Created on Dec 5, 2012

@author: niklas
'''

import argparse
import bdfilter
import sys

def main():
    
    argparser = argparse.ArgumentParser()
    
    argparser.add_argument("input",
                           help="Path to the input file.")

    argparser.add_argument("control",
                           help="A comparison file that contains SVs that should be disregarded if they exist in the input, i.e. a file with the SVs in the control group.")
    
    argparser.add_argument("output",
                           help="Path to the output file.")
      
    argparser.add_argument("-minSamples",
                           type=int,
                           help="Minimum number of samples to share an SV.")
 
    argparser.add_argument("-known",
                           help="Path to a file containing known SVs.")

    
    argparser.add_argument("-minScore",
                           type=int,
                           help="Minimum score threshold (1-99)")
    
    args = argparser.parse_args()
    
    inputFile = args.input
    outputFile = args.output
    controlFile = args.control
    
    if args.known:
        known = args.known
    else:
        known = 0
    
    if args.minSamples:
        minSamples = args.minSamples
    else:
        minSamples = 1
    
    if args.minScore:
        minScore = args.minScore
    else:
        minScore = 30

    bdfilter.main(inputFile, outputFile, controlFile, minScore, minSamples, known)
        
        
if __name__ == '__main__':
    main()
