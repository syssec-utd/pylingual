from PEPit import PEP
from PEPit.operators import MonotoneOperator
from PEPit.primitive_steps import proximal_step

def wc_proximal_point(alpha, n, verbose=1):
    """
    Consider the monotone inclusion problem

        .. math:: \\mathrm{Find}\\, x:\\, 0\\in Ax,

    where :math:`A` is maximally monotone. We denote :math:`J_A = (I + A)^{-1}` the resolvents of :math:`A`.

    This code computes a worst-case guarantee for the **proximal point** method, and looks for a low-dimensional
    worst-case example nearly achieving this worst-case guarantee using the trace heuristic.
    
    That is, it computes the smallest possible :math:`\\tau(n, \\alpha)` such that the guarantee

        .. math:: \\|x_n - x_{n-1}\\|^2 \\leqslant \\tau(n, \\alpha) \\|x_0 - x_\\star\\|^2,

    is valid, where :math:`x_\\star` is such that :math:`0 \\in Ax_\\star`. Then, it looks for a low-dimensional nearly achieving this
    performance.

    **Algorithm**: The proximal point algorithm for monotone inclusions is described as follows, for :math:`t \\in \\{ 0, \\dots, n-1\\}`,

        .. math:: x_{t+1} = J_{\\alpha A}(x_t),

    where :math:`\\alpha` is a step-size.

    **Theoretical guarantee**: A tight theoretical guarantee can be found in [1, section 4].

        .. math:: \\|x_n - x_{n-1}\\|^2 \\leqslant \\frac{\\left(1 - \\frac{1}{n}\\right)^{n - 1}}{n} \\|x_0 - x_\\star\\|^2.

    **Reference**:

    `[1] G. Gu, J. Yang (2020). Tight sublinear convergence rate of the proximal point algorithm for maximal
    monotone inclusion problem. SIAM Journal on Optimization, 30(3), 1905-1921.
    <https://epubs.siam.org/doi/pdf/10.1137/19M1299049>`_

    Args:
        alpha (float): the step-size.
        n (int): number of iterations.
        verbose (int): Level of information details to print.
                        
                        - -1: No verbose at all.
                        - 0: This example's output.
                        - 1: This example's output + PEPit information.
                        - 2: This example's output + PEPit information + CVXPY details.

    Returns:
        pepit_tau (float): worst-case value.
        theoretical_tau (float): theoretical value.

    Example:
        >>> pepit_tau, theoretical_tau = wc_proximal_point(alpha=2.2, n=11, verbose=1)
        (PEPit) Setting up the problem: size of the main PSD matrix: 13x13
        (PEPit) Setting up the problem: performance measure is minimum of 1 element(s)
        (PEPit) Setting up the problem: Adding initial conditions and general constraints ...
        (PEPit) Setting up the problem: initial conditions and general constraints (1 constraint(s) added)
        (PEPit) Setting up the problem: interpolation conditions for 1 function(s)
                         function 1 : Adding 132 scalar constraint(s) ...
                         function 1 : 132 scalar constraint(s) added
        (PEPit) Compiling SDP
        (PEPit) Calling SDP solver
        (PEPit) Solver status: optimal (solver: SCS); optimal value: 0.03504735907840766
        (PEPit) Postprocessing: 2 eigenvalue(s) > 1.885183851963194e-06 before dimension reduction
        (PEPit) Calling SDP solver
        (PEPit) Solver status: optimal (solver: SCS); objective value: 0.03503739338571882
        (PEPit) Postprocessing: 2 eigenvalue(s) > 1.9044504527414672e-06 after dimension reduction
        *** Example file: worst-case performance of the Proximal Point Method***
                PEPit example:           ||x(n) - x(n-1)||^2 == 0.0350374 ||x0 - xs||^2
                Theoretical guarantee:   ||x(n) - x(n-1)||^2 <= 0.0350494 ||x0 - xs||^2

    """
    problem = PEP()
    A = problem.declare_function(MonotoneOperator)
    xs = A.stationary_point()
    x0 = problem.set_initial_point()
    problem.set_initial_condition((x0 - xs) ** 2 <= 1)
    x = x0
    for _ in range(n):
        previous_x = x
        x, _, _ = proximal_step(previous_x, A, alpha)
    problem.set_performance_metric((x - previous_x) ** 2)
    pepit_verbose = max(verbose, 0)
    pepit_tau = problem.solve(verbose=pepit_verbose, dimension_reduction_heuristic='trace')
    theoretical_tau = (1 - 1 / n) ** (n - 1) / n
    if verbose != -1:
        print('*** Example file: worst-case performance of the Proximal Point Method***')
        print('\tPEPit example:\t\t ||x(n) - x(n-1)||^2 == {:.6} ||x0 - xs||^2'.format(pepit_tau))
        print('\tTheoretical guarantee:\t ||x(n) - x(n-1)||^2 <= {:.6} ||x0 - xs||^2'.format(theoretical_tau))
    return (pepit_tau, theoretical_tau)
if __name__ == '__main__':
    pepit_tau, theoretical_tau = wc_proximal_point(alpha=2.2, n=11, verbose=1)