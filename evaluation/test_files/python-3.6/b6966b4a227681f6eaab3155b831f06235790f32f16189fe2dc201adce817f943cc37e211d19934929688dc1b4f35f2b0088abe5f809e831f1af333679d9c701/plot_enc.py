from typing import Any
from Bio.SeqIO import parse
from .plot_funcs import _plot_enc
from CodonU.analyzer.internal_comp import filter_reference, enc, gc_123
from warnings import filterwarnings

def plot_enc(handle: str | Any, genetic_table_num: int, min_len_threshold: int=200, organism_name: None | str=None, save_image: bool=False, folder_path: str='', gene_analysis: bool=True):
    """
    Plots ENc curve from given fasta file

    :param handle: Handle to the file, or the filename as a string
    :param genetic_table_num: Genetic table number for codon table
    :param min_len_threshold: Minimum length of nucleotide sequence to be considered as gene
    :param organism_name: Name of organism (optional)
    :param save_image: Options for saving the image (optional)
    :param folder_path: Folder path where image should be saved (optional)
    :param gene_analysis: Option if gene analysis (True) or genome analysis (False) (optional)
    """
    filterwarnings('ignore')
    records = parse(handle, 'fasta')
    reference = filter_reference(records, min_len_threshold)
    enc_val_lst = []
    gc3_val_lst = []
    for seq in reference:
        enc_val_lst.append(enc([seq], genetic_table_num))
        gc3_val_lst.append(gc_123(seq)[-1] / 100)
    _plot_enc(enc_val_lst, gc3_val_lst, organism_name, save_image, folder_path, gene_analysis)