## Project Presentation

This repository is the work from the Team 9 - Downstream for the scholar project [Meet-U 2020](https://www.meet-u.org/edition_2020.html).

This repository was made by :
- Pierre CHARPENTIER
- Yacine DJABALI
- Raphaël PARMENTIER
- Jean VENCIC

The subject is to propose a folding for an input protein sequence. 

To do this, a database of 1009 protein families based on the [HOMSTRAD database](https://mizuguchilab.org/homstrad/) is used. It is used to find the closest protein family to the input sequence and then use this protein family as a model for the folding.

The project is separated in two parts :
- the Upstream Teams which role is to score the different protein families according to the analysis and alignment of the input sequence with each protein family of the database.
- the Downstream Teams which role is to use informations and especially the alignment of the input sequence with the consensus sequence of a protein family to propose a folding for the input sequence following the model of the chosen protein family.
 
See README_final.md for the merging of the two parts.

## Workflow

One foldrec file is taken as input and contains the scored alignment of the input protein sequence and each protein family.
As we need secondary structure prediction, the foldrec file must have the psiblast prediction.

From this file, several indicators are gathered for each protein family:

- (score) the score of the alignment
- (lengthRatio) the length ratio between the query and the template (query/template)
- (queryCoverage) the query coverage
- (ratioAAerasedOutStruct) the ratio of Amino Acid erased outside the structure of the template
- (ratioAAerasedInStruct) the ratio of Amino Acid erased inside the structure of the template
- (ratioAAMissingFromQuery) the ratio of query's Amino Acid missing in the output
- (ratioNbTrou) the ratio of gaps
- (meanSizetrou) the mean size of gaps

Then the alignement of the input sequence with the protein family sequence is used to naively thread the input sequence on the folding of the protein family sequence (in a backbone only pdb file format).

Then several new indicators are gathered from the generated backbone pdb files (called threaded pdb files) :

- (dope) dope score
- (SBROD) SBROD score

Since the generated pdb file are only backbone, we decided to rebuild the side chains usnig the software [SCWRL4](http://dunbrack.fccc.edu/SCWRL3.php/). This rebuild allow us to gather new indicators (mainly Pyrosetta scores) :

- (fa_atr) full-atom attractive score
- (fa_rep) full-atom repulsive score
- (fa_sol) full-atom solvation score
- (fa_intre_rep) full-atom. intraresidue rep. score
- (fa_elec) full-atom electronic score
- (pro_close) proline closure
- (hbond_sr_bb) short-range hbonding
- (hbond_lr_bb) long-range hbonding
- (hbond_bb_sc) backbone-sidechain hbonding
- (hbond_sc) sidechain-sidechain hbonding
- (dslf_fa13) disulfide full-atom score
- (total) the sum of the previous score (purpose analysis)

We calculate also our hydrophobic score (purpose analysis)

- (hydrophobicity) our hydrophobic score

All those indicators gathered at different steps of the workflow and for each protein family will be stored in a csv file.

Finally a previously trained statistical model will score (and therefore rank) the threaded pdb files using a selected subset of the variables contained in the csv file.

## Statistical models

To rank the built pbd files, Generalized Linear Model (GLM) were trained on a subset of the foldrec files of the benchmark. Since the pre-score avaliable in the foldrec (given by ORION in the benchmark) was very robust, we wanted to train glm using this score as a variable and also glm not using it as it may be less robust coming from the upstream team. Moreover, our project uses SCWRL4 to rebuild the side-chain of the pdb files which results in a longer process time. To make this process optional we needed to train glm using the variables avaliable with the side-chains and glm not using those variables.

We ended up with 4 statistical models :
- with score and with side-chain : Modele_glmfinal_glm.RData
- with score and without side-chain : Modele_sanschaine_glm.RData
- without score and with side-chain : Modele_sansscore_glm.RData
- without score and without side-chain : Modele_sansscore_sanschaine_glm.RData

All those models are avaliable in the sub-directory 2019---2020-Equipe-9/statistics_brand_new/Modèles_stats/

## Dependances

### Python 3.6
specific libraries :
- pyrosetta

you will need an academic licence, you can get one here:  
[pyrosetta licence](https://els.comotion.uw.edu/express_license_technologies/pyrosetta)  
then follow these instructions to install it:  
[install pyrosetta](http://www.pyrosetta.org/dow)  

### R 3.4.4
specific libraries :
- optparse

please install those libraries inside your R environnement using the command :
`>install.packages("library_name")`

### Softwares

##### SBROD

we use sbrod scoring in our program, it is include in the program.

##### SCWRL4

you will need an academic licence, you can get one here:  
[scwrl4 licence](http://dunbrack.fccc.edu/scwrl4/license/index.html)  
then download it and install it:  
[install scwrl4](http://dunbrack.fccc.edu/SCWRL3.php/#installation)  
finally you'll have to add scwrl4 to your linux environment, the command line to do so will be :  
`echo 'export PATH=$PATH:/home/user/scwrl4' >> /home/user/.bashrc`
or add directly 'export PATH=$PATH:/home/user/scwrl4' at the end of your .bashrc file  

## Usage

Download the project using the command :

`git clone https://github.com/meetU-MasterStudents/2019---2020-Equipe-9.git`


Be sure to give access and execution rights to all scripts and files in the project with the command :

`chmod 777 2019---2020-Equipe-9`


Terminal run :

`$ ./wrap-up.py foldrec_filepath homestrad_folderpath statistic_model_filepath output_filepath`

Arguments are avaliable with : `$ ./wrap-up.py -h`

## References

[SCWRL4](https://www.ncbi.nlm.nih.gov/pubmed/19603484) : Krivov GG, Shapovalov MV, Dunbrack RL., Jr Improved prediction of protein side-chain conformations with scwrl4. Protein. 2009 dec;77(4):778–95.
