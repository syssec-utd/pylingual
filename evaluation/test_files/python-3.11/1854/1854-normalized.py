def _backtraces_to_transductions(self, first, second, backtraces, threshold, return_cost=False):
    """
        Восстанавливает трансдукции по таблице обратных ссылок

        Аргументы:
        ----------
        first, second : string
            верхние и нижние элементы трансдукции
        backtraces : array-like, dtype=list, shape=(len(first)+1, len(second)+1)
            таблица обратных ссылок
        threshold : float
            порог для отсева трансдукций,
            возвращаются только трансдукции стоимостью <= threshold
        return_cost : bool (optional, default=False)
            если True, то вместе с трансдукциями возвращается их стоимость

        Возвращает:
        -----------
        result : list
            список вида [(трансдукция, стоимость)], если return_cost=True
            и вида [трансдукция], если return_cost=False,
            содержащий все трансдукции, переводящие first в second,
            чья стоимость не превышает threshold
        """
    m, n = (len(first), len(second))
    agenda = [None] * (m + 1)
    for i in range(m + 1):
        agenda[i] = [[] for j in range(n + 1)]
    agenda[m][n] = [((), 0.0)]
    for i_right in range(m, -1, -1):
        for j_right in range(n, -1, -1):
            current_agenda = agenda[i_right][j_right]
            if len(current_agenda) == 0:
                continue
            for i, j in backtraces[i_right][j_right]:
                up, low = (first[i:i_right], second[j:j_right])
                add_cost = self.operation_costs[up][low]
                for elem, cost in current_agenda:
                    new_cost = cost + add_cost
                    if new_cost <= threshold:
                        agenda[i][j].append((((up, low),) + elem, new_cost))
    if return_cost:
        return agenda[0][0]
    else:
        return [elem[0] for elem in agenda[0][0]]