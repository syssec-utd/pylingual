def std_coef_plot(self, num_of_features=None, server=False):
    """
        Plot a GLM model"s standardized coefficient magnitudes.

        :param num_of_features: the number of features shown in the plot.
        :param server: ?

        :returns: None.
        """
    assert_is_type(num_of_features, None, I(int, lambda x: x > 0))
    if self._model_json['algo'] != 'glm':
        raise H2OValueError('This function is available for GLM models only')
    plt = _get_matplotlib_pyplot(server)
    if not plt:
        return
    unsorted_norm_coef = self.coef_norm().items()
    drop_intercept = [tup for tup in unsorted_norm_coef if tup[0] != 'Intercept']
    norm_coef = sorted(drop_intercept, key=lambda x: abs(x[1]), reverse=True)
    signage = []
    for element in norm_coef:
        if element[1] >= 0:
            signage.append('#1F77B4')
        else:
            signage.append('#FF7F0E')
    feature_labels = [tup[0] for tup in norm_coef]
    norm_coef_magn = [abs(tup[1]) for tup in norm_coef]
    pos = range(len(feature_labels))[::-1]
    val = norm_coef_magn
    if num_of_features is None:
        num_of_features = len(val)
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    if num_of_features == 1:
        plt.barh(pos[0], val[0], align='center', height=0.8, color=signage[0], edgecolor='none')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_color('#7B7B7B')
        ax.spines['left'].set_color('#7B7B7B')
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        plt.yticks([0], feature_labels[0])
        ax.margins(None, 0.5)
    else:
        plt.barh(pos[0:num_of_features], val[0:num_of_features], align='center', height=0.8, color=signage[0:num_of_features], edgecolor='none')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_color('#7B7B7B')
        ax.spines['left'].set_color('#7B7B7B')
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        plt.yticks(pos[0:num_of_features], feature_labels[0:num_of_features])
        ax.margins(None, 0.05)
    if '#1F77B4' in signage[0:num_of_features] and '#FF7F0E' not in signage[0:num_of_features]:
        color_ids = ('Positive',)
        markers = [plt.Line2D([0, 0], [0, 0], color=color, marker='s', linestyle='') for color in signage[0:num_of_features]]
        lgnd = plt.legend(markers, color_ids, numpoints=1, loc='best', frameon=False, fontsize=13)
        lgnd.legendHandles[0]._legmarker.set_markersize(10)
    elif '#FF7F0E' in signage[0:num_of_features] and '#1F77B4' not in signage[0:num_of_features]:
        color_ids = ('Negative',)
        markers = [plt.Line2D([0, 0], [0, 0], color=color, marker='s', linestyle='') for color in set(signage[0:num_of_features])]
        lgnd = plt.legend(markers, color_ids, numpoints=1, loc='best', frameon=False, fontsize=13)
        lgnd.legendHandles[0]._legmarker.set_markersize(10)
    else:
        color_ids = ('Positive', 'Negative')
        markers = [plt.Line2D([0, 0], [0, 0], color=color, marker='s', linestyle='') for color in ['#1F77B4', '#FF7F0E']]
        lgnd = plt.legend(markers, color_ids, numpoints=1, loc='best', frameon=False, fontsize=13)
        lgnd.legendHandles[0]._legmarker.set_markersize(10)
        lgnd.legendHandles[1]._legmarker.set_markersize(10)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_color('#7B7B7B')
    ax.spines['left'].set_color('#7B7B7B')
    plt.yticks(pos[0:num_of_features], feature_labels[0:num_of_features])
    plt.tick_params(axis='x', which='minor', bottom='off', top='off', labelbottom='off')
    plt.title('Standardized Coef. Magnitudes: H2O GLM', fontsize=20)
    if not server:
        plt.show()