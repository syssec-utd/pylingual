def angles(self, zfill=3):
    """
    Returns the internal angles of all elements and the associated statistics 
    """
    elements = self.elements.sort_index(axis=1)
    etypes = elements['type', 'argiope'].unique()
    out = []
    for etype in etypes:
        etype_info = ELEMENTS[etype]
        angles_info = etype_info.angles
        loc = elements['type', 'argiope', ''] == etype
        index = elements.loc[loc].index
        angles_data = self.split(into='angles', loc=loc, at='coords')
        data = angles_data.values.reshape(index.size, angles_info.shape[0], angles_info.shape[1], 3)
        edges = data[:, :, [0, 2], :] - data[:, :, 1:2, :]
        edges /= np.linalg.norm(edges, axis=3).reshape(index.size, angles_info.shape[0], 2, 1)
        angles = np.degrees(np.arccos((edges[:, :, 0] * edges[:, :, 1]).sum(axis=2)))
        deviation = angles - etype_info.optimal_angles
        angles_df = pd.DataFrame(index=index, data=angles, columns=pd.MultiIndex.from_product([['angles'], ['a' + '{0}'.format(s).zfill(zfill) for s in range(angles_info.shape[0])]]))
        deviation_df = pd.DataFrame(index=index, data=deviation, columns=pd.MultiIndex.from_product([['deviation'], ['d' + '{0}'.format(s).zfill(zfill) for s in range(angles_info.shape[0])]]))
        df = pd.concat([angles_df, deviation_df], axis=1).sort_index(axis=1)
        df['stats', 'max_angle'] = df.angles.max(axis=1)
        df['stats', 'min_angle'] = df.angles.min(axis=1)
        df['stats', 'max_angular_deviation'] = df.deviation.max(axis=1)
        df['stats', 'min_angular_deviation'] = df.deviation.min(axis=1)
        df['stats', 'max_abs_angular_deviation'] = abs(df.deviation).max(axis=1)
        df = df.sort_index(axis=1)
        out.append(df)
    out = pd.concat(out).sort_index(axis=1)
    return out