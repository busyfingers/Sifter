#!/usr/bin/python -tt

'''
Created on Dec 5, 2012

@author: niklas
'''

import re

def fixChrName(chrName):
    chrMatch = re.match(r'chr(.*)', chrName)
    if chrMatch:
        return chrMatch.group(1)
    else:
        return chrName

def createRefList(controlFile):
    
    refList = []
    FH_CONTROL = open(controlFile, "rU")

    for line in FH_CONTROL:
        if not re.search(r'^#', line):

            splitline = line.split('\t')
            
            chr1 = fixChrName(splitline[0])
            start = float(splitline[1])
            chr2 = fixChrName(splitline[3])
            end = float(splitline[4])
            
            refList.append([chr1, start, chr2, end])

    FH_CONTROL.close()
    return sorted(refList)
    

def main(inputFile, outputFile, controlFile, minScore_):
    
    FH_INPUT = open(inputFile, "rU")
    FH_OUTPUT = open(outputFile, "w")
    refList = createRefList(controlFile)
    
    nbrOfSVs = 0
    overlaps = 1
    
    for line in FH_INPUT:
        
        matched = "NA"
        
        if not re.search(r'^#', line):
            
            splitline = line.split('\t')
            chr1_in = fixChrName(splitline[0])
            start_in = float(splitline[1])
            chr2_in = fixChrName(splitline[3])
            end_in = float(splitline[4])
            
            for ref in refList:
                             
                if ref[0] == chr1_in:

                    ## Found the correct chromosome, compare start and end positions
                                        
                    ## Case I
                    if ref[1] >= start_in and ref[1] <= end_in and ref[3] >= end_in:
                        if matched == "NA" or matched == False:
                            matched = True
                            overlaps += 1
                            overlap = str(round( (end_in-ref[1])/(end_in-start_in), 2))
                            FH_OUTPUT.write(line.rstrip("\n") + "\t" + overlap + "\n")
                        
                            print "Match: " + str(matched) + " sample " + str(chr1_in) + " " + str(start_in) + "-" + str(end_in) + " ref " + str(ref[0]) + " " + str(ref[1]) + "-" + str(ref[3]) + " Overlap: " + str(overlap)
                    
                    ## Case II
                    elif ref[3] <= end_in and ref[3] >= start_in and ref[1] <= start_in:
                        if matched == "NA" or matched == False:
                            matched = True
                            overlaps += 1
                            overlap = str(round( (ref[3]-start_in)/(end_in-start_in), 2))
                            FH_OUTPUT.write(line.rstrip("\n") + "\t" + overlap + "\n")
                        
                            print "Match: sample " + str(chr1_in) + " " + str(start_in) + "-" + str(end_in) + " ref " + str(ref[0]) + " " + str(ref[1]) + "-" + str(ref[3]) + " Overlap: " + str(overlap)
                    
                    ## Case III
                    elif ref[1] <= start_in and ref[3] >= end_in:
                        if matched == "NA" or matched == False:
                            matched = True
                            overlaps += 1
                            overlap = str(1)
                            FH_OUTPUT.write(line.rstrip("\n") + "\t" + overlap + "\n")
                        
                            print "Match: sample " + str(chr1_in) + " " + str(start_in) + "-" + str(end_in) + " ref " + str(ref[0]) + " " + str(ref[1]) + "-" + str(ref[3]) + " Overlap: " + str(overlap)
                        
                    ## Case IV
                    elif ref[1] >= start_in and ref[3] <= end_in:
                        if matched == "NA" or matched == False:
                            matched = True
                            overlaps += 1
                            overlap = str(round( (ref[3]-ref[1])/(end_in-start_in), 2))
                            FH_OUTPUT.write(line.rstrip("\n") + "\t" + overlap + "\n")
                        
                            print "Match: sample " + str(chr1_in) + " " + str(start_in) + "-" + str(end_in) + " ref " + str(ref[0]) + " " + str(ref[1]) + "-" + str(ref[3]) + " Overlap: " + str(overlap)

            
                    ## Non-overlap
                    else:
                        #print "No match: sample " + str(chr1_in) + " " + str(start_in) + "-" + str(end_in) + " ref " + str(ref[1]) + "-" + str(ref[3])
                        if matched == "NA":
                            matched = False

                
                
            if matched == False:
                overlap = str(0)
                FH_OUTPUT.write(line.rstrip("\n") + "\t" + overlap + "\n")        
                print "No match: sample " + str(chr1_in) + " " + str(start_in) + "-" + str(end_in) + " ref " + str(ref[0]) + " " + str(ref[1]) + "-" + str(ref[3]) + " Overlap: " + str(overlap)
                                
            nbrOfSVs += 1
               
    print "\nAll done!\n"
    print "Overlaps:", overlaps
    print "SVs in sample file:", nbrOfSVs
    print "Overlap percentage:", str(round(float(overlaps)/float(nbrOfSVs), 2) * 100) + "%"
                        
    FH_INPUT.close()
    FH_OUTPUT.close()
    
if __name__ == '__main__':
    main()