"""Testing the mask conversion to and from contour lines"""
import pathlib
from typing import TypedDict
import matplotlib.pyplot as plt
import numpy as np
from rai.metrics import dice
from .convert import Contours, Grid, contours_to_mask, mask_to_contours
HERE = pathlib.Path(__file__).parent
FIGURE_DIR = HERE / 'test_figures'

def test_conversion_round_trip():
    """Test a round trip of contours -> mask -> contours"""
    cases: list[_TestCase] = []
    cases.append({'title': 'edge-of-mask', 'x_grid': np.array([0, 1, 2, 3]), 'y_grid': np.array([10, 12, 14, 16]), 'contours': [np.array([(9, -0.5), (9, 2), (14, 2), (14, -0.5)])], 'dice_lower_bound': 0.9})
    t = np.linspace(0, 2 * np.pi)
    x = 1.5 * np.sin(t)
    y = np.cos(t) + 0.5
    yx_coords = np.concatenate([y[:, None], x[:, None]], axis=-1)
    cases.append({'title': 'offset-ellipse', 'x_grid': np.linspace(-2, 2, 21), 'y_grid': np.linspace(-2, 2, 31), 'contours': [yx_coords], 'dice_lower_bound': 0.99})
    cases.append({'title': 'right-angle-triangle', 'x_grid': np.linspace(0, 4, 5), 'y_grid': np.linspace(0, 10, 11), 'contours': [np.array([(0, 0), (10, 0), (0, 2), (0, 0)])], 'dice_lower_bound': 0.81})
    x_left = np.sin(t)
    y = np.cos(t)
    x_right = x_left + 2
    contours = [np.concatenate([y[:, None], x_left[:, None]], axis=-1), np.concatenate([y[:, None], x_right[:, None]], axis=-1)]
    cases.append({'title': 'two-small-abutting-circles', 'x_grid': np.linspace(-1, 4, 13), 'y_grid': np.linspace(-2, 2, 6), 'contours': contours, 'dice_lower_bound': 0.94})
    for case in cases:
        _run_round_trip_test(**case)

class _TestCase(TypedDict):
    title: str
    x_grid: Grid
    y_grid: Grid
    contours: Contours
    dice_lower_bound: float

def _run_round_trip_test(title: str, x_grid: Grid, y_grid: Grid, contours: Contours, dice_lower_bound: float):
    mask = contours_to_mask(x_grid, y_grid, contours)
    round_trip_contours = mask_to_contours(x_grid, y_grid, mask)
    assert dice.from_contours(a=contours, b=round_trip_contours) >= dice_lower_bound
    (fig, ax) = plt.subplots()
    c = ax.pcolormesh(x_grid, y_grid, mask, shading='nearest')
    fig.colorbar(c)
    for contour in contours:
        ax.plot(contour[:, 1], contour[:, 0], 'C3', lw=4, label='original contour')
    for contour in round_trip_contours:
        ax.plot(contour[:, 1], contour[:, 0], 'k--', lw=2, label='round-trip contour')
    ax.set_aspect('equal')
    ax.set_title(title)
    fig.legend(loc='upper left')
    fig.savefig(FIGURE_DIR / f'{title}.png')

def test_round_trip_with_nested_contours():
    """Test round trip with nested contours"""