def infer(cls, nij, Ti, root_state, fixed_pi=None, pc=5.0, gap_limit=0.01, **kwargs):
    """
        Infer a GTR model by specifying the number of transitions and time spent in each
        character. The basic equation that is being solved is

        :math:`n_{ij} = pi_i W_{ij} T_j`

        where :math:`n_{ij}` are the transitions, :math:`pi_i` are the equilibrium
        state frequencies, :math:`W_{ij}` is the "substitution attempt matrix",
        while :math:`T_i` is the time on the tree spent in character state
        :math:`i`. To regularize the process, we add pseudocounts and also need
        to account for the fact that the root of the tree is in a particular
        state. the modified equation is

        :math:`n_{ij} + pc = pi_i W_{ij} (T_j+pc+root\\_state)`

        Parameters
        ----------

         nij : nxn matrix
            The number of times a change in character state is observed
            between state j and i

         Ti :n vector
            The time spent in each character state

         root_state : n vector
            The number of characters in state i in the sequence
            of the root node.

         pc : float
            Pseudocounts, this determines the lower cutoff on the rate when
            no substitutions are observed

         **kwargs:
            Key word arguments to be passed

        Keyword Args
        ------------

         alphabet : str
            Specify alphabet when applicable. If the alphabet specification
            is required, but no alphabet is specified, the nucleotide alphabet will be used as default.

        """
    from scipy import linalg as LA
    gtr = cls(**kwargs)
    gtr.logger('GTR: model inference ', 1)
    dp = 1e-05
    Nit = 40
    pc_mat = pc * np.ones_like(nij)
    np.fill_diagonal(pc_mat, 0.0)
    count = 0
    pi_old = np.zeros_like(Ti)
    if fixed_pi is None:
        pi = np.ones_like(Ti)
    else:
        pi = np.copy(fixed_pi)
    pi /= pi.sum()
    W_ij = np.ones_like(nij)
    mu = nij.sum() / Ti.sum()
    while LA.norm(pi_old - pi) > dp and count < Nit:
        gtr.logger(' '.join(map(str, ['GTR inference iteration', count, 'change:', LA.norm(pi_old - pi)])), 3)
        count += 1
        pi_old = np.copy(pi)
        W_ij = (nij + nij.T + 2 * pc_mat) / mu / (np.outer(pi, Ti) + np.outer(Ti, pi) + ttconf.TINY_NUMBER + 2 * pc_mat)
        np.fill_diagonal(W_ij, 0)
        scale_factor = np.einsum('i,ij,j', pi, W_ij, pi)
        W_ij = W_ij / scale_factor
        if fixed_pi is None:
            pi = (np.sum(nij + pc_mat, axis=1) + root_state) / (ttconf.TINY_NUMBER + mu * np.dot(W_ij, Ti) + root_state.sum() + np.sum(pc_mat, axis=1))
            pi /= pi.sum()
        mu = nij.sum() / (ttconf.TINY_NUMBER + np.sum(pi * W_ij.dot(Ti)))
    if count >= Nit:
        gtr.logger('WARNING: maximum number of iterations has been reached in GTR inference', 3, warn=True)
        if LA.norm(pi_old - pi) > dp:
            gtr.logger('the iterative scheme has not converged', 3, warn=True)
        elif np.abs(1 - np.max(pi.sum(axis=0))) > dp:
            gtr.logger('the iterative scheme has converged, but proper normalization was not reached', 3, warn=True)
    if gtr.gap_index is not None:
        if pi[gtr.gap_index] < gap_limit:
            gtr.logger('The model allows for gaps which are estimated to occur at a low fraction of %1.3e' % pi[gtr.gap_index] + '\n\t\tthis can potentially result in artificats.' + '\n\t\tgap fraction will be set to %1.4f' % gap_limit, 2, warn=True)
        pi[gtr.gap_index] = gap_limit
        pi /= pi.sum()
    gtr.assign_rates(mu=mu, W=W_ij, pi=pi)
    return gtr