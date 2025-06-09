def init_date_constraints(self, ancestral_inference=False, clock_rate=None, **kwarks):
    """
        Get the conversion coefficients between the dates and the branch
        lengths as they are used in ML computations. The conversion formula is
        assumed to be 'length = k*numdate + b'. For convenience, these
        coefficients as well as regression parameters are stored in the
        'dates2dist' object.

        .. Note::
            The tree must have dates set to all nodes before calling this
            function.

        Parameters
        ----------

         ancestral_inference: bool
            If True, reinfer ancestral sequences
            when ancestral sequences are missing

         clock_rate: float
            If specified, timetree optimization will be done assuming a
            fixed clock rate as specified

        """
    self.logger('ClockTree.init_date_constraints...', 2)
    self.tree.coalescent_joint_LH = 0
    if self.aln and (ancestral_inference or not hasattr(self.tree.root, 'sequence')):
        self.infer_ancestral_sequences('probabilistic', marginal=self.branch_length_mode == 'marginal', sample_from_profile='root', **kwarks)
    self.logger('ClockTree.init_date_constraints: Initializing branch length interpolation objects...', 3)
    has_clock_length = []
    for node in self.tree.find_clades(order='postorder'):
        if node.up is None:
            node.branch_length_interpolator = None
        else:
            has_clock_length.append(hasattr(node, 'clock_length'))
            if hasattr(node, 'branch_length_interpolator') and node.branch_length_interpolator is not None:
                gamma = node.branch_length_interpolator.gamma
                merger_cost = node.branch_length_interpolator.merger_cost
            else:
                gamma = 1.0
                merger_cost = None
            if self.branch_length_mode == 'marginal':
                node.profile_pair = self.marginal_branch_profile(node)
            node.branch_length_interpolator = BranchLenInterpolator(node, self.gtr, pattern_multiplicity=self.multiplicity, min_width=self.min_width, one_mutation=self.one_mutation, branch_length_mode=self.branch_length_mode)
            node.branch_length_interpolator.merger_cost = merger_cost
            node.branch_length_interpolator.gamma = gamma
    use_cov = np.sum(has_clock_length) > len(has_clock_length) * 0.7 and self.use_covariation
    self.get_clock_model(covariation=use_cov, slope=clock_rate)
    for node in self.tree.find_clades(order='postorder'):
        if hasattr(node, 'raw_date_constraint') and node.raw_date_constraint is not None:
            if np.isscalar(node.raw_date_constraint):
                tbp = self.date2dist.get_time_before_present(node.raw_date_constraint)
                node.date_constraint = Distribution.delta_function(tbp, weight=1.0, min_width=self.min_width)
            else:
                tbp = self.date2dist.get_time_before_present(np.array(node.raw_date_constraint))
                node.date_constraint = Distribution(tbp, np.ones_like(tbp), is_log=False, min_width=self.min_width)
            if hasattr(node, 'bad_branch') and node.bad_branch is True:
                self.logger('ClockTree.init_date_constraints -- WARNING: Branch is marked as bad, excluding it from the optimization process.\n\t\tDate constraint will be ignored!', 4, warn=True)
        else:
            node.raw_date_constraint = None
            node.date_constraint = None