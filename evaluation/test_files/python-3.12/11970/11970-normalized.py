def report(self, output_file=sys.stdout):
    """Report generated model in human readable form."""
    if self._args and self._args.verbose > 2:
        pprint(self.results)
    for dimension, lc_info in self.results['dimensions'].items():
        print('{}D layer condition:'.format(dimension), file=output_file)
        for cache, lc_solution in sorted(lc_info['caches'].items()):
            print(cache + ': ', end='', file=output_file)
            if lc_solution['lt'] is sympy.true:
                print('unconditionally fulfilled', file=output_file)
            elif lc_solution['eq'] is None:
                print('{}'.format(lc_solution['lt']), file=output_file)
            elif type(lc_solution['eq']) is not list:
                print('{}'.format(lc_solution['eq']), file=output_file)
            else:
                for solu in lc_solution['eq']:
                    for s, v in solu.items():
                        print('{} <= {}'.format(s, v), file=output_file)