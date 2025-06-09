def default_exchange_proposed_fn(prob_exchange):
    """Default exchange proposal function, for replica exchange MC.

  With probability `prob_exchange` propose combinations of replica for exchange.
  When exchanging, create combinations of adjacent replicas in
  [Replica Exchange Monte Carlo](
  https://en.wikipedia.org/wiki/Parallel_tempering)

  ```
  exchange_fn = default_exchange_proposed_fn(prob_exchange=0.5)
  exchange_proposed = exchange_fn(num_replica=3)

  exchange_proposed.eval()
  ==> [[0, 1]]  # 1 exchange, 0 <--> 1

  exchange_proposed.eval()
  ==> []  # 0 exchanges
  ```

  Args:
    prob_exchange: Scalar `Tensor` giving probability that any exchanges will
      be generated.

  Returns:
    default_exchange_proposed_fn_: Python callable which take a number of
      replicas (a Python integer), and return combinations of replicas for
      exchange as an [n, 2] integer `Tensor`, `0 <= n <= num_replica // 2`,
      with *unique* values in the set `{0, ..., num_replica}`.
  """

    def default_exchange_proposed_fn_(num_replica, seed=None):
        """Default function for `exchange_proposed_fn` of `kernel`."""
        seed_stream = distributions.SeedStream(seed, 'default_exchange_proposed_fn')
        zero_start = tf.random.uniform([], seed=seed_stream()) > 0.5
        if num_replica % 2 == 0:

            def _exchange():
                flat_exchange = tf.range(num_replica)
                if num_replica > 2:
                    start = tf.cast(~zero_start, dtype=tf.int32)
                    end = num_replica - start
                    flat_exchange = flat_exchange[start:end]
                return tf.reshape(flat_exchange, [tf.size(input=flat_exchange) // 2, 2])
        else:

            def _exchange():
                start = tf.cast(zero_start, dtype=tf.int32)
                end = num_replica - tf.cast(~zero_start, dtype=tf.int32)
                flat_exchange = tf.range(num_replica)[start:end]
                return tf.reshape(flat_exchange, [tf.size(input=flat_exchange) // 2, 2])

        def _null_exchange():
            return tf.reshape(tf.cast([], dtype=tf.int32), shape=[0, 2])
        return tf.cond(pred=tf.random.uniform([], seed=seed_stream()) < prob_exchange, true_fn=_exchange, false_fn=_null_exchange)
    return default_exchange_proposed_fn_