#!/usr/bin/python -tt

'''
Created on Dec 5, 2012

@author: niklas
'''

import re
import sys

results = []

def fixChrName(chrName):
    chrMatch = re.match(r'chr(.*)', chrName)
    if chrMatch:
        return chrMatch.group(1)
    else:
        return chrName

def createRefList(controlFile, type_):
    print "[INFO] Preparing reference list (%s)..." % type_
    refList = []
    FH_CONTROL = open(controlFile, "rU")

    if type_ == "bd":
        for line in FH_CONTROL:
            if not re.search(r'^#', line):
    
                splitline = line.split('\t')
                
                chr1 = fixChrName(splitline[0])
                start = float(splitline[1])
                chr2 = fixChrName(splitline[3])
                end = float(splitline[4])
                
                refList.append([chr1, start, chr2, end])
    
    elif type_ == "ucsc":
        for line in FH_CONTROL:
            if not re.search(r'^VariationID', line):
    
                splitline = line.split('\t')
                
                chr1 = fixChrName(splitline[2])
                start = float(splitline[3])
                chr2 = "NA"
                end = float(splitline[4])
                
                refList.append([chr1, start, chr2, end])
            
    else:
        sys.exit("Incorrect type: " + type_)
        

    FH_CONTROL.close()
    return sorted(refList)

def keepOnlyCommon(inputFile_, minSamples_):
    print "[INFO] Filtering input on only common SVs ..."
    FH_INPUT = open(inputFile_, "rU")
    inputFile = inputFile_ + "-onlycommon"
    FH_OUTPUT = open(inputFile, "w")
    
    for line in FH_INPUT:
        if not re.search(r'^#', line):
            splitline = line.split('\t')
                        
            noCases = len(splitline[10].split(':'))
            #svScore = splitline[8]
            
            if noCases == minSamples_:
                FH_OUTPUT.write(line)
    
    FH_INPUT.close()
    FH_OUTPUT.close()
    return inputFile

def getRowInfo(splitline, type_):
    if type_ == "bd":
        chr1_in = fixChrName(splitline[0])
        start_in = float(splitline[1])
        chr2_in = fixChrName(splitline[3])
        end_in = float(splitline[4])
        return (chr1_in, start_in, chr2_in, end_in)
    
    elif type_ == "ucsc":
        chr1_in = fixChrName(splitline[0])
        start_in = float(splitline[1])
        chr2_in = "NA"
        end_in = float(splitline[4])    
        return (chr1_in, start_in, chr2_in, end_in)
    
    else:
        sys.exit("Incorrect type: " + type_)

def writeOutput(outputFile_, results):

    FH_OUTPUT = open(outputFile_, "w")
    
    for result in results:
        for element in result:
            #print element
            FH_OUTPUT.write(element)
        FH_OUTPUT.write("\n")
    
    FH_OUTPUT.close()


def checkAllSVs(inputFile, outputFile_, controlFile_, minScore_, minSamples_, type_):
    refList = createRefList(controlFile_, type_)
    
    if type_ == "bd":
        print "[INFO] Comparing SVs against reference control ..."
    
    elif type_ == "ucsc":
        print "[INFO] Comparing SVs against known variants ..."

    FH_INPUT = open(inputFile, "rU")
    
#    if type_ == "bd":
#        FH_OUTPUT = open(outputFile_, "w")
#    
#    elif type_ == "ucsc":
#        FH_OUTPUT = open(outputFile_, "a")
#
#    
#    else:
#        sys.exit("Error opening output file." + type_)
     
    nbrOfSVs = 0
    overlaps = 0
    
    for line in FH_INPUT:
        
        if nbrOfSVs % 1000 == 0 and nbrOfSVs > 0:
            print "[INFO] Progress:", nbrOfSVs, "SVs compared"
        
        matched = "NA"
        
        if not re.search(r'^#', line):
            splitline = line.split('\t')
            
            rowInfo = getRowInfo(splitline, type_)
            
            chr1_in = fixChrName(rowInfo[0])
            start_in = float(rowInfo[1])
            chr2_in = "NA"
            end_in = float(rowInfo[3])
                       
            for ref in refList:
                             
                if ref[0] == chr1_in:
                    ## Found the correct chromosome, compare start and end positions
                                        
                    ## Case I
                    if ref[1] >= start_in and ref[1] <= end_in and ref[3] >= end_in:
                        if matched == "NA" or matched == False:
                            matched = True
                            overlaps += 1
                            overlap = str(round( (end_in-ref[1])/(end_in-start_in), 2))
                            
                            rowRes = [line.rstrip("\n") + "\t" + overlap]
                            
                            if type_ == "bd":
                                results.append(rowRes)
                            elif type_ == "ucsc":
                                results[nbrOfSVs].append("\t" + overlap)
                            else:
                                sys.exit("Error storing results. Exiting ...")
                            
                            #writeRow(FH_OUTPUT, overlap, line, type_)
                            
                            #FH_OUTPUT.write(line.rstrip("\n") + "\t" + overlap + "\n")
                        
                            #print "Match: " + str(matched) + " sample " + str(chr1_in) + " " + str(start_in) + "-" + str(end_in) + " ref " + str(ref[0]) + " " + str(ref[1]) + "-" + str(ref[3]) + " Overlap: " + str(overlap)
                    
                    ## Case II
                    elif ref[3] <= end_in and ref[3] >= start_in and ref[1] <= start_in:
                        if matched == "NA" or matched == False:
                            matched = True
                            overlaps += 1
                            overlap = str(round( (ref[3]-start_in)/(end_in-start_in), 2))
                            
                            rowRes = [line.rstrip("\n") + "\t" + overlap]
                            
                            if type_ == "bd":
                                results.append(rowRes)
                            elif type_ == "ucsc":
                                results[nbrOfSVs].append("\t" + overlap)
                            else:
                                sys.exit("Error storing results. Exiting ...")                       
                            
                            #writeRow(FH_OUTPUT, overlap, line, type_)
                            
                            #FH_OUTPUT.write(line.rstrip("\n") + "\t" + overlap + "\n")
                        
                            #print "Match: sample " + str(chr1_in) + " " + str(start_in) + "-" + str(end_in) + " ref " + str(ref[0]) + " " + str(ref[1]) + "-" + str(ref[3]) + " Overlap: " + str(overlap)
                    
                    ## Case III
                    elif ref[1] <= start_in and ref[3] >= end_in:
                        if matched == "NA" or matched == False:
                            matched = True
                            overlaps += 1
                            overlap = str(1)

                            rowRes = [line.rstrip("\n") + "\t" + overlap]
                            
                            if type_ == "bd":
                                results.append(rowRes)
                            elif type_ == "ucsc":
                                results[nbrOfSVs].append("\t" + overlap)
                            else:
                                sys.exit("Error storing results. Exiting ...")
                            
                            #writeRow(FH_OUTPUT, overlap, line, type_)
                            
                            #FH_OUTPUT.write(line.rstrip("\n") + "\t" + overlap + "\n")
                        
                            #print "Match: sample " + str(chr1_in) + " " + str(start_in) + "-" + str(end_in) + " ref " + str(ref[0]) + " " + str(ref[1]) + "-" + str(ref[3]) + " Overlap: " + str(overlap)
                        
                    ## Case IV
                    elif ref[1] >= start_in and ref[3] <= end_in:
                        if matched == "NA" or matched == False:
                            matched = True
                            overlaps += 1
                            overlap = str(round( (ref[3]-ref[1])/(end_in-start_in), 2))

                            rowRes = [line.rstrip("\n") + "\t" + overlap]
                            
                            if type_ == "bd":
                                results.append(rowRes)
                            elif type_ == "ucsc":
                                results[nbrOfSVs].append("\t" + overlap)
                            else:
                                sys.exit("Error storing results. Exiting ...")
                            
                            #writeRow(FH_OUTPUT, overlap, line, type_)
                            
                            #FH_OUTPUT.write(line.rstrip("\n") + "\t" + overlap + "\n")
                        
                            #print "Match: sample " + str(chr1_in) + " " + str(start_in) + "-" + str(end_in) + " ref " + str(ref[0]) + " " + str(ref[1]) + "-" + str(ref[3]) + " Overlap: " + str(overlap)   
            
                    ## Non-overlap
                    else:
                        #print "No match: sample " + str(chr1_in) + " " + str(start_in) + "-" + str(end_in) + " ref " + str(ref[1]) + "-" + str(ref[3])
                        if matched == "NA":
                            matched = False
    
                else:
                    if matched == "NA":
                        matched = False

                
            if matched == False:
                overlap = str(0)
                
                rowRes = [line.rstrip("\n") + "\t" + overlap]
                
                if type_ == "bd":
                    results.append(rowRes)
                elif type_ == "ucsc":
                    results[nbrOfSVs].append("\t" + overlap)
                else:
                    sys.exit("Error storing results. Exiting ...")

                #writeRow(FH_OUTPUT, overlap, line, type_)
                
                #FH_OUTPUT.write(line.rstrip("\n") + "\t" + overlap + "\n")        
                #print "No match: sample " + str(chr1_in) + " " + str(start_in) + "-" + str(end_in) + " ref " + str(ref[0]) + " " + str(ref[1]) + "-" + str(ref[3]) + " Overlap: " + str(overlap)
                                
            nbrOfSVs += 1
    
    print "\n[INFO] All done!\n"
    print "[INFO] Overlaps:", overlaps
    print "[INFO] SVs in sample file:", nbrOfSVs
    print "[INFO] Overlap percentage:", str(round(float(overlaps)/float(nbrOfSVs), 2) * 100) + "%\n"
                        
    FH_INPUT.close()



def main(inputFile_, outputFile_, controlFile_, minScore_, minSamples_, known_):
    
    if minSamples_ > 1:

        inputFile = keepOnlyCommon(inputFile_, minSamples_)
        checkAllSVs(inputFile, outputFile_, controlFile_, minScore_, minSamples_, "bd")
        if known_:
            checkAllSVs(inputFile, outputFile_, known_, minScore_, minSamples_, "ucsc")
        
    
    else:
        checkAllSVs(inputFile_, outputFile_, controlFile_, minScore_, minSamples_, "bd")
        if known_:
            checkAllSVs(inputFile, outputFile_, known_, minScore_, minSamples_, "ucsc")


    writeOutput(outputFile_, results)
    
if __name__ == '__main__':
    main()