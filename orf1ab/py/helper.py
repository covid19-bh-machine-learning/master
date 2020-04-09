import pandas as pd
from Bio import SeqIO
from Bio.Alphabet import generic_protein
from skbio import Protein
from pathlib import Path
import os
import logging
from collections import defaultdict
import numpy as np


class FastaMeta:
    '''
    object to hold fasta file and its corresponding meta file paths
    '''
    def __init__(self, fasta, meta):
        '''
        fasta: .fa file name
        meta: .csv file name
        '''
        self.data_path = Path(Path(__file__).resolve().parent.parent.parent, "data")
        self.fasta = os.path.join(self.data_path, fasta)
        self.meta = os.path.join(self.data_path, meta)

class DataProcessing(FastaMeta):
    def __init__(self, fasta, meta):
        super().__init__(fasta, meta)

    def get_amino_kmer_df(self, k):
        '''
        returns a pandas dataframe
        '''
        unique_seqs = self.get_uniqe_seqs()
        print(f"Generating all possible kmers({k}) for the unique reads...")
        kmers =  [[str(kmer) for kmer in Protein(str(s.seq)).iter_kmers(4)] for s in unique_seqs]
        print(len(kmers))
        print(f"Generated a total of {sum([len(i) for i in kmers])} kmers.")
        return pd.DataFrame.from_dict(dict(zip([seq.id for seq in unique_seqs], kmers)))

    def get_amino_df(self, k):
        '''
        k = kmer length
        Generates all possible offsets of amino acid sequence and
        returns a pandas dataframe merged with given metadata
        '''
        meta_df = self.get_meta_df()
        seq_seq = defaultdict(list)
        seq_list = list(SeqIO.parse(self.fasta, 'fasta', alphabet=generic_protein))
        for s in seq_list:
            for i in range(k):
                seq_seq[f'seq_offset_{i}'].append(str(s.seq)[i:])
        for key in seq_seq:
            meta_df[key] = seq_seq[key]
        return meta_df


    def get_uniqe_seqs(self):
        seq_list = list(SeqIO.parse(self.fasta, 'fasta', alphabet=generic_protein))
        unique_seqs = []
        unique = set()
        for seq in seq_list:
            if seq.id not in unique:
                unique.add(seq.id)
                unique_seqs.append(seq)
        print(f"Found {len(unique_seqs)} unique reads out of {len(seq_list)} total reads!")
        return unique_seqs

    def get_meta_df(self):
        return pd.read_csv(self.meta)





if __name__ == '__main__':
    train = FastaMeta('fa', 'meta')
    print(train.meta)
    print(train.fasta)
