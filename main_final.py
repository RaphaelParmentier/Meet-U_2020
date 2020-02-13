#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 11:17:51 2020

@author: jean

Purpose : Python script that manage both upstream and downstream main scripts

requirements under linux SE :

    Softwares
        $sudo apt install ncbi-blast+
        $sudo apt install muscle
        $sudo apt install mafft
        
        pyrosetta
            get a license here : https://els.comotion.uw.edu/express_license_technologies/pyrosetta
            follow the installation protocol here : http://www.pyrosetta.org/dow
        SCWRL4
            get a license here : http://dunbrack.fccc.edu/scwrl4/license/index.html
            follow the installation protocol here : http://dunbrack.fccc.edu/SCWRL3.php/installation
        
    Python libraries
        $pip install nump
        $pip install biopytho
        $pip install ra
        $pip install psutil
        $pip install tqdm
        $pip install joblib
        $pip install setproctitle

    R library
        (in R console)>install.packages("optparse")
"""

import argparse, os, subprocess, sys



def traiteAll(pathDirFasta, pathDirOut, databaseFilePath, HOMSTRAD, dirE6, modele, backbone=True):
    
    #part1 execute group6 code and create foldrec in the good place
    mainE6 = ('/').join([dirE6,"code/main.py"])
    formated = databaseFilePath.split('.')[0] + ".formated" 
    
    dirFoldrec = ('/').join([pathDirOut, "outputE6"])
    
    try:
        os.makedirs(dirFoldrec)
    except OSError:
        if not os.path.isdir(dirFoldrec): #on verfie que ce n'est pas un fichier
            raise
    
    arguments = ["python3", mainE6, pathDirFasta, dirFoldrec, databaseFilePath, formated]
    
    subprocess.run(args=arguments)
    
    #fin parti1
    
    #part2 creer dinamyquement les resultas en une arborescence dans outputdir
    
    print("preparation de l'environnement")
    dirFoldrec = dirFoldrec + "/emdApprox/foldrecs"
    
    print("recuperation de la liste des foldrecs")
    foldrecList = os.listdir(dirFoldrec)
    
    print("creation des repertoires de sorties")
    dirInfo = pathDirOut + '/info'
    try:
        os.makedirs(dirInfo)
    except OSError:
        if not os.path.isdir(dirInfo): #on verfie que ce n'est pas un fichier
            raise

    dirPDB = pathDirOut + '/pdb'
    try:
        os.makedirs(dirPDB)
    except OSError:
        if not os.path.isdir(dirPDB): #on verfie que ce n'est pas un fichier
            raise

    dirCSV = pathDirOut + '/csv'
    try:
        os.makedirs(dirCSV)
    except OSError:
        if not os.path.isdir(dirCSV): #on verfie que ce n'est pas un fichier
            raise
    
    dirResult = pathDirOut + '/result'
    try:
        os.makedirs(dirResult)
    except OSError:
        if not os.path.isdir(dirResult): #on verfie que ce n'est pas un fichier
            raise
    
    print("lancement de la boucle")
    for file in foldrecList:
        
        print("traitement de : " + file)
        
        #recuperation parametres
        foldrecFile = ('/').join([dirFoldrec, file])
        name = file.split('.')[0]
        infoOut = ('/').join([dirInfo, (name + '.info')])
        pdbDir = ('/').join([dirPDB, name])
        csvOut = ('/').join([dirCSV, (name + '.csv')])
        resultOut = ('/').join([dirResult, (name + '.txt')])
        wrap = 'wrap-up.py'
        
        back="True"
        if(backbone):
            back = "False"
        
        arguments=['python3',
                    wrap,
                    foldrecFile,
                    HOMSTRAD,
                    modele,
                    resultOut,
                    '-pdb_folderpath',
                    pdbDir,
                    '-info_folderpath',
                    infoOut,
                    '-csv_filepath',
                    csvOut,
                    '-backbone_only',
                    back
                ]
        print("execution du wrap_up pour : " + file)
        subprocess.run(args=arguments)
    
    #normalement si tout c'est bien passé c'est fini
    
    
def main():
    
    #argv management
    parser = argparse.ArgumentParser(description='Main script for executing upstream and downstream sub-main scripts')
    
    parser.add_argument('fasta_filepath', type = str, help="filepath of the multifasta file with the protein sequences to analyse.")
    parser.add_argument('upstream_database_filepath', type = str, help="filepath of a fasta database used by the upstream part to construct profile of the query sequences.")
    parser.add_argument('output_dirpath', type = str, help="directory path where pdb files and the ranking table will be written.")
    
    parser.add_argument('Homstrad', type = str, help="directory of homstrad")
    parser.add_argument('statistical_model_filepath', type = str, help="filepath of the trained statistical model (RData file) to use for pdb ranking.")
    
    parser.add_argument('-backbone_only', type = str,default = "False", help="if you need to rebuild side chain")
    parser.add_argument('-upstream_dirpath', type =str, default= os.path.dirname(os.path.realpath(__file__))+"../2019---2020-Equipe-6",help = "directory path of the downstream project (should be named \"2019---2020-Equipe-9\")")

    args = parser.parse_args()


    back=True
    if(args.backbone_only=="True"):
        back=False


    sys.path.append('2019---2020-Equipe-9/code')
    sys.path.append('2019---2020-Equipe-9/code/scoring/dope') #on ajoute le path pour trouver les fichiers relatifs au score
    sys.path.append('2019---2020-Equipe-9/code/scoring/SBROD')
    sys.path.append('2019---2020-Equipe-9/code/scoring/Rosetta')
    sys.path.append('2019---2020-Equipe-9/code/scoring/hydrophobicity_stickiness')

    #traiteAll(args.fasta_filepath, pathDirOut, databaseFilePath, HOMESTRAD, dirE6, dirE9, modele, backbone=True)
    traiteAll(args.fasta_filepath,
              args.output_dirpath,
              args.upstream_database_filepath,
              args.Homstrad,
              args.upstream_dirpath,
              args.statistical_model_filepath,
              backbone=back)


if __name__ == "__main__":
    main()