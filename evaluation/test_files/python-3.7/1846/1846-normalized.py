def get_operation_cost(self, up, low):
    """
        Возвращает стоимость элементарной трансдукции up->low
        или np.inf, если такой элементарной трансдукции нет

        Аргументы:
        ----------
        up, low : string
            элементы элементарной трансдукции

        Возвращает:
        -----------
        cost : float
            стоимость элементарной трансдукции up->low
            (np.inf, если такая трансдукция отсутствует)
        """
    up_costs = self.operation_costs.get(up, None)
    if up_costs is None:
        return np.inf
    cost = up_costs.get(low, np.inf)
    return cost