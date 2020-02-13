#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 13:48:08 2019

@author: jean

Purpose : Python script that wrap-up all the scripts of the downstream team in order to run all steps from one foldrec file to the final ranking.
"""
import argparse, sys, os, subprocess

sys.path.append('./code')
sys.path.append('code/scoring/dope') #on ajoute le path pour trouver les fichiers relatifs au score
sys.path.append('code/scoring/SBROD')
sys.path.append('code/scoring/Rosetta')
sys.path.append('code/scoring/hydrophobicity_stickiness')
#sys.path.append('code/scoring/SBROD/sbrod')


import argparse, scoring_dope, scoring_SBROD, rosettaScoring, scoring_hydrophobicity
import ajouterUnTitreQuiDechire2 as autqd
import processFoldrec
import time


def main():
    #argv management
    parser = argparse.ArgumentParser(description='Wrap-up of downstream scripts')
    
    parser.add_argument('foldrec_filepath', type = str, help="filepath of the foldrec to analyse (input).")
    parser.add_argument('homestrad_folderpath', type = str, help="folderpath of HOMESTRAD database used in the project.")
    parser.add_argument('model_filepath', type = str, default = "statistics_meta/Modele_glmfinal_glm.RData", help="filepath to the statisics trained model used to rank threaded pdb files.")
    parser.add_argument('output_filepath', type = str, default = "results.txt", help="filepath to the result txt file containing the ranking.")
    
    parser.add_argument('-pdb_folderpath', type = str, default='./pdbfiles', help="folderpath to store threaded pdb files.")
    parser.add_argument('-info_folderpath', type = str, default='./info.info', help="folderpath to store \"*.info\" file containing primary informations used later by the statistic part of the pipeline.")
    parser.add_argument('-csv_filepath', type = str, default='data_test.csv', help="filepath of csv file used by the statistic part of the pipeline.")
    parser.add_argument('-logfile_filepath', type = str, default = "downstream_makeAllPdb_log.txt", help="filepath to logfile of makeAllPdb() subpart of pipeline.")
    parser.add_argument('-dope_par_filepath', type = str, default = "./code/scoring/dope/dope.par", help="filepath of dope score matrix.")
    parser.add_argument('-dope_dist_threshold', type = float, default = 15.25, help="distance threshold for atoms to be considered neighbours (default = 15.25 A)")
    parser.add_argument('-sbrod', type = str, default='code/scoring/SBROD/sbrod', help="path to sbrod")
    
    parser.add_argument('-backbone_only', type = str, default="True", help = "don't rebuild side chain (this will speed up the method but some information about the pdb won't be gathered).")
    
    parser.add_argument('--delete_pdbfiles', action = "store_true", help = "[not avaliable yet]should threaded pdbfiles be deleted after the run.")
    parser.add_argument('--delete_infofiles', action = "store_true", help = "[not avaliable yet]should the info file be deleted after the run.")
    parser.add_argument('--delete_csvfiles', action = "store_true", help = "[not avaliable yet]should the csv file be deleted after the run.")
    
    args = parser.parse_args()
    
    
    if (args.backbone_only=="True"):
        rustine=True
    else:
        rustine=False
    
    
    start_time = time.time()
    
    #Step 1 : analysis of foldrec file, threading on master pdbfiles, rebuild of side chains using SWRL4, creation of "*.info" files and threaded pdb files
    processFoldrec.makeAllPdb(foldrecPath = args.foldrec_filepath,
                              homestradPath = args.homestrad_folderpath,
                              pathPDBOut = args.pdb_folderpath,
                              rebuildSideChain = not rustine,
                              #pathInfoOut = (args.info_folderpath + '/' + "info.info"),
                              pathInfoOut = args.info_folderpath,
                              outPdb=True,
                              log=args.logfile_filepath)
    
    #Step 2 : analysis of threaded pdbfiles and creation of one csv file containing all informations for each threaded pdb file
    """
    commandline_to_run = "./code/stat_traindata_table.py"
    
    commandline_to_run += " "
    commandline_to_run += args.info_folderpath
    
    commandline_to_run += " "
    commandline_to_run += args.pdb_folderpath
    
    commandline_to_run += " "
    commandline_to_run += args.csv_filepath
    
    commandline_to_run += " "
    commandline_to_run += args.dope_par_filepath
    
    commandline_to_run += " -dope_dist_threshold "
    commandline_to_run += str(args.dope_dist_threshold)
    
    commandline_to_run += " 1"#learn argument is a bit shady

    os.sys(commandline_to_run)
    """
   
    #var extraction
    dope_CAsubset_dict = scoring_dope.subset_DOPEini_todict(args.dope_par_filepath)
    
    print("paf")
    
    #subprocess.run(args=['./code/ajouterUnTitreQuiDechire2.py', args.info_folderpath, args.pdb_folderpath, args.csv_filepath, args.dope_par_filepath, "-dope_dist_threshold", str(args.dope_dist_threshold), "-sbrod", args.sbrod, "-rebuildSC", str(not args.backbone_only)])
    autqd.processOneFile(args.info_folderpath, args.pdb_folderpath, args.csv_filepath, dope_CAsubset_dict, args.dope_dist_threshold, args.sbrod,  not rustine)
    
    #Step 3 : ranking of treated pdb files by applying a statistic trained model using the csv file
    """
    commandline_to_run = "./statisics_meta/Scoring_logistique.R"
    
    commandline_to_run += " -i "
    commandline_to_run += args.csv_filepath
    
    commandline_to_run += " -m "
    commandline_to_run += args.model_filepath
    
    commandline_to_run += " -o "
    commandline_to_run += args.output_filepath
    
    os.sys(commandline_to_run)
    """
    subprocess.call(args=["Rscript", "./statistics_brand_new/Scoring_logistique.R", "-i", args.csv_filepath, '-m', args.model_filepath, "-o", args.output_filepath])
   
    print("Temps d execution : %s secondes ---" % (time.time() - start_time))
    return(0)


if __name__ == "__main__":
    main()