---
title: 'Determining a novel feature-space for SARS-COV2 Sequence data'
tags:
  - Feature determination
  - k-mer modelling
  - word2vec
  - machine learning
  - epitope
  - CoVID-19
  - SARS-CoV-2
authors:
  - name: Lukas Heumos
    orcid: 0000-0002-8937-3457
    affiliation: 1
  - name: Ali Haider Bangash
    orcid: 0000-0002-8256-3194
    affiliation: 2
  - name: Fotis Psomopoulos
    orcid: 0000-0002-0222-4273
    affiliation: 3
  - name: Anastasios Togkousidis
    orcid: 0000-0003-4306-3709
    affiliation: 3
  - name: Phillip Davis
    orcid: 0000-0003-3562-4836
    affiliation: 4
  - name: Second Last
    orcid: 0000-0000-0000-0000
    affiliation: 3
affiliations:
 - name: University of Tübingen/Quantitative Biology Center,  Auf der Morgenstelle 10, Tübingen, Germany
   index: 1
 - name: Shifa College of Medicine, STMU, Islamabad, Pakistan
   index: 2
 - name: Institute of Applied Biosciences, Centre for Research and Technology Hellas, 6th km Charilaou-Thermis rd, Thessaloniki, Greece
   index: 3  
 - name: MRIGlobal, 425 Volker Boulevard, Kansas City, MO 64110, USA
   index: 4  
 - name: Institution 3, address, city, country
   index: 3  
date: 10 April 2020
bibliography: paper.bib
---

# Introduction

In late 2019, a previously unknown virus began spreading within the population of the Wuhan-city in the Hubei province of China [@Huang-Jan2020]. The virus, identified as a new type of coronavirus [@WHO-sitrep1], has since spread over the globe as a pandemic of an unprecedented scale [@WHO-press-pandemic,@WHO-sitrep78].

Through a global effort, a number of virus samples have been fully sequenced, with the data deposed in publicly accessible repositories, such as the [SARS-CoV-2 sequences GenBank](https://www.ncbi.nlm.nih.gov/genbank/sars-cov-2-seqs/) and the [EBI Data](https://www.ebi.ac.uk/ena/pathogens/covid-19).

Given the high similarity of the sequences, both at the aminoacid and the nucleotide level, a key question is how to identify interesting / discriminating features across the different sequences, so that the underling structure of the evolutionary story of the virus can be highlighted.

In order to address this question, the Machine Learning group of the [COVID-19 Biohackathon](https://github.com/virtual-biohackathons/covid-19-bh20), defined the following tasks:

- Identify potential features at the nucleotide level based on the k-mers (for various k)
- Identify potential features at the aminoacid level, based on the AA frequencies (and for various word sizes)
- Perform in-silico estimates of epitopes for COVID19
- Identify patterns in secondary structure (e.g. vs random sequences)

Each task, and the corresponding outputs are detailed below.

# Methods

## Potential features at the nucleotide level based on the k-mers

This approach focuses on the detection of k-mers that appear with high frequency in the data. The main dataset that was used for feature extraction is https://github.com/covid19-bh-machine-learning/master/blob/master/data/sars_cov_2_fixed.fasta and is actually a set of 281 genome sequences of SARS-CoV-2, each one consisting of approximately 30.000 nucleotides. The correspoding meta-data set is https://github.com/covid19-bh-machine-learning/master/blob/master/data/sars_cov_2_fixed_meta.csv and contains information about the length of each sequence, geographical location, isolation source, collection date of the sample etc.

The analysis that was conducted is an algorithmic procedure based on a pruning tree, which dymanically evaluates k-mers of different lengths and keeps those with the highest evaluation, while at the same time kmers with low evaluation are rejected. The evaluation parameter depends both on the length of each k-mer and its frequency in the data. In this way, the most significant k-mers are isolated within a very decent time and can be used as features in our data. 

The analysis was conducted in two different ways. In the first approach the algorithm was applied to each sequence separately. In this way, the repetitiveness of k-mers within a single sequence was examined. The data that were extracted from this analysis have been joined with the meta data in a single data matrix (https://github.com/covid19-bh-machine-learning/master/blob/master/kmerClusteringData/kmer_analysis_and_mata_data_merged.csv). The elements below the k-mer columns correspond to the frequency of each k-mer within a single sequence. 

In the second approach, the algorithm was applied to the total data set and, thus, genome sequencies were treated as a single set. K-mers that appear with high frequency within all the  genome sequences were successfully isolated in an output k-mers set. The next step was to remove all k-mers that appeared to every sequence from this output set, in order to reduce the dimensionality of the problem. The data that were extracted from this analysis have also been joined with the meta data set in a single data matrix (https://github.com/covid19-bh-machine-learning/master/blob/master/kmerClusteringData/kmer_analysis_and_meta_data__fixed_merged.csv). The elements below the k-mer columns are zeros and ones. One means that the current k-mer apperars in the corresponding sequence, while zero that it doesn't, as well. 

## Potential features at the aminoacid level, based on the AA frequencies

tbf -> t-SNE analysis, word2vec

## In-silico estimates of epitopes for COVID19

tbf  -> MHC estimated epitope comparisons

## Identify patterns in secondary structure

tbf  -> Feature extraction method for RNA secondary structure comparisons. Feature selection for variables of interest. Incorporate discoveries into other projects (e.g. pangenome annotations)

# Results

Preliminary results include:

- t-SNE analysis of the word2vec data
- 


# Conclusion

We recommend to include some discussion or conclusion about your work. Feel free to modify the section title as it fits better to your manuscript.

# Future work

And maybe you want to add a sentence or two on how you plan to continue. Please keep reading to learn about citations and references.

For citations of references, we prefer the use of parenthesis, last name and year. If you use a citation manager, Elsevier – Harvard or American Psychological Association (APA) will work. If you are referencing web pages, software or so, please do so in the same way. Whenever possible, add authors and year. We have included a couple of citations along this document for you to get the idea. Please remember to always add DOI whenever available, if not possible, please provide alternative URLs. You will end up with an alphabetical order list by authors’ last name.

# Jupyter notebooks, GitHub repositories and data repositories

* Please add a list here
* Make sure you let us know which of these correspond to Jupyter notebooks. Although not supported yet, we plan to add features for them
* And remember, software and data need a license for them to be used by others, no license means no clear rules so nobody could legally use a non-licensed research object, whatever that object is

# Acknowledgements

This work was done within the [COVID-19 Biohackathon of April 2020](https://github.com/virtual-biohackathons/covid-19-bh20).

# References

Leave thise section blank, create a paper.bib with all your references.


# Notes, to be removed

## Tables, figures and so on

Please remember to introduce tables (see Table 1) before they appear on the document. We recommend to center tables, formulas and figure but not the corresponding captions. Feel free to modify the table style as it better suits to your data.

Table 1
| Header 1 | Header 2 |
| -------- | -------- |
| item 1 | item 2 |
| item 3 | item 4 |

Remember to introduce figures (see Figure 1) before they appear on the document. 

![BioHackrXiv logo](./biohackrxiv.png)
 
Figure 1. A figure corresponding to the logo of our BioHackrXiv preprint.

