"""
Settings, constants and options used package-wide.

In future these settings may be stored in a configuration file instead.

References
----------
.. [Cheng2013]
    Cheng, H., Lawrence Edwards, R., Shen, C.-C., Polyak, V.J., Asmerom, Y.,
    Woodhead, J., Hellstrom, J., Wang, Y., Kong, X., Spötl, C., Wang, X.,
    Calvin Alexander, E., 2013. Improvements in 230Th dating, 230Th and
    234U half-life values, and U–Th isotopic measurements by multi-collector
    inductively coupled plasma mass spectrometry. Earth and Planetary
    Science Letters 371–372, 82–91. https://doi.org/10.1016/j.epsl.2013.04.006
.. [Hiess2012]
    Hiess, J., Condon, D.J., McLean, N., Science, S.N., 2012. 238U/235U
    systematics in terrestrial uranium-bearing minerals. Science.
    https://doi.org/10.1126/science.1215507
.. [Jaffey1971]
    Jaffey, A.H., Flynn, K.F., Glendeni, L.E., Bentley, W.C., Essling, A.M.,
    1971. Precision measurement of half-lives and specific activities of
    U-235 and U-238. Physical Review C 4, 1889–1906.
.. [Jerome2020]
    Jerome, S., Bobin, C., Cassette, P., Dersch, R., Galea, R., Liu, H., Honig,
    A., Keightley, J., Kossert, K., Liang, J., Marouli, M., Michotte, C.,
    Pommé, S., Röttger, S., Williams, R., Zhang, M., 2020. Half-life
    determination and comparison of activity standards of 231Pa. Applied
    Radiation and Isotopes 155, 108837.
    https://doi.org/10.1016/j.apradiso.2019.108837
.. [Ludwig1977]
    Ludwig, K.R., 1977. Effect of initial radioactive-daughter disequilibrium on
    U-Pb isotope apparent ages of young minerals. Journal of Research of
    the US Geological Survey 5, 663–667.
.. [Robert1969]
    Robert, J., Miranda, C.F., Muxart, R., 1969. Mesure de la période du
    protactinium 231 par microcalorimétrie. Radiochimica Acta 11, 104–108.

"""
import numpy as np
lam238 = np.log(2) / (4468300000.0 * 1e-06)
lam235 = np.log(2) / (703810000.0 * 1e-06)
lam234 = np.log(2) / (245620 * 1e-06)
lam231 = np.log(2) / (32765.0 * 1e-06)
lam230 = np.log(2) / (75584 * 1e-06)
lam227 = np.log(2) / (22.0 * 1e-06)
lam226 = np.log(2) / (1600.0 * 1e-06)
lam210 = np.log(2) / (22.0 * 1e-06)
s238 = lam238 ** 2 / np.log(2) * (2400000.0 * 1e-06)
s235 = lam235 ** 2 / np.log(2) * (480000.0 * 1e-06)
s234 = lam234 ** 2 / np.log(2) * (130.0 * 1e-06)
s231 = lam231 ** 2 / np.log(2) * (110.0 * 1e-06)
s230 = lam230 ** 2 / np.log(2) * (55.0 * 1e-06)
s227 = 0.0
s226 = lam226 ** 2 / np.log(2) * (7.0 * 1e-06)
s210 = 0.0
cor_238_234 = 0.95194
cor_238_230 = 0.71046
cor_234_230 = 0.67631
U = 137.818
sU = 0.0225
A48_eq = 1.0
A08_eq = 1.0
A68_eq = 1.0
A15_eq = 1.0
secular_eq = True
rng = np.random.default_rng()
h = 1.4
mswd_ci_thresholds = (0.85, 0.95)
mswd_wav_ci_thresholds = (0.85, 0.95)
IsoLam238 = 1.55125e-10 * 10 ** 6
IsoLam234 = 2.8338e-06 * 10 ** 6
IsoLam230 = 9.19525e-06 * 10 ** 6
IsoLam235 = 9.8485e-10 * 10 ** 6
IsoLam231 = 2.13276e-05 * 10 ** 6
IsoS238 = 0.107 * IsoLam238 / 200.0
IsoS234 = 0.2 * IsoLam234 / 200.0
IsoS230 = 0.3 * IsoLam230 / 200.0
IsoS235 = 0.136 * IsoLam235 / 200.0
IsoU = 137.88
file_ext = '.pdf'
tight_layout = True
sort_ages = False
comma_sep_thousands = False
exp_font_size = 9
hide_right_spine = False
hide_top_spine = False
wav_marker_width = 0.6
sci_limits = [-3, 4]
show_major_gridlines = False
show_minor_gridlines = False
show_minor_ticks = False
tick_label_size = 9
wav_major_gridlines = True
wav_minor_gridlines = False
conc_age_bounds = [0.01, 4600]
diseq_conc_age_bounds = [[0.001, 100.0], [0.001, 2.5], [0.001, 1.5]]
plot_age_markers = True
label_markers = True
ellipse_label_va = 'bottom'
ellipse_label_ha = 'left'
prefix_in_label = True
every_second_threshold = 8
individualised_labels = True
offset_factor = 0.8
rotate_conc_labels = True
perpendicular_rotation = False
remove_overlaps = False
axis_labels_kw = {'color': 'k', 'fontsize': 10}
conc_age_ellipse_kw = {'alpha': 1.0, 'edgecolor': 'black', 'facecolor': 'white', 'linewidth': 0.5, 'zorder': 20}
conc_env_kw = {'alpha': 1.0, 'edgecolor': 'none', 'facecolor': '#FFFFC0', 'linestyle': '--', 'linewidth': 0.0, 'zorder': 18}
conc_env_line_kw = {'alpha': 1.0, 'color': 'black', 'linestyle': '--', 'linewidth': 0.8, 'zorder': 18}
conc_intercept_ellipse_kw = {'alpha': 0.6, 'edgecolor': 'black', 'facecolor': '#C5F7C5', 'linewidth': 1.0, 'zorder': 25}
conc_intercept_markers_kw = {'alpha': 0.5, 'markeredgecolor': 'none', 'markerfacecolor': 'black', 'linewidth': 0, 'marker': ',', 'markersize': 4, 'zorder': 25}
conc_line_kw = {'alpha': 1.0, 'color': 'black', 'linestyle': '-', 'linewidth': 0.8, 'zorder': 19}
conc_markers_kw = {'alpha': 1.0, 'linewidth': 0, 'marker': 'o', 'markeredgecolor': 'black', 'markerfacecolor': 'white', 'markersize': 4, 'zorder': 20}
conc_text_kw = {'annotation_clip': False, 'clip_on': True, 'color': 'black', 'fontsize': 8, 'horizontalalignment': 'left', 'textcoords': 'offset points', 'verticalalignment': 'center', 'xytext': (3, 3), 'zorder': 21}
dp_ellipse_kw = {'alpha': 0.8, 'edgecolor': 'black', 'facecolor': '#1FB714', 'linewidth': 0.5, 'zorder': 30}
dp_label_kw = {'color': 'black', 'fontsize': 8, 'horizontalalignment': 'center', 'textcoords': 'offset points', 'verticalalignment': 'center', 'xytext': (10, 0), 'zorder': 30}
fig_kw = {'dpi': 300, 'facecolor': 'whitesmoke', 'figsize': (4.72, 4.012), 'tight_layout': True}
gridlines_kw = {'alpha': 1.0, 'color': 'black', 'linestyle': ':', 'linewidth': 0.5}
hist_bars_kw = {'alpha': 0.75, 'edgecolor': 'red', 'facecolor': 'green', 'histtype': 'step', 'linewidth': 0.75}
hist_fig_kw = {'dpi': 300, 'facecolor': 'whitesmoke', 'figsize': (4.72, 4.012), 'tight_layout': True}
major_ticks_kw = {'color': 'black', 'direction': 'in', 'length': 4, 'width': 0.5}
minor_ticks_kw = {'color': 'black', 'direction': 'in', 'length': 2, 'width': 0.5}
pb76_line_kw = {'alpha': 0.5, 'color': 'blue', 'linestyle': '--', 'linewidth': 1.0, 'zorder': 10}
renv_kw = {'alpha': 0.3, 'edgecolor': 'none', 'facecolor': 'blue', 'linewidth': 0.0, 'zorder': 9}
renv_line_kw = {'alpha': 1.0, 'color': 'blue', 'linewidth': 0.0, 'zorder': 9}
rline_kw = {'alpha': 1.0, 'color': 'blue', 'linestyle': '-', 'linewidth': 0.8, 'zorder': 10}
scatter_markers_kw = {'alpha': 0.3, 'markeredgecolor': 'none', 'linewidth': 0, 'markerfacecolor': 'black', 'marker': ',', 'markersize': 4, 'zorder': 1}
spine_kw = {'color': 'k', 'linewidth': 0.8}
subplot_kw = {'facecolor': 'white'}
wav_env_kw = {'alpha': 0.8, 'facecolor': 'palegreen', 'edgecolor': 'none', 'linestyle': '--', 'linewidth': 0.0, 'zorder': 9}
wav_fig_kw = {'dpi': 300, 'facecolor': 'whitesmoke', 'figsize': (4.72, 4.012), 'tight_layout': True}
wav_line_kw = {'alpha': 1.0, 'color': 'black', 'linestyle': '-', 'linewidth': 1.0, 'zorder': 10}
wav_markers_kw = {'alpha': 1.0, 'color': 'lightblue', 'zorder': 31}
wav_markers_rand_kw = {'alpha': 1.0, 'color': 'blue', 'zorder': 30}