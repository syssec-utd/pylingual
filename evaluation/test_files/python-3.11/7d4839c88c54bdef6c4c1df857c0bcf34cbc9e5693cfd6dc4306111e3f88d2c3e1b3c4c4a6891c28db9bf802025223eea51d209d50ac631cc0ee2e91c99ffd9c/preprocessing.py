license = '\nMIT License\n\nCopyright (c) 2022 Stefan Güttel, Xinye Chen\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n'
import copy
import numpy as np
from collections import Counter
from scipy.spatial import distance
from sklearn.feature_extraction.text import TfidfVectorizer
'\nNatural language processing (NLP) fundamental operation on symbolic sequences. \nIt is useful for research in symbolic time series representaion with NLP, like ABBA.\n\n\nsequences   -> n-gram \n            -> categorical encoding\n            -> padding sequences (optional)\n               bag-of-words encoding\n               one-hot encoding\n               tf-idf encoding\n'

class encoders:
    """
    Transform texts/symbols to numerical values
    
    This package provide various essential tools to transform symbols data into numerical data.
    Each symbolic sequence in the dataset might be of various length, hence we provide the 
    ``pad_sequence`` method to unify the length of each instance. The package offers numerous API
    like ``BOW_encode``, ``categorical_encode``, ``one_hot_encode``, and ``tfidf_encode`` to transform
    the symbolic sequence to the vector representations. Additionally, you can transform the symbolic 
    data in n-grams form with ``n_gram_build``.
        
    Parameters
    ----------     
    sequences: list
        List of symbolic sequence.
    
    dictionary: dict, default=None
        The dictionary for symbols to transform symbols to labels. If None, will employ
        simple label encoding.
    
    
    Attributes
    ----------
    dict_tokens: dict
        The dictionary for symbols to labels. 
    
    """

    def __init__(self, dictionary=None):
        self.corpus_size = 0
        if dictionary == None:
            self.dict_tokens = None
        else:
            self.dict_tokens = dictionary

    def truncate_sequence(self, sequences, maxlen=10, truncating='post'):
        """ 
        Truncate the sequence.

        Parameters
        ----------   
        sequences: list
            The symbolic sequences.
            
        maxlen: int
            The truncated length, specify the dimensionality of transformed data.
        
        truncating: str, default='pre'
            Remove values from sequences larger than maxlen, either at the beginning or at the end of the sequences.
        
        """
        if maxlen <= 0:
            raise ValueError('please ensure maxlen is correct value.')
        tseq = list()
        if truncating == 'post':
            for i in range(len(sequences)):
                tseq.append(sequences[i][:maxlen])
        else:
            for i in range(len(sequences)):
                tseq.append(sequences[i][-maxlen:])
        return tseq

    def pad_sequence(self, sequences, maxlen=10, value='last', method='post', truncating='pre'):
        """ 
        Pad sequence with the specified value 

        Parameters
        ----------   
        sequences: list
            The symbolic sequences.
            
        maxlen: int
            The truncated length, specify the dimensionality of transformed data.
        
        value: float or str, default='last'
            The padding value.
            specify ``none`` means the ABBA embedding will use zero to feed the missing values as embedding.
    
        method: str, default="post" 
            Add the corresponding value of at the begin/end of the sequence to 
            make each instance are of the same length. 
            
            Pad either before ("pre") or after each sequence ("post").
            
        truncating: str, default='pre'
            Remove values from sequences larger than maxlen, either at the beginning or at the end of the sequences.
            
        Returns 
        ---------- 
        pseq: numpy.ndarray
            The padding sequence.
        
        """
        if maxlen <= 0:
            raise ValueError('please ensure maxlen greater than 0.')
        if value == 'first':
            pseq = np.full((len(sequences), maxlen), 0)
            for i in range(len(pseq)):
                for j in range(maxlen):
                    pseq[i, j] = sequences[i][0]
        elif value == 'last':
            pseq = np.full((len(sequences), maxlen), 0)
            for i in range(len(pseq)):
                for j in range(maxlen):
                    pseq[i, j] = sequences[i][-1]
        elif value == 'none':
            pseq = np.full((len(sequences), maxlen), -1)
        else:
            pseq = np.full((len(sequences), maxlen), value)
        if method == 'pre':
            if truncating == 'pre':
                for i in range(len(sequences)):
                    truncated = sequences[i][-maxlen:]
                    pseq[i, -len(truncated):] = truncated
            else:
                for i in range(len(sequences)):
                    truncated = sequences[i][:maxlen]
                    pseq[i, -len(truncated):] = truncated
        elif method == 'post':
            if truncating == 'pre':
                for i in range(len(sequences)):
                    truncated = sequences[i][-maxlen:]
                    pseq[i, 0:len(truncated)] = truncated
            else:
                for i in range(len(sequences)):
                    truncated = sequences[i][:maxlen]
                    pseq[i, 0:len(truncated)] = truncated
        else:
            raise ValueError('Please specify a method for pooling.')
        return pseq

    def BOW_encode(self, sequences):
        """
        Encode with bag-of-words
        
        """
        if self.dict_tokens is None:
            self.dict_tokens = self.dict_form(sequences)
        N = len(self.dict_tokens)
        matrix = np.zeros((len(sequences), N))
        count = dict()
        for i in range(len(sequences)):
            for j in range(len(sequences[i])):
                token = sequences[i][j]
                if token not in count:
                    count[token] = 1
                else:
                    count[token] += 1
        for i in range(len(sequences)):
            sentence = sequences[i]
            for token in sentence:
                matrix[i, self.dict_tokens[token] - 1] = count[token]
        return matrix

    def categorical_encode(self, sequences):
        """ 
        Encode with categories
        
        """
        if self.dict_tokens is None:
            self.dict_tokens = self.dict_form(sequences)
        new_set = []
        for sentence in sequences:
            new_sentence = []
            for token in sentence:
                new_sentence.append(self.dict_tokens[token])
            new_set.append(new_sentence)
        return new_set

    def one_hot_encode(self, sequences):
        """
        Encode with One-hot 
        
        """
        if self.dict_tokens is None:
            self.dict_tokens = self.dict_form(sequences)
        N = len(self.dict_tokens)
        matrix = np.zeros((len(sequences), N))
        for i in range(len(sequences)):
            sentence = sequences[i]
            for word in sentence:
                matrix[i, self.dict_tokens[word] - 1] = 1
        return matrix

    def tfidf_encode(self, sequences):
        """
        Encode with TF-IDF 
        
        """
        sequences_string = self.string_encode(sequences)
        vectorizer = TfidfVectorizer(analyzer='char', stop_words=None, ngram_range=(1, 1))
        X = vectorizer.fit_transform(sequences_string).toarray()
        return X

    def n_gram_build(self, sequences, w=5):
        """ 
        Transform the symbolic sequences into the symbolic sequences in n-gram form
        
        """
        n_grams = list()
        for series in data:
            sequence = list()
            sequence = [''.join(series[j:j + w]) for j in range(len(series) - w + 2)]
            n_grams.append(sequence)
        return n_grams

    def dict_form(self, sequences):
        """
        From dictionary for symbols 
        
        """
        token_index = {}
        for sentence in sequences:
            for token in sentence:
                if token not in token_index:
                    token_index[token] = len(token_index) + 1
        self.corpus_size = len(token_index) + 1
        return token_index

    def string_encode(self, sequences):
        """
        Transform the symbolic sequences into a single symbolic sequence 
        
        """
        new_sets = []
        for sentence in sequences:
            new_sets.append(' '.join(sentence))
        return new_sets

    def symbols_count(self, sequences):
        """
        Count the symbols in sequences
        
        """
        count = dict()
        for i in range(len(sequences)):
            for j in range(len(sequences[i])):
                if sequences[i][j] in count.keys():
                    count[sequences[i][j]] = count[sequences[i][j]] + 1
                else:
                    count[sequences[i][j]] = 1
        return count

    def return_percent_len(self, sequences, percent=1.0):
        """
        Return the length that can cover percent of the sequences
        
        """
        count_len = list()
        for sequence in sequences:
            count_len.append(len(sequence))
        sorted_count = sorted(count_len)
        percent_len = sorted_count[int(round(percent * len(sorted_count))) - 1]
        return percent_len

class vector_embed(object):
    """
    Embed the vector into the symbolic sequences.
    
    Parameters
    ---------- 
    embeddings: numpy.ndarray
        The embedding vector space for symbolic sequences.
    
    dictionary: dict, default=None
        The dictionary for mapping the symbols to labels corresponding 
        to the embedding matrix row.
        
    scl: float, default=1
        Apply the scaling to the first column of embedding matrix.
        
    string: boolean, default=True
        Whether the sequences are string values or numerical values.
        
    """

    def __init__(self, embeddings, dictionary=None, scl=1, string=True):
        self.dictionary = dictionary
        if dictionary is not None:
            self.string = False
        else:
            self.string = string
        self.embeddings = embeddings
        self.scl = scl

    def transform(self, data, std=True):
        if std:
            embeddings = (self.embeddings - self.embeddings.mean(axis=0)) / self.embeddings.std(axis=0)
        else:
            embeddings = self.embeddings
        embeddings[:, 0] = embeddings[:, 0] * self.scl
        transformed = copy.deepcopy(data)
        if self.string:
            for i in range(len(data)):
                for j in range(len(data[0])):
                    ID = self.dictionary[data[i][j]]
                    transformed[i][j] = list(embeddings[ID])
        else:
            transformed = transformed.tolist()
            for i in range(len(data)):
                for j in range(len(data[0])):
                    if transformed[i][j] != -1:
                        transformed[i][j] = list(embeddings[data[i][j]])
                    else:
                        transformed[i][j] = [0, 0]
        return np.array(transformed)

def vsm_classify(data, matrix, terms, label_mark=None):
    """
    Using vector space model to allocate the data to the nearest class.
    
    Transform the data into bag of word vectors, and compute their closest 
    class weight vector and assign the data to the class.
    
    Parameters
    ----------   
    data - list
        Each instance correspond to the symbolic sequence.
        
    matrix - np.array
        The class weight vectors.
        
    terms - list
        The list of key symbols for bag of words vector representation.
        
    label_mark - list
        The associated ground truth labels for the predicted labels. We use this since 
        some of label are start with -1 or 0. For example, for binary data, it might have 
        labels like {-1, 1} and {0, 1}. We can use label_mark to uniform them.
        
    Returns 
    ---------- 
    labels, label_scores: list
        The predictions and the associated probabilistic output.
        
    """
    if label_mark is None:
        label_mark = np.arange(matrix.shape[1])
    labels = list()
    label_scores = list()
    for instance in data:
        scores = list()
        vector = np.zeros(matrix.shape[0])
        freq = Counter(instance)
        for i in freq:
            if i in terms:
                vector[terms.index(i)] = freq[i]
        for category in range(matrix.shape[1]):
            scores.append(distance.cosine(matrix[:, category], vector))
        label_scores.append(scores)
        labels.append(label_mark[np.argmin(scores)])
    return (labels, label_scores)

def contruct_tf_idf_class_matrix(dictionaries, threshold=None):
    """
    Build TF-IDF class matrix
    
    Each column denotes a class weight matrix (weights are represented by TF-IDF),
    while each row denotes TF-IDF vector for each word/symbol. 
    
    
    Parameters
    ----------   
    dictionaries: list
        Each element denotes the dictionary associated with  the class.
        
    threshold: float or int
        The weight below this threshold will abandon the associated symbol
        instead of putting the symbol into the dictionary.
        
    Returns 
    ---------- 
    matrix: numpy.ndarray
        The matrix returned as TF-IDF class matrix.
    
    terms: list
        The list of words in represented in TF-IDF class matrix. 
        The order of the list correspond to that of rows in the matrix.
    
    """
    terms = list()
    if threshold is not None:
        for i in range(len(dictionaries)):
            dkeys = list(dictionaries[i].keys())
            for j in dkeys:
                if dictionaries[i][j] < threshold:
                    dictionaries[i].pop(j)
            terms = terms + list(dictionaries[i].keys())
    else:
        for i in range(len(dictionaries)):
            terms = terms + list(dictionaries[i].keys())
    terms = list(set(terms))
    matrix = np.zeros((len(terms), len(dictionaries)))
    for col in range(matrix.shape[1]):
        for row in range(matrix.shape[0]):
            if terms[row] in dictionaries[col]:
                matrix[row, col] = dictionaries[col][terms[row]]
            else:
                matrix[row, col] = 0
    return (matrix, terms)

def tf_idf(dictionaries):
    """
    Construct TF-IDF dictionary
    
    """
    tf_dicts = copy.deepcopy(dictionaries)
    tf_idf_dicts = copy.deepcopy(dictionaries)
    documents_length = len(dictionaries)
    for i in range(documents_length):
        total = sum(tf_dicts[i].values())
        for j in tf_dicts[i]:
            tf_dicts[i][j] = tf_dicts[i][j] / total
            tf_idf_dicts[i][j] = tf_dicts[i][j] * inverse_freq(j, dictionaries)
    return (tf_dicts, tf_idf_dicts)

def inverse_freq(word, dictionaries):
    total = len(dictionaries)
    count = 0
    for corpus in dictionaries:
        if word in corpus:
            count = count + 1
    return np.log(1 + total / count)

def count_dictionary(store_corpus):
    dictionaries = list()
    for document in store_corpus:
        dictionary = dict()
        for word in document:
            if word not in dictionary:
                dictionary[word] = 1
            else:
                dictionary[word] = dictionary[word] + 1
        dictionaries.append(dictionary)
    return dictionaries

def build_corpus(corpus, labels):
    store_corpus = list()
    for i in set(labels):
        document = []
        for j in np.where(labels == i)[0]:
            document = document + corpus[j]
        store_corpus.append(document)
    return store_corpus