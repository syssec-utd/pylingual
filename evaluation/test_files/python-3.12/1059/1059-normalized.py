def _resolve_graph(self, distribution_names=None, leaf_name='x'):
    """Creates a `tuple` of `tuple`s of dependencies.

    This function is **experimental**. That said, we encourage its use
    and ask that you report problems to `tfprobability@tensorflow.org`.

    Args:
      distribution_names: `list` of `str` or `None` names corresponding to each
        of `model` elements. (`None`s are expanding into the
        appropriate `str`.)
      leaf_name: `str` used when no maker depends on a particular
        `model` element.

    Returns:
      graph: `tuple` of `(str tuple)` pairs representing the name of each
        distribution (maker) and the names of its dependencies.

    #### Example

    ```python
    d = tfd.JointDistributionSequential([
                     tfd.Independent(tfd.Exponential(rate=[100, 120]), 1),
        lambda    e: tfd.Gamma(concentration=e[..., 0], rate=e[..., 1]),
                     tfd.Normal(loc=0, scale=2.),
        lambda n, g: tfd.Normal(loc=n, scale=g),
    ])
    d._resolve_graph()
    # ==> (
    #       ('e', ()),
    #       ('g', ('e',)),
    #       ('n', ()),
    #       ('x', ('n', 'g')),
    #     )
    ```

    """
    if distribution_names is None or any(self._dist_fn_args):
        distribution_names = _resolve_distribution_names(self._dist_fn_args, distribution_names, leaf_name)
    if len(set(distribution_names)) != len(distribution_names):
        raise ValueError('Distribution names must be unique: {}'.format(distribution_names))
    if len(distribution_names) != len(self._dist_fn_wrapped):
        raise ValueError('Distribution names must be 1:1 with `rvs`.')
    return tuple(zip(distribution_names, tuple((() if a is None else a for a in self._dist_fn_args))))