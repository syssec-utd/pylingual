def __mutate_parameter(value, param, mut_rate, max_mut_amt):
    """Private, static method: mutates parameter

        Args:
            value (int or float): current value for Member's parameter
            param (Parameter): parameter object
            mut_rate (float): mutation rate of the value
            max_mut_amt (float): maximum mutation amount of the value

        Returns:
            int or float: mutated value
        """
    if uniform(0, 1) < mut_rate:
        mut_amt = uniform(0, max_mut_amt)
        op = choice((add, sub))
        new_val = op(value, param.dtype((param.max_val - param.min_val) * mut_amt))
        if new_val > param.max_val:
            return param.max_val
        elif new_val < param.min_val:
            return param.min_val
        else:
            return new_val
    else:
        return value