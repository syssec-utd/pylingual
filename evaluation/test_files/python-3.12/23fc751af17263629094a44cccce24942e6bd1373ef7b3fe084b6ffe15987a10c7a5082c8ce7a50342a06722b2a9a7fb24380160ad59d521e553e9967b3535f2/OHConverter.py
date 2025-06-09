import pandas as pd

class Converter:

    def __init__(self, full_df, cat_feats, oh_col):
        self.col = list(full_df.columns)
        self.oh_col = oh_col
        self.oh_dict = {}
        self.cat_feats = cat_feats
        self.binary_cats = []
        for cat_f in cat_feats:
            if len(full_df[cat_f].unique()) <= 2:
                self.binary_cats.append(cat_f)
        for cat_f in cat_feats:
            values = list(full_df[cat_f].unique())
            for v in values:
                cat_feat_simple = f'{cat_f}_{v}'
                cat_feat_ordered = f"{''.join(['0'] * (4 - len(str(cat_f))))}{str(cat_f)}_{v}"
                cat_feat_binary_ordered = f"{''.join(['0'] * (4 - len(str(cat_f))))}{str(cat_f)}"
                if cat_feat_simple in oh_col:
                    self.oh_dict[cat_feat_simple] = {cat_f: v}
                elif cat_feat_ordered in oh_col:
                    self.oh_dict[cat_feat_ordered] = {cat_f: v}
                elif cat_feat_binary_ordered in oh_col:
                    self.oh_dict[cat_feat_binary_ordered] = {cat_f: 'binary'}
                else:
                    self.oh_dict[cat_f] = {cat_f: 'binary'}
        self.dict_feat_idx = {}
        for idx, col in enumerate(self.oh_col):
            cat_name = col.split('_')[0]
            value_name = '_'.join(col.split('_')[1:])
            if cat_name != 'output':
                if str(int(cat_name)) in self.dict_feat_idx.keys():
                    self.dict_feat_idx[str(int(cat_name))][value_name] = idx
                else:
                    self.dict_feat_idx[str(int(cat_name))] = {value_name: idx}

    def convert_to_oh(self, data):
        out_data = [0] * (len(self.oh_col) - 1)
        for idx, c_value in enumerate(data):
            if str(idx) in self.cat_feats and str(idx) not in self.binary_cats:
                try:
                    idx_oh = self.dict_feat_idx[str(idx)][c_value]
                except KeyError:
                    try:
                        idx_oh = self.dict_feat_idx[str(idx)][str(c_value)]
                    except KeyError:
                        idx_oh = self.dict_feat_idx[str(idx)][str(int(float(c_value)))]
                out_data[idx_oh] = 1
            else:
                try:
                    idx_oh = self.oh_col.index(str(idx))
                except ValueError:
                    len_idx = len(str(idx))
                    extended_idx = '0' * (4 - len_idx) + str(idx)
                    idx_oh = self.oh_col.index(extended_idx)
                out_data[idx_oh] = c_value
        return out_data

    def convert(self, data):
        if type(data) == pd.DataFrame:
            data = data.to_numpy().tolist()
        output = []
        for d in data:
            out_row = [0] * (len(self.col) - 1)
            for idx, f in enumerate(d):
                of_feat_col = self.oh_col[idx]
                if of_feat_col in self.oh_dict.keys():
                    col_idx, v = list(self.oh_dict[of_feat_col].items())[0]
                    if v == 'binary':
                        out_row[int(col_idx)] = f
                    elif f == 1:
                        out_row[int(col_idx)] = v
                else:
                    out_row[int(of_feat_col)] = f
            output.append(out_row)
        return output