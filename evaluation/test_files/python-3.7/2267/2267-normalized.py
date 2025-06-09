def transform(self, words, aggregate_method):
    """
        Transform words (or sequences of words) to vectors using a word2vec model.

        :param str words: An H2OFrame made of a single column containing source words.
        :param str aggregate_method: Specifies how to aggregate sequences of words. If method is `NONE`
               then no aggregation is performed and each input word is mapped to a single word-vector.
               If method is 'AVERAGE' then input is treated as sequences of words delimited by NA.
               Each word of a sequences is internally mapped to a vector and vectors belonging to
               the same sentence are averaged and returned in the result.

        :returns: the approximate reconstruction of the training data.
        """
    j = h2o.api('GET /3/Word2VecTransform', data={'model': self.model_id, 'words_frame': words.frame_id, 'aggregate_method': aggregate_method})
    return h2o.get_frame(j['vectors_frame']['name'])