#!/usr/bin/python -tt

'''
Created on Dec 5, 2012

@author: niklas
'''

import re

def main(inputFile, outputFile, minSamples, controlID_, controlFilter_, minScore_):
    
    FH_INPUT = open(inputFile, "rU")
    FH_OUTPUT = open(outputFile, "w")
    controlID = controlID_
    controlFilter = controlFilter_
    
    for line in FH_INPUT:
        
        if not re.search(r'^#', line):
    
            splitline = line.split('\t')
            
            noControls = 0
            samples = splitline[10].split(':')
            
            for sample in samples:
                noControls += sample.count(controlID)
            
            noCases = len(splitline[10].split(':')) - noControls
            svScore = splitline[8]
            
            if controlFilter:
                if noCases == minSamples and noControls == 0:
                    if svScore >= minScore_:
                        FH_OUTPUT.write(line)
            
            else:
                if noCases == minSamples:
                    if svScore >= minScore_:
                        FH_OUTPUT.write(line)
                        
    FH_INPUT.close()
    FH_OUTPUT.close()
    
if __name__ == '__main__':
    main()