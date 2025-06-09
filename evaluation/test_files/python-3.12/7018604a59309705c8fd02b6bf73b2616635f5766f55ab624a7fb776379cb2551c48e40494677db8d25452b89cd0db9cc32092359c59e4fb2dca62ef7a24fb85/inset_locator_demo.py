"""
==================
Inset Locator Demo
==================

"""
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
fig, (ax, ax2) = plt.subplots(1, 2, figsize=[5.5, 2.8])
axins = inset_axes(ax, width=1.3, height=0.9)
axins2 = inset_axes(ax, width='30%', height='40%', loc=3)
axins3 = inset_axes(ax2, width='30%', height=1.0, loc=2)
axins4 = inset_axes(ax2, width='20%', height='20%', loc=4, borderpad=1)
for axi in [axins, axins2, axins3, axins4]:
    axi.tick_params(labelleft=False, labelbottom=False)
plt.show()
fig = plt.figure(figsize=[5.5, 2.8])
ax = fig.add_subplot(121)
axins = inset_axes(ax, width='50%', height='75%', bbox_to_anchor=(0.2, 0.4, 0.6, 0.5), bbox_transform=ax.transAxes, loc=3)
ax.add_patch(plt.Rectangle((0.2, 0.4), 0.6, 0.5, ls='--', ec='c', fc='none', transform=ax.transAxes))
ax.set(xlim=(0, 10), ylim=(0, 10))
ax2 = fig.add_subplot(222)
axins2 = inset_axes(ax2, width='30%', height='50%')
ax3 = fig.add_subplot(224)
axins3 = inset_axes(ax3, width='100%', height='100%', bbox_to_anchor=(0.7, 0.5, 0.3, 0.5), bbox_transform=ax3.transAxes)
ax2.add_patch(plt.Rectangle((0, 0), 1, 1, ls='--', lw=2, ec='c', fc='none'))
ax3.add_patch(plt.Rectangle((0.7, 0.5), 0.3, 0.5, ls='--', lw=2, ec='c', fc='none'))
for axi in [axins2, axins3, ax2, ax3]:
    axi.tick_params(labelleft=False, labelbottom=False)
plt.show()
fig = plt.figure(figsize=[5.5, 2.8])
ax = fig.add_subplot(131)
axins = inset_axes(ax, width='100%', height='100%', bbox_to_anchor=(1.05, 0.6, 0.5, 0.4), bbox_transform=ax.transAxes, loc=2, borderpad=0)
axins.tick_params(left=False, right=True, labelleft=False, labelright=True)
axins2 = inset_axes(ax, width=0.5, height=0.4, bbox_to_anchor=(0.33, 0.25), bbox_transform=ax.transAxes, loc=3, borderpad=0)
ax2 = fig.add_subplot(133)
ax2.set_xscale('log')
ax2.set(xlim=(1e-06, 1000000.0), ylim=(-2, 6))
axins3 = inset_axes(ax2, width='100%', height='100%', bbox_to_anchor=(0.01, 2, 1000.0, 3), bbox_transform=ax2.transData, loc=2, borderpad=0)
from matplotlib.transforms import blended_transform_factory
transform = blended_transform_factory(fig.transFigure, ax2.transAxes)
axins4 = inset_axes(ax2, width='16%', height='34%', bbox_to_anchor=(0, 0, 1, 1), bbox_transform=transform, loc=8, borderpad=0)
plt.show()