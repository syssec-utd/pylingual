def evaluate(self, data=None, data_type='string', is_list=False):
    """Evaluates the expression with the provided context and format."""
    payload = {'data': data, 'expression': self.expr, 'data_type': data_type, 'is_list': is_list}
    res = self._client.post('/v1/evaluate', payload)
    return res['result']