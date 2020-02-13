## Project Presentation

This repository is the work from the Team 9 - Downstream for the scholar project [Meet-U 2020](https://www.meet-u.org/edition_2020.html).

This repository was made by :
- Pierre CHARPENTIER
- Yacine DJABALI
- Raphaël PARMENTIER
- Jean VENCIC

The subject is to propose a folding for an input protein sequence. 

To do this, a database of 1009 protein families based on the [HOMSTRAD database](https://mizuguchilab.org/homstrad/) is used. It is used to find the closest protein family to the input sequence and then use this protein family as a model for the folding.

You can find a database for the first part [here] : ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz

## Workflow

One fasta file is taken as input.

This pipeline is composed of two part:
- the fasta file is take as input by team 6 code
- the result is taken by our code (see README.md)

##warning

- Due to some validity criteria, team 6 code is not able to make a foldrec if he can't find more than 30 homologues, if you don't have an output, try to take a bigger database.

## Statistical models

To rank the pdb, we have 4 statistical models available:
- with score and with side-chain : Modele_glmfinal_glm.RData
- with score and without side-chain : Modele_sanschaine_glm.RData
- without score and with side-chain : Modele_sansscore_glm.RData
- without score and without side-chain : Modele_sansscore_sanschaine_glm.RData

All those models are avaliable in the sub-directory 2019---2020-Equipe-9/statistics_brand_new/Modèles_stats/

## Dependances

All the dependance introduce to work our work fine (see README.md)

The [team 6 code] :(https://github.com/meetU-MasterStudents/2019---2020-Equipe-6.git)
And all its dependencies:

-ncbi-blast+ : sudo apt install ncbi-blast+
-muscle muscle : sudo apt install muscle
-mafft : sudo apt install mafft
-Python : Libraries
-numpy : pip install numpy
-biopython : pip install biopython
-ray : pip install ray
-psutil : pip install psutil
-tqdm : pip install tqdm
-joblib : pip install joblib

## Usage

Download the project using the command :

`git clone https://github.com/meetU-MasterStudents/2019---2020-Equipe-9.git`

and:

 git clone https://github.com/meetU-MasterStudents/2019---2020-Equipe-6.git`

Be sure to give access and execution rights to all scripts and files in the project with the command :

`chmod 777 2019---2020-Equipe-9`

Terminal run :

`$ python3 main_final.py (fasta_file) (database.fasta) (output_directory) (homestrad_directory) (modele_file) -upstream_path (path to team 6 directory) -backbone_only False

Arguments are avaliable with : `$ ./main_final.py -h`

## References

[SCWRL4](https://www.ncbi.nlm.nih.gov/pubmed/19603484) : Krivov GG, Shapovalov MV, Dunbrack RL., Jr Improved prediction of protein side-chain conformations with scwrl4. Protein. 2009 dec;77(4):778–95.
