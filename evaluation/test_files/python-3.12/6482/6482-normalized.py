def _init_vocab(self, analyzed_docs):
    """Create vocabulary
        """

    class SetAccum(AccumulatorParam):

        def zero(self, initialValue):
            return set(initialValue)

        def addInPlace(self, v1, v2):
            v1 |= v2
            return v1
    if not self.fixed_vocabulary_:
        accum = analyzed_docs._rdd.context.accumulator(set(), SetAccum())
        analyzed_docs.foreach(lambda x: accum.add(set(chain.from_iterable(x))))
        vocabulary = {t: i for i, t in enumerate(accum.value)}
    else:
        vocabulary = self.vocabulary_
    if not vocabulary:
        raise ValueError('empty vocabulary; perhaps the documents only contain stop words')
    return vocabulary