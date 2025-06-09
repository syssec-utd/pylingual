"""
Visualizing a 3d field interactively
====================================

This example demonstrates how to display 3d data interactively using the
`napari <https://napari.org>`_ viewer.
"""
import numpy as np
from pde import CartesianGrid, ScalarField
grid = CartesianGrid([[0, 2 * np.pi]] * 3, 64)
data = ScalarField.from_expression(grid, '(cos(2 * x) * sin(3 * y) + cos(2 *  z))**2')
data += ScalarField.random_normal(grid, std=0.1)
data.label = '3D Field'
data.plot_interactive()