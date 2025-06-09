def make_decoder(num_topics, num_words):
    """Create the decoder function.

  Args:
    num_topics: The number of topics.
    num_words: The number of words.

  Returns:
    decoder: A `callable` mapping a `Tensor` of encodings to a
      `tfd.Distribution` instance over words.
  """
    topics_words_logits = tf.compat.v1.get_variable('topics_words_logits', shape=[num_topics, num_words], initializer=tf.compat.v1.glorot_normal_initializer())
    topics_words = tf.nn.softmax(topics_words_logits, axis=-1)

    def decoder(topics):
        word_probs = tf.matmul(topics, topics_words)
        return tfd.OneHotCategorical(probs=word_probs, name='bag_of_words')
    return (decoder, topics_words)