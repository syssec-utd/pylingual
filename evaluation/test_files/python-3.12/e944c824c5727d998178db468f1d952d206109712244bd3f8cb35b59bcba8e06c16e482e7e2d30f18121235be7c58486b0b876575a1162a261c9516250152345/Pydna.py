"""
##############################################################################

A class used for computing different types of DNA descriptors!

You can freely use and distribute it. If you have any problem,

you could contact with us timely.

Authors: Zhijiang Yao and Dongsheng Cao.

Date: 2016.06.14

Email: gadsby@163.com and oriental-cds@163.com

##############################################################################
"""
from PyBioMed.PyDNA.PyDNAac import *
from PyBioMed.PyDNA.PyDNAnac import *
from PyBioMed.PyDNA.PyDNApsenac import *
from PyBioMed.PyDNA.PyDNAutil import *

class PyDNA:
    """

    This GetProDes class aims at collecting all descriptor calcualtion modules into a simple class.

    """

    def __init__(self, DNASequence=''):
        """
        input a DNA sequence
        """
        if len(DNASequence) == 0:
            print('You must input a DNA sequence when constructing a object. It is a string!')
        else:
            self.DNASequence = DNASequence

    def GetDAC(self, **kwargs):
        """
        #################################################################
        Make DAC dictionary.

        :param input_data: file object or sequence list.
        :param phyche_index: physicochemical properties list.
        :param all_property: bool, choose all physicochemical properties or not.
        :param extra_phyche_index: dict, the key is the dinucleotide (string), and its corresponding value is a list.
                                   It means user-defined phyche_index.
        #################################################################
        """
        res = GetDAC(self.DNASequence, **kwargs)
        return res

    def GetDCC(self, **kwargs):
        """
        #################################################################
        Make DCC dictionary.

        :param input_data: file object or sequence list.
        :param phyche_index: physicochemical properties list.
        :param all_property: bool, choose all physicochemical properties or not.
        :param extra_phyche_index: dict, the key is the dinucleotide (string), and its corresponding value is a list.
                                   It means user-defined phyche_index.
        #################################################################
        """
        res = GetDCC(self.DNASequence, **kwargs)
        return res

    def GetDACC(self, **kwargs):
        """
        #################################################################
        Make DACC dictionary.

        :param input_data: file object or sequence list.
        :param phyche_index: physicochemical properties list.
        :param all_property: bool, choose all physicochemical properties or not.
        :param extra_phyche_index: dict, the key is the dinucleotide (string), and its corresponding value is a list.
                                   It means user-defined phyche_index.
        #################################################################
        """
        res = GetDACC(self.DNASequence, **kwargs)
        return res

    def GetTAC(self, **kwargs):
        """
        #################################################################
        Make TAC dictionary.

        :param input_data: file object or sequence list.
        :param phyche_index: physicochemical properties list.
        :param all_property: bool, choose all physicochemical properties or not.
        :param extra_phyche_index: dict, the key is the dinucleotide (string), and its corresponding value is a list.
                                   It means user-defined phyche_index.
        #################################################################
        """
        res = GetTAC(self.DNASequence, **kwargs)
        return res

    def GetTCC(self, **kwargs):
        """
        #################################################################
        Make TCC dictionary.

        :param input_data: file object or sequence list.
        :param phyche_index: physicochemical properties list.
        :param all_property: bool, choose all physicochemical properties or not.
        :param extra_phyche_index: dict, the key is the dinucleotide (string), and its corresponding value is a list.
                                   It means user-defined phyche_index.
        #################################################################
        """
        res = GetTCC(self.DNASequence, **kwargs)
        return res

    def GetTACC(self, **kwargs):
        """
        #################################################################
        Make TACC dictionary.

        :param input_data: file object or sequence list.
        :param phyche_index: physicochemical properties list.
        :param all_property: bool, choose all physicochemical properties or not.
        :param extra_phyche_index: dict, the key is the dinucleotide (string), and its corresponding value is a list.
                                   It means user-defined phyche_index.
        #################################################################
        """
        res = GetTACC(self.DNASequence, **kwargs)
        return res

    def GetKmer(self, **kwargs):
        """
        ###########################################################################
        Make a kmer dictionary with options k, upto, revcomp, normalize.

        :param k: int, the k value of kmer, it should be larger than 0.
        :param normalize: bool, normalize the result vector or not.
        :param upto: bool, whether to generate 1-kmer, 2-kmer, ..., k-mer.
        :param alphabet: string.
        :param data: file object or sequence list.
        :return: kmer vector.
        ###########################################################################
        """
        res = GetKmer(self.DNASequence, **kwargs)
        return res

    def GetRevcKmer(self, **kwargs):
        """
        ###########################################################################
        Make a reverse compliment kmer dictionary with options k, upto, normalize.

        :param data: file object or sequence list.
        :return: reverse compliment kmer vector.
        ###########################################################################
        """
        res = GetRevcKmer(self.DNASequence, **kwargs)
        return res

    def GetPseDNC(self, **kwargs):
        """
        Make PseDNC dictionary.

        :param input_data: file type or handle.
        :param k: k-tuple.
        :param extra_phyche_index: dict, the key is the dinucleotide (string),
                                         the value is its physicochemical property value (list).
                                   It means the user-defined physicochemical indices.
        """
        res = GetPseDNC(self.DNASequence, **kwargs)
        return res

    def GetPseKNC(self, **kwargs):
        """
        Make PseKNC dictionary.

        :param input_data: file type or handle.
        :param k: k-tuple.
        :param extra_phyche_index: dict, the key is the dinucleotide (string),
                                         the value is its physicochemical property value (list).
                                   It means the user-defined physicochemical indices.
        """
        res = GetPseKNC(self.DNASequence, **kwargs)
        return res

    def GetPCPseDNC(self, **kwargs):
        """
        Make a PCPseDNC dictionary.

        :param input_data: file object or sequence list.
        :param phyche_index: physicochemical properties list.
        :param all_property: choose all physicochemical properties or not.
        :param extra_phyche_index: dict, the key is the dinucleotide (string),
                                         the value is its physicochemical property value (list).
                                   It means the user-defined physicochemical indices.
        """
        res = GetPCPseDNC(self.DNASequence, **kwargs)
        return res

    def GetPCPseTNC(self, **kwargs):
        """
        Make a PCPseDNC dictionary.

        :param input_data: file object or sequence list.
        :param phyche_index: physicochemical properties list.
        :param all_property: choose all physicochemical properties or not.
        :param extra_phyche_index: dict, the key is the dinucleotide (string),
                                         the value is its physicochemical property value (list).
                                   It means the user-defined physicochemical indices.
        """
        res = GetPCPseTNC(self.DNASequence, **kwargs)
        return res

    def GetSCPseDNC(self, **kwargs):
        """
        Make a SCPseDNC dictionary.

        :param input_data: file object or sequence list.
        :param phyche_index: physicochemical properties list.
        :param all_property: choose all physicochemical properties or not.
        :param extra_phyche_index: dict, the key is the dinucleotide (string),
                                         the value is its physicochemical property value (list).
                                   It means the user-defined physicochemical indices.
        """
        res = GetSCPseDNC(self.DNASequence, **kwargs)
        return res

    def GetSCPseTNC(self, **kwargs):
        """
        Make a SCPseTNC dictionary.

        :param input_data: file object or sequence list.
        :param phyche_index: physicochemical properties list.
        :param all_property: choose all physicochemical properties or not.
        :param extra_phyche_index: dict, the key is the dinucleotide (string),
                                         the value is its physicochemical property value (list).
                                   It means the user-defined physicochemical indices.
        """
        res = GetSCPseTNC(self.DNASequence, **kwargs)
        return res
if __name__ == '__main__':
    phyche_index = [[7.176, 6.272, 4.736, 7.237, 3.81, 4.156, 4.156, 6.033, 3.41, 3.524, 4.445, 6.033, 1.613, 5.087, 2.169, 7.237, 3.581, 3.239, 1.668, 2.169, 6.813, 3.868, 5.44, 4.445, 3.81, 4.678, 5.44, 4.156, 2.673, 3.353, 1.668, 4.736, 4.214, 3.925, 3.353, 5.087, 2.842, 2.448, 4.678, 3.524, 3.581, 2.448, 3.868, 4.156, 3.467, 3.925, 3.239, 6.272, 2.955, 3.467, 2.673, 1.613, 1.447, 3.581, 3.81, 3.41, 1.447, 2.842, 6.813, 3.81, 2.955, 4.214, 3.581, 7.176]]
    DNASequence = 'GACTGAACTGCACTTTGGTTTCATATTATTTGCTC'
    dna_obj = PyDNA(DNASequence)
    print(dna_obj.GetDAC(phyche_index=['Twist', 'Tilt']))
    print(dna_obj.GetDAC(all_property=True))
    print(dna_obj.GetDCC(phyche_index=['Twist', 'Tilt']))
    print(dna_obj.GetDACC(all_property=True))
    print(dna_obj.GetTAC(all_property=True))
    print(dna_obj.GetTACC(phyche_index=['Dnase I', 'Nucleosome'], extra_phyche_index=NormalizeIndex(phyche_index, is_convert_dict=True)))
    print(dna_obj.GetTCC(phyche_index=['Dnase I', 'Nucleosome'], extra_phyche_index=NormalizeIndex(phyche_index, is_convert_dict=True)))
    print(dna_obj.GetKmer(k=2))
    print(dna_obj.GetRevcKmer(k=2, normalize=True, upto=True))
    print(dna_obj.GetPseDNC(phyche_index=['Dnase I', 'Nucleosome'], lamada=2, w=0.05))
    print(dna_obj.GetPseKNC(phyche_index=['Dnase I', 'Nucleosome']))
    print(dna_obj.GetPCPseDNC(phyche_index=['Twist', 'Tilt']))
    print(dna_obj.GetPCPseTNC(all_property=True, lamada=2, w=0.05))
    print(dna_obj.GetSCPseDNC(phyche_index=['Twist', 'Tilt'], lamada=2, w=0.05))
    print(dna_obj.GetSCPseTNC(phyche_index=['Dnase I', 'Nucleosome'], lamada=1, w=0.05))
    print(len(dna_obj.GetDAC(phyche_index=['Twist', 'Tilt'])))
    print(len(dna_obj.GetDAC(all_property=True)))
    print(len(dna_obj.GetDCC(phyche_index=['Twist', 'Tilt'])))
    print(len(dna_obj.GetDCC(all_property=True)))
    print(len(dna_obj.GetDACC(all_property=True)))
    print(len(dna_obj.GetTAC(all_property=True)))
    print(len(dna_obj.GetTACC(phyche_index=['Dnase I', 'Nucleosome'], extra_phyche_index=NormalizeIndex(phyche_index, is_convert_dict=True))))
    print(len(dna_obj.GetTACC(all_property=True)))
    print(len(dna_obj.GetTCC(all_property=True)))
    print(len(dna_obj.GetTCC(phyche_index=['Dnase I', 'Nucleosome'], extra_phyche_index=NormalizeIndex(phyche_index, is_convert_dict=True))))
    print(len(dna_obj.GetKmer(k=2)))
    print(len(dna_obj.GetRevcKmer(k=2, normalize=True, upto=True)))
    print(len(dna_obj.GetPseDNC(phyche_index=['Dnase I', 'Nucleosome'], lamada=2, w=0.05)))
    print(len(dna_obj.GetPseKNC(phyche_index=['Dnase I', 'Nucleosome'])))
    print(len(dna_obj.GetPCPseDNC(phyche_index=['Twist', 'Tilt'])))
    print(len(dna_obj.GetPCPseTNC(all_property=True, lamada=2, w=0.05)))
    print(len(dna_obj.GetSCPseDNC(phyche_index=['Twist', 'Tilt'], lamada=2, w=0.05)))
    print(len(dna_obj.GetSCPseTNC(phyche_index=['Dnase I', 'Nucleosome'], lamada=1, w=0.05)))
    print(len(dna_obj.GetPseDNC(all_property=True, lamada=2, w=0.05)))
    print(len(dna_obj.GetPseKNC(all_property=True, lamada=2, w=0.05)))
    print(len(dna_obj.GetPCPseDNC(all_property=True, lamada=2, w=0.05)))
    print(len(dna_obj.GetPCPseTNC(all_property=True, lamada=2, w=0.05)))
    print(len(dna_obj.GetSCPseDNC(all_property=True, lamada=2, w=0.05)))
    print(len(dna_obj.GetSCPseTNC(all_property=True, lamada=2, w=0.05)))