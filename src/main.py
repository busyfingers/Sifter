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
    
#    argparser.add_argument("type",
#                           help="Input file type. [bd|bdf] (BreakDancer|BreakDancer_filtered).")
#    
#    argparser.add_argument("-minSamples",
#                           type=int,
#                           help="Minimum number of samples to share an SV.")
#    
#    argparser.add_argument("-controlID",
#                           help="A common name or partial name that can be used to identify the control samples.")
#    
#    argparser.add_argument("-controlFilter",
#                           action="store_true",
#                           help="Enable to exclude SVs that occurs in the controls.")
#
    argparser.add_argument("-minScore",
                           type=int,
                           help="Minimum score threshold (1-99)")
    
    args = argparser.parse_args()
    
    inputFile = args.input
    outputFile = args.output
    controlFile = args.control
#    inputType = args.type
#    minSamples = args.minSamples
#    controlID = args.controlID
    
    if args.minScore:
        minScore = args.minScore
    else:
        minScore = 30
#    
#    if args.controlFilter:
#        controlFilter = True
#    else:
#        controlFilter = False
    
    #if inputType == "bd":
#        bdfilter.main(inputFile, outputFile, minSamples, controlID, controlFilter, minScore)
    bdfilter.main(inputFile, outputFile, controlFile, minScore)
        
#    elif inputType == "bdf":
#        bdcompare.main(inputFile, outputFile, )
    
#    else:
#        sys.exit("Invalid input type: " + inputType)
        
if __name__ == '__main__':
    main()
