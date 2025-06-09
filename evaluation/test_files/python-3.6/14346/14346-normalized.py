def add_data(self, data_descriptor):
    """
		Add a data set to the graph

		>>> graph.add_data({data:[1,2,3,4]}) # doctest: +SKIP

		Note that a 'title' key is ignored.

		Multiple calls to add_data will sum the elements, and the pie will
		display the aggregated data.  e.g.

		>>> graph.add_data({data:[1,2,3,4]}) # doctest: +SKIP
		>>> graph.add_data({data:[2,3,5,7]}) # doctest: +SKIP

		is the same as:

		>>> graph.add_data({data:[3,5,8,11]}) # doctest: +SKIP

		If data is added of with differing lengths, the corresponding
		values will be assumed to be zero.

		>>> graph.add_data({data:[1,2,3,4]}) # doctest: +SKIP
		>>> graph.add_data({data:[5,7]}) # doctest: +SKIP

		is the same as:

		>>> graph.add_data({data:[5,7]}) # doctest: +SKIP
		>>> graph.add_data({data:[1,2,3,4]}) # doctest: +SKIP

		and

		>>> graph.add_data({data:[6,9,3,4]}) # doctest: +SKIP
		"""
    pairs = itertools.zip_longest(self.data, data_descriptor['data'])
    self.data = list(itertools.starmap(robust_add, pairs))