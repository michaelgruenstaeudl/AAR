#!/usr/bin/env python2
''' Conducting Ancestral State Reconstructions (ASRs) with Mesquite'''
__author__ = "Michael Gruenstaeudl, PhD"
__copyright__ = "Copyright (C) 2015 Michael Gruenstaeudl"
__email__ = "mi.gruenstaeudl@gmail.com"
__version__ = "2015.10.08.1500"

# IMPORT OPERATIONS
from prettytable import PrettyTable
from subprocess import Popen, PIPE
from termcolor import colored
import argparse
import csv
import dendropy
import numpy
import os
import sys
import time
import GeneralFileOperations as GFO
import GeneralStringOperations as GSO

# DEBUG HELPER
#import pdb
#pdb.set_trace()

# GLOBAL VARIABLES
bayesModel = "Begin MESQUITE;\n\tMESQUITESCRIPTVERSION 2;\n\tTITLE AUTO;\n\ttell ProjectCoordinator;\n\tgetEmployee #mesquite.minimal.ManageTaxa.ManageTaxa;\n\ttell It;\n\t\tsetID 0 111; \n\tendTell;\n\tgetEmployee #mesquite.charMatrices.ManageCharacters.ManageCharacters;\n\ttell It;\n\t\tsetID 0 222; \n\tendTell;\n\tString.resultsFile 'RAWRESULTS_treeID_reconstID.txt';\n\tgetWindow;\n\tgetEmployee  #mesquite.trees.BasicTreeWindowCoord.BasicTreeWindowCoord; \n\ttell It;\n\t\tmakeTreeWindow #111  #mesquite.trees.BasicTreeWindowMaker.BasicTreeWindowMaker; \n\t\ttell It;\n\t\t\tsetTreeSource  #mesquite.trees.StoredTrees.StoredTrees; \n\t\t\ttell It;\n\t\t\t\tsetTreeBlock 2;\n\t\t\t\ttoggleUseWeights off;\n\t\t\tendTell;\n\t\t\tgetTreeWindow;\n\t\t\t\ttell It;\n\t\t\t\t\tsetTreeNumber 1; \n\t\t\t\t\tnewAssistant  #mesquite.ancstates.TraceCharOverTrees.TraceCharOverTrees;\n\t\t\t\t\ttell It;\n\t\t\t\t\t\tsuppress;\n\t\t\t\t\t\tsetHistorySource  #mesquite.ancstates.RecAncestralStates.RecAncestralStates;\n\t\t\t\t\t\ttell It;\n\t\t\t\t\t\t\tgetCharacterSource  #mesquite.charMatrices.CharSrcCoordObed.CharSrcCoordObed;\n\t\t\t\t\t\t\ttell It;\n\t\t\t\t\t\t\t\tsetCharacterSource #mesquite.charMatrices.StoredCharacters.StoredCharacters;\n\t\t\t\t\t\t\t\t\ttell It;\n\t\t\t\t\t\t\t\t\t\tsetDataSet #222;\n\t\t\t\t\t\t\t\t\tendTell;\n\t\t\t\t\t\t\t\tendTell;\n\t\t\t\t\t\t\tsetMethod  #mesquite.stochchar.StochCharMapper.StochCharMapper;\n\t\t\t\t\t\t\ttell It;\n\t\t\t\t\t\t\t\tsetModelSource  #mesquite.stochchar.CurrentProbModels.CurrentProbModels;\n\t\t\t\t\t\t\t\tgetEmployee #mesquite.stochchar.zMargLikeCateg.zMargLikeCateg;\n\t\t\t\t\t\t\t\ttell It;\n\t\t\t\t\t\t\t\t\tsetReportMode Proportional_Likelihoods;\n\t\t\t\t\t\t\t\t\tsetRootMode Use_Root_State_Frequencies_as_Prior;\n\t\t\t\t\t\t\t\t\tsetDecision 2.0;\n\t\t\t\t\t\t\t\t\tsetUnderflowCheckFreq 2;\n\t\t\t\t\t\t\t\tendTell;\n\t\t\t\t\t\t\tendTell;\n\t\t\t\t\t\tendTell;\n\t\t\t\t\t\tsetCharacter 1;\n\t\t\t\t\t\tsetTreeSource  #mesquite.trees.StoredTrees.StoredTrees;\n\t\t\t\t\t\ttell It;\n\t\t\t\t\t\t\tsetTreeBlock 1;\n\t\t\t\t\t\t\ttoggleUseWeights off;\n\t\t\t\t\t\tendTell;\n\t\t\t\t\t\tsetNumTrees 100;\n\t\t\t\t\t\tsetMode Count_All_Trees_with_State;\n\t\t\t\t\t\tdesuppress;\n\t\t\t\t\tendTell; \n\t\t\t\tendTell; \n\t\t\t\ttell It;\n\t\t\t\t\ttext;\n\t\t\t\tendTell;\n\t\t\tendTell; \n\t\tendTell; \n\tendTell;\n\tcloseFileAfterRead;\nend;\n"
likeModel = "Begin MESQUITE;\n\tMESQUITESCRIPTVERSION 2;\n\tTITLE AUTO;\n\ttell ProjectCoordinator;\n\tgetEmployee #mesquite.minimal.ManageTaxa.ManageTaxa;\n\ttell It;\n\t\tsetID 0 111; \n\tendTell;\n\tgetEmployee #mesquite.charMatrices.ManageCharacters.ManageCharacters;\n\ttell It;\n\t\tsetID 0 222; \n\tendTell;\n\tString.resultsFile 'RAWRESULTS_treeID_reconstID.txt';\n\tgetWindow;\n\tgetEmployee  #mesquite.trees.BasicTreeWindowCoord.BasicTreeWindowCoord; \n\ttell It;\n\t\tmakeTreeWindow #111  #mesquite.trees.BasicTreeWindowMaker.BasicTreeWindowMaker; \n\t\ttell It;\n\t\t\tsetTreeSource  #mesquite.trees.StoredTrees.StoredTrees; \n\t\t\ttell It;\n\t\t\t\tsetTreeBlock 2;\n\t\t\t\ttoggleUseWeights off;\n\t\t\tendTell;\n\t\t\tgetTreeWindow;\n\t\t\ttell It;\n\t\t\t\tsetTreeNumber 1; \n\t\t\t\tnewAssistant  #mesquite.ancstates.TraceCharOverTrees.TraceCharOverTrees;\n\t\t\t\ttell It;\n\t\t\t\t\tsuppress;\n\t\t\t\t\tsetHistorySource  #mesquite.ancstates.RecAncestralStates.RecAncestralStates;\n\t\t\t\t\ttell It;\n\t\t\t\t\t\tgetCharacterSource  #mesquite.charMatrices.CharSrcCoordObed.CharSrcCoordObed;\n\t\t\t\t\t\ttell It;\n\t\t\t\t\t\t\tsetCharacterSource #mesquite.charMatrices.StoredCharacters.StoredCharacters;\n\t\t\t\t\t\t\ttell It;\n\t\t\t\t\t\t\t\tsetDataSet #222;\n\t\t\t\t\t\t\tendTell;\n\t\t\t\t\t\tendTell;\n\t\t\t\t\t\tsetMethod  #mesquite.stochchar.MargProbAncStates.MargProbAncStates;\n\t\t\t\t\t\ttell It;\n\t\t\t\t\t\t\tsetModelSource  #mesquite.stochchar.CurrentProbModels.CurrentProbModels;\n\t\t\t\t\t\t\tgetEmployee #mesquite.stochchar.zMargLikeCateg.zMargLikeCateg;\n\t\t\t\t\t\t\ttell It;\n\t\t\t\t\t\t\t\tsetReportMode Proportional_Likelihoods;\n\t\t\t\t\t\t\t\tsetRootMode Use_Root_State_Frequencies_as_Prior;\n\t\t\t\t\t\t\t\tsetDecision 2.0;\n\t\t\t\t\t\t\t\tsetUnderflowCheckFreq 2;\n\t\t\t\t\t\t\tendTell;\n\t\t\t\t\t\tendTell;\n\t\t\t\t\tendTell;\n\t\t\t\t\tsetCharacter 1;\n\t\t\t\t\tsetTreeSource  #mesquite.trees.StoredTrees.StoredTrees;\n\t\t\t\t\ttell It;\n\t\t\t\t\t\tsetTreeBlock 1;\n\t\t\t\t\t\ttoggleUseWeights off;\n\t\t\t\t\tendTell;\n\t\t\t\t\tsetNumTrees 100;\n\t\t\t\t\tsetMode Count_All_Trees_with_State;\n\t\t\t\t\tdesuppress;\n\t\t\t\tendTell; \n\t\t\tendTell; \n\t\t\ttell It;\n\t\t\t\ttext;\n\t\t\tendTell;\n\t\tendTell; \n\tendTell; \n\tendTell;\n\tcloseFileAfterRead;\nend;\n"

# MODULES
def main(treedistrFn, plottreeFn, charsFn, charnum, rcnmdl, pathToSoftware):

# 1. Generating indata
    # 1.1. Setting outfilenames
    fileprfx = GSO.rmext(treedistrFn)
    outFn_raw = fileprfx + ".ASRviaMESQUITE.full"
    outFn_tree = fileprfx + ".ASRviaMESQUITE.tre"
    outFn_table = fileprfx + ".ASRviaMESQUITE.csv"

    # 1.2. Load infiles
    treedistr = GFO.loadR(treedistrFn).lower()
    plottree = GFO.loadR(plottreeFn).lower()
    
    # 1.3. Parse treedistr
    try:
        pos = treedistr.find("begin trees;") + len("begin trees;")
        treedistrH = treedistr[:pos] + '\nTitle "block1"' + treedistr[pos:]
    except: 
        print colored("  Warning: ", "magenta"), "Something wrong with treedistr!"
        
    # 1.4. Parse plottree
    plottreeH = plottree.strip("#nexus")
    try:
        pos = plottreeH.find("end;", plottreeH.find("begin taxa;")) + len("end;")
    except: 
        print colored("  Warning: ", "magenta"), "Something wrong with plottree!"
        pos = 0
    plottreeH = plottreeH[pos:]
    try:
        pos = plottreeH.find("begin trees;") + len("begin trees;")
        plottreeH = plottreeH[:pos] + '\nTitle "block2"' + plottreeH[pos:]
    except: 
        sys.exit(colored("  ERROR: ", "magenta") + "Something wrong with plottree!")

    # 1.5. Parse characters
    block1 = '\nBEGIN CHARACTERS;\nDIMENSIONS  NCHAR='
    block2 = ';\nFORMAT DATATYPE = STANDARD GAP = - MISSING = ? SYMBOLS = "'
    block3 = '";\nMATRIX\n'
    block4 = '\n;\nEND;\n'
    try:
        reader = csv.reader(open(charsFn, "r"), delimiter=",")
        matrx = numpy.array(list(reader))
        nchars = matrx.shape[1]-1
        n = int(charnum)
        symbls = set(matrx[:, n])
        p = PrettyTable()
        for row in matrx:
            p.add_row(row)
        matrxStr = p.get_string(header=False, border=False)
        chars = block1 + str(nchars) + block2 + " ".join(set(symbls)) + block3 + matrxStr + block4
    except: 
        sys.exit(colored("  ERROR: ", "magenta") + "Something wrong with parsing the characters!")


    # 1.6. Combine to indata
    inD = treedistrH + plottreeH + chars
    inD = inD.replace("#nexus", "#NEXUS")


# 2. Character Reconstruction
#   2.1. Decision on model
    if rcnmdl.lower() == "likelihood":
        mdl = likeModel
    if rcnmdl.lower() == "bayesian":
        mdl = bayesModel

#   2.2. Saving of tempfile
    tmpFn = GSO.randomword(6) + ".tmp"
    GFO.saveFile(tmpFn, "\n".join([inD, mdl]))                           # a temporary infile without underscores is generated, but deleted immediately after execution.

#   2.3. Execute and then delete tempfile
    print "  Character Reconstruction in Mesquite"
    print "  Selected Reconstruction Method:", rcnmdl
    startMesquite = "sh " + pathToSoftware
    p = Popen(startMesquite, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    time.sleep(5)                                                       # WIthout such waiting times, scripting Mesquite does not work.
    p.stdin.write("cd " + os.getcwd() + "/\n")                          # Can contain underscores
    time.sleep(2)
    p.stdin.write("openFile " + tmpFn + "\n")                           # Must not contain underscores, because Mesquite cannot load filenames containing underscores! Hence, I chose "tmp".
    time.sleep(45)
    p.stdin.write("quit\n")
    output, error = p.communicate()
    data_handle = [output, error]
    if not data_handle:
        sys.exit(colored("  ERROR: ", 'red') + "No reconstruction data from Mesquite received.")
    GFO.deleteFile(tmpFn)

#   2.4. Parsing out the relevant section of the reconstruction output and saving it to file
    mainD = GSO.exstr(data_handle[0], "Reading block: MESQUITE", "File reading complete")
    GFO.saveFile(outFn_raw, mainD)

#   2.5. More parsing of the reconstruction output for subsequent parsed_data generation
    keywds = ["Trace Character Over Trees", "Trace Character History"]
    for k in keywds:
        if k in mainD:
            mainD = mainD[mainD.find(k):]
    if "File reading complete" in mainD:
        mainD = mainD[mainD.find(k):]
    mainD = mainD[mainD.find("\nnode"):].splitlines()                    # This steps split the string into a list!
    mainD = filter(None, mainD)                                         # removing all empty elements of mainD
    if not mainD:
        sys.exit(colored("  ERROR: ", 'red') + "Parsing of reconstr. data unsuccessful. Possible issue: Malformed NEXUS file.")


# 3. Parsing the reconstruction output
    print "  Parsing of Reconstruction Data"
    alist = [elem.split("  ") for elem in mainD if elem]                # generating parsed_data; field delimiter: two whitespaces
    outD = []
    for i in alist:
        try:
            nodeN = GSO.exstr(i[0], 'node ', ':')
        except: 
            print colored("  Warning:", 'magenta'), "No node number information recovered!"
            pass
        try:
            Ntrees = GSO.exstr(i[1], 'Node in ', ' trees.')
        except: 
            print colored("  Warning:", 'magenta'), "No NofTrees information recovered!"
            pass
        try:
            tmp = i[2].split("each: ")[1]
            recon = tmp.replace(" ","")
            outD.append(",".join([nodeN] + [Ntrees] + [recon]))         # Must be inside a try-command to avoid breakage when no reconstr. info for node
        except: 
            print colored("  Warning:", 'magenta'), "No reconstruction information for node", nodeN
            pass
    outD = "\n".join(outD) # must be outside of loop

    if not outD:
        sys.exit(colored("  ERROR: ", 'red') + "Parsing of reconstruction data unsuccessful.")


# 4. Saving files to disk
#   4.1. Converting tree from nexus into newick
    treeH = dendropy.Tree.get_from_string(plottree, schema="nexus")     # Converting tree from nexus into newick format, because nexus format may contain translation table, which TreeGraph2 cannot parse
    plottree_newick = treeH.as_string(schema='newick')
    GFO.saveFile(outFn_tree, plottree_newick)

#   4.2. Save table
    GFO.saveFile(outFn_table, outD)


# EXECUTE

print ""
print colored("  Script name: "+sys.argv[0], 'cyan')
print colored("  Author: "+__author__, 'cyan')
print colored("  Version: "+__version__, 'cyan')
print colored("  Notes:", 'yellow')
print colored("  1. Mesquite cannot perform reconstruction if missing data.", 'yellow')
print colored("  2. Mesquite cannot open filenames with underscores.", 'yellow')
print ""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Performing ASR with Mesquite; 2015 Michael Gruenstaeudl')
    parser.add_argument('-t', '--treedistr',
                        help='/path_to_working_dir/treedistr.nex',
                        required=True)
    parser.add_argument('-p', '--plottree',
                        help='/path_to_working_dir/plottree.nex',
                        required=True)
    parser.add_argument('-c', '--chars',
                        help='/path_to_working_dir/characters.csv',
                        required=True)
    parser.add_argument('-n', '--charnumber',
                        help='which character to use (e.g. 1)',
                        default='1',
                        required=True)
    parser.add_argument('-m', '--reconmodel',
                        help='likelihood, bayesian',
                        default='likelihood',
                        required=True)
    parser.add_argument('-s', '--software',
                        help='/path_to_program/mesquite.sh',
                        required=True,
                        default='/home/michael_science/binaries/mesquite3.03/mesquite.sh')
    args = parser.parse_args()

main(args.treedistr, args.plottree, args.chars, args.charnumber, args.reconmodel, args.software)

print ""
print colored("  Done.", 'cyan')
print ""