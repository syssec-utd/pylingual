import pandas as pd
import numpy as np
import anndata
import math
import os
import time
import xgboost
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from scipy.stats import zscore
from scipy.stats import t
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt
from pyInfinityFlow.fcs_io import FCSFileObject
from pyInfinityFlow.Transformations import apply_logicle
from pyInfinityFlow.Transformations import apply_inverse_logicle
from pyInfinityFlow.Debugging_Utilities import printv
from pyInfinityFlow.Plotting_Utilities import plot_feature_over_x_y_coordinates_and_save_fig
from pyInfinityFlow.Plotting_Utilities import plot_markers_df
FREQUENT_LINEAR_CHANNELS = np.array(['FSC-W', 'FSC-H', 'FSC-A', 'SSC-B-W', 'SSC-B-H', 'SSC-B-ASSC-W', 'SSC-H', 'SSC-A', 'umap-x', 'umap-y'])

class InfinityFlowFileHandler:
    """

    Class to specify how to handle InfinityMarker files.

    Parameters
    ----------
    ordered_reference_backbone : numpy.Array[str]
        Array of backbone channel names

    Attributes
    ----------
    list_infinity_markers : list[str]
        List of the InfinityMarker names that the object can handle
    handles : dict{dicts}
        A dictionary with a key for every InfinityMarker. Each key stores a 
        dictionary with the following values to specify how to handle the given 
        InfinityMarker:
            - ["name"]: (str) InfinityMarker name
            - ["file_name"]: (str) .fcs file name for the InfinityMarker
            - ["directory"]: (str) path to the directory where the .fcs file is saved
            - ["reference_backbone_channels"]: (list[str]) list of the channel             names to use for the backbone in the reference .fcs file (the events             used for prediction)
            - ["backbone_channels"]: (list[str]) list of the channel names to             use for the backbone in the reference .fcs file (the events used             for XGBoost regression model fitting)
            - ["prediction_channel"]: (str) channel name of the InfinityMarker,             the channel name to predict
            - ["train_indices"]: (numpy.Array[int]) indices of the InfinityMarker             .fcs file to use for fitting
            - ["test_indices"]: (numpy.Array[int]) indices of the InfinityMarker             .fcs file to use for validation
            - ["pool_indices"]: (numpy.Array[int]) indices of the InfinityMarker             .fcs file to use for pooling into the reference to use
    use_isotype_controls : bool
        If True, pipeline functions will require Isotype controls
    isotype_control_names : numpy.Array[str]
        Array of InfinityMarker names
    ordered_reference_backbone : numpy.Array[str]
        Array of backbone channel names

    """

    def __init__(self, ordered_reference_backbone):
        self.list_infinity_markers = []
        self.handles = {}
        self.use_isotype_controls = False
        self.isotype_control_names = []
        self.ordered_reference_backbone = ordered_reference_backbone

    def add_handle(self, name, file_name, directory, reference_backbone_channels, backbone_channels, prediction_channel, train_indices, test_indices, pool_indices):
        """Add a new InfinityMarker handle to the InfinityFlowFileHandler

        Parameters
        ----------
        name : str
            The name of the InfinityMarker (Required)
        file_name : str
            The .fcs file name for the InfinityMarker (Required)
        directory : str
            The path to the directory where the .fcs file is saved (Required)
        reference_backbone_channels : list[str]
            list of the channel names to use for the backbone in the reference             .fcs file (the events used for prediction)
        backbone_channels : list[str]
            list of the channel names to use for the backbone in the reference             .fcs file (the events used for XGBoost regression model fitting)
        prediction_channel : str
            The channel name of the InfinityMarker, the channel name to predict
        train_indices : numpy.Array[int]
            The indices of the InfinityMarker .fcs file to use for fitting
        test_indices : numpy.Array[int]
            The indices of the InfinityMarker .fcs file to use for validation
        pool_indices : numpy.Array[int]
            The indices of the InfinityMarker .fcs file to use for pooling into             the reference to use

        Returns
        -------
        None
            Adds the given InfinityMarker handle to InfinityFlowFileHandler,             where handles is a dictionary, and each entry, named by the             InfinityMarker name is a dictionary with the following keys:
                - ["name"]
                - ["file_name"]
                - ["directory"]
                - ["reference_backbone_channels"]
                - ["backbone_channels"]
                - ["prediction_channel"]
                - ["train_indices"]
                - ["test_indices"]
                - ["pool_indices"]

        """
        self.list_infinity_markers.append(name)
        self.handles[name] = {'name': name, 'file_name': file_name, 'directory': directory, 'reference_backbone_channels': reference_backbone_channels, 'backbone_channels': backbone_channels, 'prediction_channel': prediction_channel, 'train_indices': train_indices, 'test_indices': test_indices, 'pool_indices': pool_indices}

    def __repr__(self):
        tmp_repr_str = 'InfinityFlowFileHandler Object from pyInfinityFlow\n'
        if len(self.list_infinity_markers) > 0:
            tmp_repr_str += '\t.handles the following InfinityMarkers:\n\t\t\t{}\n\n\tHeld in the InfinityFlowFileHandler.handles dictionary\n\n'.format('\n\t\t\t'.join(self.list_infinity_markers))
            tmp_repr_str += '\tInfinityFlowFileHandler.list_infinity_markers holds ordered list of InfinityMarkers\n\n'
        return tmp_repr_str

class CombinedRegressionModels:
    """
    Class to store XGBoost regression models, the settings used to fit the 
    model, and the validation metrics from testing.

    Attributes
    ----------
    ordered_training_channels : numpy.Array[str]
        The features used to train each of the regression models
    var_annotations : pandas.DataFrame
        The feature parameters for the training features of backbone
    infinity_markers : numpy.Array[str]
        The response variables the regression models can predict
    regression_models : dict{InfinityMarker: xgboost.XGBRegressor}
        Dictionary of response variable to regression model for prediction
    parameter_annotations : dict{InfinityMarker: Series}
        Dictionary of Series to specify the feature parameter (was logicle         applied to the response varialble)
    infinity_channels : dict{InfinityMarker: str}
        The channel name for the InfinityMarker ("Response Variable")
    validation_metrics : dict{InfinityMarker: dict}
        Provide validation metrics as an object with each InfinityMarker as a key
    
    """

    def __init__(self, ordered_training_channels, var_annotations, infinity_markers, regression_models, parameter_annotations, infinity_channels):
        self.ordered_training_channels = ordered_training_channels
        self.var_annotations = var_annotations
        self.infinity_markers = infinity_markers
        self.regression_models = regression_models
        self.parameter_annotations = parameter_annotations
        self.infinity_channels = infinity_channels
        self.validation_metrics = {}

    def __repr__(self):
        tmp_repr_str = 'CombinedRegressionModels Object from pyInfinityFlow\n'
        tmp_repr_str += '\tContains regression models for the following InfinityMarkers (Response Variables):\n{}\n\n'.format(','.join(self.infinity_markers))
        tmp_repr_str += '\tUses the following backbone (Explanatory Variables):\n{}\n\n'.format(','.join(self.ordered_training_channels))
        tmp_repr_str += 'The object holds the following variables:\n\tordered_training_channels\n\tvar_annotations\n\tinfinity_markers\n\tregression_models\n\tparameter_annotations\n\tinfinity_channels\n\tvalidation_metrics\n\n'
        tmp_repr_str += '\tAccess regression models as dictionary with the InfinityMarker as the key: \n'
        tmp_repr_str += '\t\tEg. CombinedRegressionModels.regression_models["{}"]\n\n'.format(self.infinity_markers[0])
        return tmp_repr_str

def read_annotation_table(input_file):
    """
    Read in an annotation file. Annotation files are used to dictate how to
    carry out the regression models.

    Arguments
    ---------
    input_file : str
        The path to the file containing the annotation information. (Should be 
        either comma separated (.csv) or tab separated (.tsv or .txt))
        (Required)
    
    use_raw_feature_names : bool
        Optional argument. If True, only use the raw feature names from 
        input_anndata.var.index. If False, add the "name" values for the 
        features in input_anndata.var.index, formatted as <index>:<name>. 
        (Default: True)

    add_index_names : bool
        Optional argument. If True, will add the input_anndata.obs.index as the 
        index of the returned DataFrame. If False, the index will simply be the 
        integers from range(len(input_anndata.obs.shape[0]))

    Returns
    -------
    pandas.DataFrame
        DataFrame of the annotation table

    """
    try:
        format_specifier = input_file[-4:].lower()
        if format_specifier == '.tsv' or format_specifier == '.txt':
            return pd.read_table(input_file)
        else:
            return pd.read_csv(input_file)
    except:
        raise ImportError('Failed to import the file {}. Only ".tsv ".csv and ".txt (tab-delimited) files are accepted.'.format(input_file))

def anndata_to_df(input_anndata, use_raw_feature_names=True, add_index_names=True):
    """
    Function to quickly convert an AnnData object containing pyInfinityFlow
    formatted flow cytometry data to a pandas DataFrame object

    Arguments
    ---------
    input_anndata : anndata.AnnData
        AnnData object for which to generate a DataFrame (Required)
    
    use_raw_feature_names : bool
        Optional argument. If True, only use the raw feature names from 
        input_anndata.var.index. If False, add the "name" values for the 
        features in input_anndata.var.index, formatted as <index>:<name>. 
        (Default: True)

    add_index_names : bool
        Optional argument. If True, will add the input_anndata.obs.index as the 
        index of the returned DataFrame. If False, the index will simply be the 
        integers from range(len(input_anndata.obs.shape[0]))

    Returns
    -------
    pandas.DataFrame
        DataFrame of the AnnData object's X attribute

    """
    tmp_feature_names = input_anndata.var.index.values
    if not use_raw_feature_names:
        try:
            tmp_feature_names = [f'{tmp_channel}:{tmp_name}' for (tmp_channel, tmp_name) in zip(tmp_feature_names, input_anndata.var['name'].values)]
        except:
            print("WARNING! Could not add feature names to channels. Make sure 'name' is a feature in input_anndata.var")
    if add_index_names:
        tmp_index = input_anndata.obs.index.values
    else:
        tmp_index = list(range(input_anndata.obs.shape[0]))
    return pd.DataFrame(input_anndata.X, columns=tmp_feature_names, index=tmp_index)

def calculate_centroids(input_df, groups):
    input_df['group'] = groups
    return pd.pivot_table(input_df, index='group', aggfunc=np.mean)

def pearson_corr_df_to_df(df1, df2):
    norm1 = df1 - df1.mean(axis=0)
    norm2 = df2 - df2.mean(axis=0)
    sqsum1 = (norm1 ** 2).sum(axis=0)
    sqsum2 = (norm2 ** 2).sum(axis=0)
    return norm1.T @ norm2 / np.sqrt(sqsum1.apply(lambda x: x * sqsum2))

def marker_finder(input_df, groups):
    """
    Function to find which features in input_df correspond best to which groups
    annotating the observations in input_df. The function will perform a 
    Pearson correlation of the input_df feature values to an "idealized" 
    group specific expression vector, where each observation in a given group
    is set to a value of 1, and the observations in other groups are set to 0.

    Arguments
    ---------
    input_df : pandas.DataFrame
        DataFrame with observations as index and features as columns (Required)
    
    groups : list[str]
        List-like of specified groups corresponding to observations from the 
        input_df. The order of groups should match the order in input_df.index
        (Required)

    Returns
    -------
    pandas.DataFrame
        DataFrame of the Pearson correlation test results. Each feature is
        assigned the cluster for which the test resulted in the highest Pearson
        correlation coefficient. The columns of the DataFrame will be 
        ["marker", "top_cluster", "pearson_r", "p_value"]
    """
    ideal_vectors = pd.get_dummies(groups)
    ideal_vectors.index = input_df.index.values
    degrees_f = input_df.shape[0] - 2
    r_df = pearson_corr_df_to_df(input_df, ideal_vectors)
    t_df = r_df * np.sqrt(degrees_f) / np.sqrt(1 - r_df ** 2)
    p_df = t_df.applymap(lambda x: t.sf(abs(x), df=degrees_f) * 2)
    top_cluster = r_df.idxmax(axis=1)
    top_r = r_df.max(axis=1)
    markers_df = pd.DataFrame({'marker': top_cluster.index.values, 'top_cluster': top_cluster.values, 'pearson_r': top_r.values, 'p_value': [p_df.loc[i, j] for (i, j) in zip(top_cluster.index.values, top_cluster.values)]})
    markers_df = markers_df.sort_values(by=['top_cluster', 'pearson_r'], ascending=[True, False])
    return markers_df

def read_fcs_into_anndata(fcs_file_path, obs_prefix='', batch_key=''):
    """
    Reads an .fcs file into an AnnData object.

    Arguments
    ---------
    fcs_file_path : str
        Path to the .fcs file (Required)
    
    obs_prefix : str
        String to append to the index values of the output 
        anndata.AnnData.obs.index (Default="")

    batch_key : str
        If len(batch_key) > 0, this str will be added as a value to a "batch"
        feature in the returned AnnData.obs Data.Frame (Default="")


    Returns
    -------
    anndata.AnnData
        An AnnData object with the DATA segment of the .fcs file saved to the X 
        attribute. 

    """
    try:
        tmp_fcs = FCSFileObject(fcs_file_path=fcs_file_path)
        tmp_var_df = pd.DataFrame({'name': tmp_fcs.named_par, 'USE_LOGICLE': [False if item in FREQUENT_LINEAR_CHANNELS else True for item in tmp_fcs.named_par_channel], 'LOGICLE_T': 3000000, 'LOGICLE_W': 0, 'LOGICLE_M': 3, 'LOGICLE_A': 1, 'LOGICLE_APPLIED': False, 'IMPUTED': False}, index=tmp_fcs.named_par_channel)
        tmp_obs_df = pd.DataFrame({'cell_number': list(range(tmp_fcs.data.shape[0]))}, index=np.array([f'{obs_prefix}:{str(i)}' for i in list(range(tmp_fcs.data.shape[0]))]))
        if len(batch_key) > 0:
            tmp_obs_df['batch'] = batch_key
        tmp_anndata = anndata.AnnData(tmp_fcs.data.astype(np.float32), obs=tmp_obs_df, var=tmp_var_df)
        if 'batch' in tmp_anndata.obs.columns.values:
            tmp_anndata.obs['batch'] = tmp_anndata.obs['batch'].astype(str)
        tmp_anndata.var['name'] = tmp_anndata.var['name'].astype(str)
        tmp_anndata.var['USE_LOGICLE'] = tmp_anndata.var['USE_LOGICLE'].astype(bool)
        tmp_anndata.var['LOGICLE_T'] = tmp_anndata.var['LOGICLE_T'].astype(np.float32)
        tmp_anndata.var['LOGICLE_W'] = tmp_anndata.var['LOGICLE_W'].astype(np.float32)
        tmp_anndata.var['LOGICLE_M'] = tmp_anndata.var['LOGICLE_M'].astype(np.float32)
        tmp_anndata.var['LOGICLE_A'] = tmp_anndata.var['LOGICLE_A'].astype(np.float32)
        tmp_anndata.var['LOGICLE_APPLIED'] = tmp_anndata.var['LOGICLE_APPLIED'].astype(bool)
        tmp_anndata.var['IMPUTED'] = tmp_anndata.var['IMPUTED'].astype(bool)
        return tmp_anndata
    except Exception as e:
        print(e)
        print('ERROR! Failed to open file {}.'.format(fcs_file_path))
        return None

def write_anndata_to_fcs(input_anndata, fcs_file_path, add_umap=False, verbosity=0):
    """
    Writes a given pyInfinityFlow structured AnnData object to an .fcs file
    according to the FCS3.1 file standard.

    Arguments
    ---------
    input_anndata : anndata.AnnData
        The pyInfinityFlow formatted AnnData object to save to an .fcs file 
        (Required)

    fcs_file_path : str
        The path to which the .fcs file should be written. (Required)
    
    add_umap : bool
        Specifies whether the 2D-UMAP coordinates should be written to the DATA
        segment of the .fcs file. This expects the features "umap-x" and 
        "umap-y" are in the input_anndata.obs.columns. (Default=False)

    verbosity : int (0|1|2|3)
        The level of verbosity with which to print debug statements.


    Returns
    -------
    None
        The file will be saved to fcs_file_path.

    """
    try:
        if sum(input_anndata.var['LOGICLE_APPLIED'].values) > 0:
            print('WARNING! Some features are logicle normalized.\n\tRun apply_inverse_logicle_to_anndata(input_anndata) to invert logicle normalization.')
        tmp_fcs = FCSFileObject(fcs_file_path=fcs_file_path, mode='w')
        tmp_df = anndata_to_df(input_anndata)
        tmp_channel_names = input_anndata.var['name'].values
        if add_umap:
            umap_names = ['umap-x', 'umap-y']
            tmp_df = pd.concat([tmp_df, input_anndata.obs[umap_names]], axis=1)
            tmp_channel_names = np.concatenate([tmp_channel_names, ['', '']])
        tmp_fcs.load_data_from_pd_df(tmp_df, input_channel_names=tmp_channel_names, additional_text_segment_values={'$CYT': 'Aurora'})
        tmp_fcs.to_fcs(fcs_file_path=fcs_file_path)
    except Exception as e:
        printv(verbosity, v3=str(e))
        print('Failed to write .fcs file.')

def apply_logicle_to_anndata(input_anndata, in_place=True):
    """
    Applies the Logicle transformation function to the given input_anndata
    object. 

    Note
    ----
        The T, W, M, and A parameters are specified in the input_anndata.var.

    Arguments
    ---------
    input_anndata : anndata.AnnData
        The pyInfinityFlow formatted AnnData object on which to carry out 
        Logicle normalization (Required)
    
    in_place : bool
        Specifies whether the function should act on the input_anndata in-place
        (Default=True)


    Returns
    -------
    anndata.AnnData or None
        The AnnData object with logicle normalization applied or None if 
        in_place=True

    """
    check_to_logicle = (input_anndata.var['USE_LOGICLE'] & ~input_anndata.var['LOGICLE_APPLIED']).values
    features_to_logicle = input_anndata.var.index.values[check_to_logicle]
    if len(features_to_logicle) == 0:
        print('WARNING! No features required logicle normalization at this time.')
        if in_place:
            return ()
        else:
            return input_anndata.copy()
    if not in_place:
        input_anndata = input_anndata.copy()
    try:
        input_anndata[:, features_to_logicle].X = anndata_to_df(input_anndata)[features_to_logicle].apply(lambda x: apply_logicle(x.values, T=input_anndata.var.loc[x.name, 'LOGICLE_T'], W=input_anndata.var.loc[x.name, 'LOGICLE_W'], M=input_anndata.var.loc[x.name, 'LOGICLE_M'], A=input_anndata.var.loc[x.name, 'LOGICLE_A']), axis=0).values
        input_anndata.var.loc[features_to_logicle, 'LOGICLE_APPLIED'] = True
    except Exception as e:
        print('Failed to apply logicle function correctly!')
        print(e)
    if in_place:
        return None
    else:
        return input_anndata
'\nCarry out inverting the logicle normalization on a pyInfinityFlow AnnData object.\n'

def apply_inverse_logicle_to_anndata(input_anndata, in_place=True):
    """
    Applies the inverse Logicle transformation function to the given 
    input_anndata object. 

    Arguments
    ---------
    input_anndata : anndata.AnnData
        The pyInfinityFlow formatted AnnData object on which to carry out 
        Logicle normalization (Required)
    
    in_place : bool
        Specifies whether the function should act on the input_anndata in-place
        (Default=True)


    Returns
    -------
    anndata.AnnData or None
        The AnnData object with logicle normalization applied or None if 
        in_place=True

    """
    check_to_invert_logicle = (input_anndata.var['USE_LOGICLE'] & input_anndata.var['LOGICLE_APPLIED']).values
    features_to_logicle = input_anndata.var.index.values[check_to_invert_logicle]
    if len(features_to_logicle) == 0:
        print('WARNING! No features required inverting logicle normalization at this time.')
        if in_place:
            return ()
        else:
            return input_anndata.copy()
    if not in_place:
        input_anndata = input_anndata.copy()
    try:
        input_anndata[:, features_to_logicle].X = anndata_to_df(input_anndata)[features_to_logicle].apply(lambda x: apply_inverse_logicle(x.values, T=input_anndata.var.loc[x.name, 'LOGICLE_T'], W=input_anndata.var.loc[x.name, 'LOGICLE_W'], M=input_anndata.var.loc[x.name, 'LOGICLE_M'], A=input_anndata.var.loc[x.name, 'LOGICLE_A']), axis=0).values
        input_anndata.var.loc[features_to_logicle, 'LOGICLE_APPLIED'] = False
    except Exception as e:
        print('Failed to apply inverse logicle function correctly!')
        print(e)
    if in_place:
        return ()
    else:
        return input_anndata

def move_features_to_silent(input_anndata, features):
    """
    This function will "silence" a set of feature values by moving them out of
    the AnnData.X array, and move them into a DataFrame stored in the
    AnnData.obsm["silent"] key. The DataFrame in AnnData.var corresponding to 
    the features is moved to the AnnData.uns["silent_var"] key. This is useful 
    when you want to keep some features out of the data for downstream analyses. 
    For example, the "Time" parameter stored in .fcs files is not meaningful to 
    cell state.

    Arguments
    ---------
    input_anndata: anndata.AnnData
        A pyInfinityFlow formatted AnnData object. (Required)

    features: list[str]
        The features (must be present in AnnData.var.index) to move to 'silent'.
        (Required)

    Returns
    -------
    anndata.AnnData
        A pyInfinityFlow formatted AnnData object. The 'silent' feature values
        are moved to AnnData.obsm["silent"], and the 'silent' feature var 
        DataFrame values are moved to AnnData.uns["silent_var"]

    """
    try:
        input_anndata = input_anndata.copy()
        tmp_varm = input_anndata.var.loc[features].copy()
        tmp_obsm = pd.DataFrame(input_anndata[:, features].X.toarray(), index=input_anndata.obs.index.values, columns=features)
        keep = np.setdiff1d(input_anndata.var.index.values, features)
        input_anndata = input_anndata[:, keep]
        if 'silent' in input_anndata.obsm:
            input_anndata.obsm['silent'] = pd.concat([input_anndata.obsm['silent'], tmp_obsm], axis=1)
        else:
            input_anndata.obsm['silent'] = tmp_obsm
        if 'silent_var' in input_anndata.uns:
            input_anndata.uns['silent_var'] = pd.concat([input_anndata.uns['silent_var'], tmp_varm])
        else:
            input_anndata.uns['silent_var'] = tmp_varm
        return input_anndata
    except Exception as e:
        print(str(e))
        raise ValueError('Failed to move features to silent obsm...')

def move_features_out_of_silent(input_anndata, features):
    """
    This function will move the features that were "silenced" by pyInfinityFlow.
    InfinityFlow_Utilities.move_features_to_silent back into the AnnData.X and
    AnnData.var values.
    
    It is required that AnnData.obsm["silent"] and AnnData.uns["silent_var"] 
    exist.

    Arguments
    ---------
    input_anndata: anndata.AnnData
        A pyInfinityFlow formatted AnnData object. (Required)

    features: list[str]
        The features (must be present in AnnData.var.index) to move out of 
        'silent'. (Required)

    Returns
    -------
    anndata.AnnData
        A pyInfinityFlow formatted AnnData object. The features values are moved
        out of silent and back into AnnData.X and AnnData.var.

    """
    input_anndata = input_anndata.copy()
    if 'silent' not in input_anndata.obsm:
        raise ValueError("'silent' not in input_anndata.obsm")
    if 'silent_var' not in input_anndata.uns:
        raise ValueError("'silent_var' not in input_anndata.uns")
    check_features = ~pd.Series(features).isin(input_anndata.obsm['silent'].columns.values)
    if sum(check_features) > 0:
        raise ValueError("The following features were not currently found in input_anndata.obsm['silent']: \n\t{}".format('\n\t'.join(np.array(features)[check_features.values])))
    try:
        new_X = np.concatenate([input_anndata.X, input_anndata.obsm['silent'][features].values], axis=1)
        new_var = pd.concat([input_anndata.var, input_anndata.uns['silent_var'].loc[features]])
        new_obsm = input_anndata.obsm
        new_obsm['silent'] = new_obsm['silent'].drop(labels=features, axis=1)
        new_uns = input_anndata.uns
        new_uns['silent_var'] = input_anndata.uns['silent_var'].drop(labels=features, axis=0)
        add_obsp = False
        if input_anndata.obsp is not None:
            add_obsp = True
            tmp_obsp = input_anndata.obsp
        if add_obsp:
            tmp_return = anndata.AnnData(X=new_X, obs=input_anndata.obs, var=new_var, obsm=new_obsm, uns=new_uns, filename=input_anndata.filename)
            tmp_return.obsp = tmp_obsp
            return tmp_return
        else:
            return anndata.AnnData(X=new_X, obs=input_anndata.obs, var=new_var, obsm=new_obsm, uns=new_uns, filename=input_anndata.filename)
    except Exception as e:
        print(str(e))
        raise ValueError('Failed to move features out of silent obsm...')

def make_pca_elbo_plot(sub_p_adata, output_paths):
    """
    This function will make a PCA elbo curve plot to show the variance explained
    by each principal component. Requires that scanpy.tl.pca has been run on the
    sub_p_adata object.

    Arguments
    ---------
    input_anndata: anndata.AnnData
        A pyInfinityFlow formatted AnnData object that has the sub_p_adata.uns
        ['pca']['variance'] attribute. (Required)

    output_paths: dict
        The output_paths dictionary created by the pyInfinityFlow.
        InfinityFlow_Utilities.setup_output_directories function (Required)

    Returns
    -------
    None

    """
    plt.close('all')
    plt.plot(list(range(1, sub_p_adata.uns['pca']['variance'].shape[0] + 1)), sub_p_adata.uns['pca']['variance'])
    plt.title('PC Elbo Plot')
    plt.ylabel('Explained Variance')
    plt.xlabel('PC')
    plt.savefig(os.path.join(output_paths['qc'], 'pc_elbo_plot.png'))

def check_infinity_flow_annotation_dataframes(backbone_annotation, infinity_marker_annotation, n_events_train=0, n_events_validate=0, n_events_combine=0, ratio_for_validation=0.2, separate_backbone_reference=None, random_state=None, input_fcs_dir=None, verbosity=0):
    """
    This function prepares the FileHandler object to control how the pipeline
    will handle each .fcs file for the indicated regression model. Both the 
    backbone_annotation table and the infinity_marker_annotation table are 
    checked for validity.

    Arguments
    ---------
    backbone_annotation: pandas.DataFrame 
        The first column is the backbone features as they appear in the channel 
        names of the fcs file for the reference data. The second column is the 
        channel names as they appear in the query file, which is used to build 
        the regression model. The last column is the final name to give to the 
        user defined channel parameter of fcs file. (Required)

    infinity_marker_annotation: pandas.DataFrame 
        The first column is the fcs file name. The second column is the channel 
        name in fcs file to use as the response variable in the regression model. 
        The third column is the desired name to give to the final channel in the 
        output. The fourth column, which is optional, is the name of the isotype  
        background control antibody as it appears in the third column.

    n_events_train: int 
        The number of events in each fcs file that should be considered

    n_events_validate: int
        The number of events to use to validate each regression model

    n_events_combine: int or None 
        If pooling events from each file to merge into a final dataset, this 
        variable specifies how many events from each file will be taken from 
        each file to combine into a final object to  use as the reference for 
        regression.

    ratio_for_validation: float from 0 to 1 
        If n_events_train and n_events_validate are set to 0, then all events 
        from the fcs file will be used and this parameter will specify what 
        ratio of the fcs events will be used for validation. The remainder will 
        be used for training.

    random_state: int 
        Integer to give for sampling indices from fcs file so that sampling 
        indices from fcs files can be reproduced.

    input_fcs_dir: str 
        The path to the directory that holds all of the fcs files in column 1 
        of the infinity_marker_annotation DataFrame
    
    exclusive_train_and_validate: bool 
        If true, the program will be forced to use separate events for training 
        and validation, n_events_combine will be taken from validation but 
        cannot be taken from training.

    verbosity: int (0|1|2|3) 
        Specifies to what verbosity level the function will output progress and 
        debugging statements.


    Returns
    -------
    pyInfinityFlow.InfinityFlow_Utilities.InfinityFlowFileHandler
        An instance of InfinityFlowFileHandler, which is an object to specify
        how input .fcs files should be treated during the regression pipeline.

    """
    if input_fcs_dir is None:
        raise ValueError('Must input an input_fcs_dir!')
    list_fcs_files = os.listdir(input_fcs_dir)
    if backbone_annotation.shape[1] != 3:
        raise ValueError('File reading error. The backbone_annotation_file should have 3 columns.')
    file_handler = InfinityFlowFileHandler(backbone_annotation.iloc[:, 0].values)
    if infinity_marker_annotation.shape[1] == 3:
        printv(verbosity, v1='Isotype controls will not be used...')
    elif infinity_marker_annotation.shape[1] == 4:
        file_handler.use_isotype_controls = True
        printv(verbosity, v1='Isotype controls detected. Will attempt to use background correction...')
        isotype_control_names = infinity_marker_annotation.iloc[:, 3].unique()
        isotype_control_names = isotype_control_names[isotype_control_names != '']
        printv(verbosity, v3='The following isotype controls will be used: \n\t{}\n\n'.format('\n\t'.join(isotype_control_names)))
        check_isotype_controls = ~pd.Series(isotype_control_names).isin(infinity_marker_annotation.iloc[:, 2].values)
        if sum(check_isotype_controls) > 0:
            raise ValueError('The following isotype controls do not have infinity_marker_annotation_file entries: \n\t{}'.format('\n\t'.join(isotype_control_names[check_isotype_controls])))
        file_handler.isotype_control_names = isotype_control_names
    else:
        raise ValueError('Error with infinity_marker_annotation_file. There should either be 3 (no Isotype background correction) or 4 columns (with Isotype background correction).')
    if backbone_annotation.shape[0] == 0:
        raise ValueError('File reading error. No values found in backbone_annotation_file.')
    if infinity_marker_annotation.shape[0] == 0:
        raise ValueError('File reading error. No values found in infinity_marker_annotation_file.')
    check_duplicates = infinity_marker_annotation.iloc[:, 2].duplicated().values
    if sum(check_duplicates) > 0:
        raise ValueError('InfinityMarker names must be unique. The following duplicate InfinityMarker names were found: \n\t{}\n\n'.format('\n\t'.join(infinity_marker_annotation.iloc[:, 2].values[check_duplicates])))
    check_input_fcs = ~infinity_marker_annotation.iloc[:, 0].isin(list_fcs_files).values
    if sum(check_input_fcs) > 0:
        raise ValueError("File reading error. Couldn't find the following .fcs files in the fcs_file_dir: \n\t{}".format('\n\t'.join(infinity_marker_annotation.iloc[:, 0].values[check_input_fcs])))
    if separate_backbone_reference is not None:
        printv(verbosity, v3='Checking separate backbone reference fcs file for necessary backbone channels...')
        tmp_fcs = FCSFileObject(fcs_file_path=separate_backbone_reference, mode='r', read_data_segment=False)
        tmp_check_backbone = ~backbone_annotation.iloc[:, 0].isin(tmp_fcs.named_par_channel).values
        if sum(tmp_check_backbone) > 0:
            raise ValueError('The following backbone channels were not detected in input file {}:\n\t{}'.format(separate_backbone_reference, '\n\t'.join(backbone_annotation.iloc[:, 0].values[tmp_check_backbone])))
    printv(verbosity, v3='Streaming through .fcs files to specify events for training, validation, and prediction...')
    for (i, tmp_file) in enumerate(infinity_marker_annotation.iloc[:, 0].values):
        try:
            tmp_fcs = FCSFileObject(fcs_file_path=os.path.join(input_fcs_dir, tmp_file), mode='r', read_data_segment=False)
            tmp_fcs_n_cells = int(tmp_fcs.text_segment_values['$TOT'])
            tmp_check_backbone = ~backbone_annotation.iloc[:, 1].isin(tmp_fcs.named_par_channel).values
            if sum(tmp_check_backbone) > 0:
                raise ValueError('The following backbone channels were not detected in input file {}:\n\t{}'.format(tmp_file, '\n\t'.join(backbone_annotation.iloc[:, 1].values[tmp_check_backbone])))
            if n_events_combine is not None:
                tmp_check_backbone = ~backbone_annotation.iloc[:, 0].isin(tmp_fcs.named_par_channel).values
                if sum(tmp_check_backbone) > 0:
                    raise ValueError('The following backbone channels were not detected in input file {}:\n\t{}'.format(tmp_file, '\n\t'.join(backbone_annotation.iloc[:, 0].values[tmp_check_backbone])))
            if n_events_train == 0:
                if n_events_validate == 0:
                    if ratio_for_validation <= 0 or ratio_for_validation >= 1:
                        raise ValueError('\tratio_for_validation must be between 0 and 1.')
                    tmp_n_events_validate = math.floor(tmp_fcs_n_cells * ratio_for_validation)
                    tmp_n_events_train = tmp_fcs_n_cells - tmp_n_events_validate
                else:
                    tmp_n_events_validate = n_events_validate
                    tmp_n_events_train = tmp_fcs_n_cells - n_events_validate
                    if tmp_n_events_train <= 0:
                        raise ValueError(f'Could not get enough events for training. {tmp_n_events_validate} events were asked to be used for validation, but the file only has {tmp_fcs_n_cells} events.')
            else:
                tmp_n_events_train = n_events_train
                if n_events_validate == 0:
                    tmp_n_events_validate = tmp_fcs_n_cells - tmp_n_events_train
                    if tmp_n_events_validate <= 0:
                        raise ValueError(f'Could not get enough events for validation. {tmp_n_events_train} events were asked to be used for training, but the file only has {tmp_fcs_n_cells} events.')
                else:
                    tmp_n_events_validate = n_events_validate
                    if tmp_n_events_train + tmp_n_events_validate > tmp_fcs_n_cells:
                        raise ValueError(f'Could not use {tmp_n_events_train} events for training and {tmp_n_events_validate} events for validation when the file only has {tmp_fcs_n_cells} events.')
            if n_events_combine == 0:
                tmp_n_events_combine = tmp_n_events_validate
            elif n_events_combine is None:
                tmp_n_events_combine = None
            elif n_events_combine <= tmp_n_events_validate:
                tmp_n_events_combine = n_events_combine
            else:
                raise ValueError(f'Invalid entry for n_events_combine: {n_events_combine}\n\tThere are {tmp_fcs_n_cells} events in the file, and {tmp_n_events_validate} events are being used for validation. \n\tn_events_combine must be less than or equal to n_events_validate.')
            printv(verbosity, v3=f'Input file {tmp_file} was found to have {tmp_fcs_n_cells} events')
            printv(verbosity, v3=f'\t{tmp_n_events_train} events will be used for training...')
            printv(verbosity, v3=f'\t{tmp_n_events_validate} events will be used for validation...')
            if n_events_combine is not None:
                printv(verbosity, v3=f'\t{tmp_n_events_combine} events will be taken to combine into the final reference object...')
            tmp_indices = pd.Series(list(range(tmp_fcs_n_cells)))
            tmp_train_indices = tmp_indices.sample(tmp_n_events_train, random_state=random_state).sort_values().values
            tmp_indices_remaining = pd.Series(np.setdiff1d(tmp_indices.values, tmp_train_indices))
            tmp_test_indices = tmp_indices_remaining.sample(tmp_n_events_validate, random_state=random_state).sort_values().values
            if n_events_combine is not None:
                if random_state is None:
                    tmp_random_state = None
                else:
                    tmp_random_state = random_state + 1
                tmp_combine_indices = tmp_indices_remaining.sample(tmp_n_events_combine, random_state=tmp_random_state).sort_values().values
            else:
                tmp_combine_indices = None
            file_handler.add_handle(name=infinity_marker_annotation.iloc[i, 2], file_name=tmp_file, directory=input_fcs_dir, reference_backbone_channels=backbone_annotation.iloc[:, 0].values, backbone_channels=backbone_annotation.iloc[:, 1].values, prediction_channel=infinity_marker_annotation.iloc[i, 1], train_indices=tmp_train_indices, test_indices=tmp_test_indices, pool_indices=tmp_combine_indices)
        except Exception as e:
            printv(verbosity, v3=str(e))
            raise ValueError('File reading error. Could not set up FileHandler for  file {}.'.format(tmp_file))
    printv(verbosity, prefix_debug=False, v3='\n\n')
    return file_handler

def setup_output_directories(output_dir, file_handler, verbosity=0):
    """
    Set up the output directories for the InfinityFlow Regression workflow

    Arguments
    ---------
    output_dir: str
        The directory to which the pipeline outputs should be saved. (Required)

    file_handler: pyInfinityFlow.InfinityFlow_Utilities.InfinityFlowFileHandler
        The InfinityFlowFileHandler that is returned by pyInfinityFlow.
        InfinityFlow_Utilities.check_infinity_flow_annotation_dataframes.

    verbosity: int (0|1|2|3) 
        Specifies to what verbosity level the function will output progress and 
        debugging statements.


    Returns
    -------
    dict
        A dictionary that stores the output directories as strings:
            - ["output_regression_path"]
            - ["output_umap_feature_plot_path"]
            - ["clustering"]
            - ["qc"]
            - ["output_umap_bc_feature_plot_path"]

        The function will check if each of the output directory paths can be
        created and make them if they don't exist.

    """
    if not os.path.isdir(output_dir):
        try:
            os.mkdir(output_dir)
        except Exception as e:
            printv(verbosity, v3=str(e))
            raise ValueError('Failed to make output directory: \n\t\t{}'.format())
    output_paths = {'output_regression_path': os.path.join(output_dir, 'regression_results'), 'output_umap_feature_plot_path': os.path.join(output_dir, 'umap_feature_plots'), 'clustering': os.path.join(output_dir, 'clustering'), 'qc': os.path.join(output_dir, 'QC')}
    if file_handler.use_isotype_controls:
        output_paths['output_umap_bc_feature_plot_path'] = os.path.join(output_dir, 'umap_feature_plots_background_corrected')
    try:
        for tmp_item in output_paths.items():
            if not os.path.isdir(tmp_item[1]):
                os.mkdir(tmp_item[1])
    except Exception as e:
        printv(verbosity, v3=str(e))
        raise ValueError('Failed to create the necessary output directories. Check the validity of the output_dir.')
    return output_paths

def single_chunk_training(file_handler, cores_to_use=1, random_state=None, xgb_params={}, use_logicle_scaling=True, normalization_method=None, verbosity=0):
    """
    This function carries out fitting of XGBoost regression models. It will 
    read the data using the file_handler object to specify which events will be
    used for fitting. It will then carry out optional Logicle data normalization
    and batch normalization before fitting the model. It will then save the
    settings of the XGBoost regression models to the output.

    Arguments
    ---------
    file_handler: pyInfinityFlow.InfinityFlow_Utilities.InfinityFlowFileHandler
        The InfinityFlowFileHandler that is returned by pyInfinityFlow.
        InfinityFlow_Utilities.check_infinity_flow_annotation_dataframes.

    cores_to_use: int
        The number of cores to use for XGBoost model fitting. (Default=1)

    random_state: int or None
        Integer to specify the random state for XGBoost model fitting in an 
        attempt to make the regression more reproducible, or None to not use 
        a random seed. (Default=None)

    xgb_params: dict
        Dictionary of keyword-argument value pairs to pass to the XGBoost model
        instantiation. (Default={})

    use_logicle_scaling: bool
        Whether or not to use Logicle scaling before model fitting. 
        (Default=True)

    normalization_method: None or "zscore"
        The method for normalizing the backbone of different samples in an 
        attempt to remove batch effects. (Default=None)

    verbosity: int (0|1|2|3) 
        Specifies to what verbosity level the function will output progress and 
        debugging statements. (Default=0)


    Returns
    -------
    tuple (CombinedRegressionModels, timings_dict)
        pyInfinityFlow.InfinityFlow_Utilities.CombinedRegressionModels
            An object to track the state of XGBoost Regression models as well 
            as the models themselves.

        timings_dict
            A dictionary that saves how much time each step of function takes.

    """
    t_start_file_read_1 = time.time()
    printv(verbosity, v1='Reading in data from .fcs files for model training...')
    ordered_markers = file_handler.list_infinity_markers
    ordered_files = [file_handler.handles[marker]['file_name'] for marker in ordered_markers]
    for (i, marker) in enumerate(ordered_markers):
        printv(verbosity, v3=f'\t\tReading in the data for InfinityMarker {marker}...')
        tmp_path = os.path.join(file_handler.handles[marker]['directory'], file_handler.handles[marker]['file_name'])
        tmp_indices = file_handler.handles[marker]['train_indices']
        tmp_anndata = read_fcs_into_anndata(fcs_file_path=tmp_path, obs_prefix=f'F{i}', batch_key=marker)
        tmp_anndata = tmp_anndata[tmp_anndata.obs.index.values[tmp_indices], :]
        if i == 0:
            sub_t_adata = tmp_anndata
        else:
            sub_t_adata = anndata.concat([sub_t_adata, tmp_anndata], merge='same')
    sub_t_adata.uns['obs_file_origin'] = pd.DataFrame({'file': ordered_files, 'InfinityMarker': ordered_markers}, index=[f'F{i}' for i in range(len(ordered_markers))])
    t_end_file_read_1 = time.time()
    t_start_logicle_1 = time.time()
    if use_logicle_scaling:
        printv(verbosity, v1='Applying Logicle normalization to data...')
        apply_logicle_to_anndata(sub_t_adata)
    t_end_logicle_1 = time.time()
    t_start_zscore_1 = time.time()
    if normalization_method == 'zscore':
        for (i, infinity_marker) in enumerate(ordered_markers):
            tmp_indices = sub_t_adata.obs.loc[sub_t_adata.obs['batch'] == infinity_marker].index.values
            tmp_backbone = file_handler.handles[infinity_marker]['backbone_channels']
            sub_t_adata[tmp_indices, tmp_backbone].X = zscore(sub_t_adata[tmp_indices, tmp_backbone].X.toarray())
    t_end_zscore_1 = time.time()
    t_start_fit_model = time.time()
    output_models = {}
    infinity_parameter_annotations = {}
    infinity_channels = {}
    ordered_training_channels = file_handler.handles[file_handler.list_infinity_markers[0]]['backbone_channels']
    for infinity_marker in ordered_markers:
        try:
            printv(verbosity, v2='\tBuilding regression model for {}...'.format(infinity_marker))
            tmp_indices = sub_t_adata.obs.loc[sub_t_adata.obs['batch'] == infinity_marker].index.values
            tmp_response_channel = file_handler.handles[infinity_marker]['prediction_channel']
            t_model_start = time.time()
            printv(verbosity, v3=f'Setting n_jobs to {cores_to_use} and random_state to {random_state}')
            tmp_model = xgboost.XGBRegressor(n_jobs=cores_to_use, random_state=random_state, **xgb_params)
            tmp_model.fit(sub_t_adata[tmp_indices, file_handler.handles[infinity_marker]['backbone_channels']].X.toarray(), sub_t_adata[tmp_indices, tmp_response_channel].X)
            t_model_end = time.time()
            printv(verbosity, v3='\t\tXGBoost regression model trained in {:.2f} seconds.\n'.format(t_model_end - t_model_start))
            output_models[infinity_marker] = tmp_model
            infinity_parameter_annotations[infinity_marker] = sub_t_adata.var.loc[tmp_response_channel].copy()
            infinity_channels[infinity_marker] = tmp_response_channel
        except Exception as e:
            printv(verbosity, v3=str(e))
            raise ValueError(f'Failed to build regression model for InfinityMarker {infinity_marker}.')
    regression_models = CombinedRegressionModels(ordered_training_channels=ordered_training_channels, var_annotations=sub_t_adata.var, infinity_markers=ordered_markers, regression_models=output_models, parameter_annotations=infinity_parameter_annotations, infinity_channels=infinity_channels)
    t_end_fit_model = time.time()
    tmp_timings = {'file_read_1': t_end_file_read_1 - t_start_file_read_1, 'logicle_1': t_end_logicle_1 - t_start_logicle_1, 'zscore_1': t_end_zscore_1 - t_start_zscore_1, 'fit_model': t_end_fit_model - t_start_fit_model}
    return (regression_models, tmp_timings)

def single_chunk_testing(file_handler, regression_models, use_logicle_scaling=True, normalization_method=None, verbosity=0):
    """
    This function carries out validation of XGBoost regression models. It will 
    read the data using the file_handler object to specify which events will be
    used for validation. It will then predict the InfinityMarker signal on held
    out data from its .fcs file. Then it will save metrics to the 
    regression_models object and return it, along with a dictionary to track
    timings for steps of the function.

    Arguments
    ---------
    file_handler: pyInfinityFlow.InfinityFlow_Utilities.InfinityFlowFileHandler
        The InfinityFlowFileHandler that is returned by pyInfinityFlow.
        InfinityFlow_Utilities.check_infinity_flow_annotation_dataframes. 
        (Required)

    regression_models: pyInfinityFlow.InfinityFlow_Utilities.CombinedRegressionModels
        The CombinedRegressionModels that is returned by pyInfinityFlow.
        InfinityFlow_Utilities.single_chunk_training function. (Required)

    use_logicle_scaling: bool
        Whether or not to use Logicle scaling before model fitting. 
        (Default=True)

    normalization_method: None or "zscore"
        The method for normalizing the backbone of different samples in an 
        attempt to remove batch effects. (Default=None)

    verbosity: int (0|1|2|3) 
        Specifies to what verbosity level the function will output progress and 
        debugging statements. (Default=0)


    Returns
    -------
    tuple (CombinedRegressionModels, timings_dict)
        pyInfinityFlow.InfinityFlow_Utilities.CombinedRegressionModels
            An object to track the state of XGBoost Regression models as well 
            as the models themselves. The .validation_metrics attribute will be
            filled with a dictionary that provides the following validation
            data:
                - ["pred"] - predicted values
                - ["true"] - real values
                - ["r2_score"] - r2_score provided by sklearn.metrics.r2_score
                - ["mean_squared_error"] - provided by sklearn.metrics.mean_squared_error

        timings_dict
            A dictionary that saves how much time each step of function takes.

    """
    ordered_markers = file_handler.list_infinity_markers
    ordered_files = [file_handler.handles[marker]['file_name'] for marker in ordered_markers]
    t_start_file_read_2 = time.time()
    printv(verbosity, v1='Reading in data from .fcs files for model validation...')
    for (i, marker) in enumerate(ordered_markers):
        printv(verbosity, v3=f'\t\tReading in the data for InfinityMarker {marker}...')
        tmp_path = os.path.join(file_handler.handles[marker]['directory'], file_handler.handles[marker]['file_name'])
        tmp_indices = file_handler.handles[marker]['test_indices']
        tmp_anndata = read_fcs_into_anndata(fcs_file_path=tmp_path, obs_prefix=f'F{i}', batch_key=marker)
        tmp_anndata = tmp_anndata[tmp_anndata.obs.index.values[tmp_indices], :]
        if i == 0:
            sub_v_adata = tmp_anndata
        else:
            sub_v_adata = anndata.concat([sub_v_adata, tmp_anndata], merge='same')
    t_end_file_read_2 = time.time()
    sub_v_adata.uns['obs_file_origin'] = pd.DataFrame({'file': ordered_files, 'InfinityMarker': ordered_markers}, index=[f'F{i}' for i in range(len(ordered_markers))])
    t_start_logicle_2 = time.time()
    if use_logicle_scaling:
        printv(verbosity, v1='Applying Logicle normalization to data...')
        try:
            tmp_anno = regression_models.var_annotations
            tmp_logicle_features = ['USE_LOGICLE', 'LOGICLE_T', 'LOGICLE_W', 'LOGICLE_M', 'LOGICLE_A']
            sub_v_adata.var.loc[tmp_anno.index.values, tmp_logicle_features] = tmp_anno[tmp_logicle_features]
        except Exception as e:
            printv(verbosity, v3=str(e))
            raise ValueError('Could not apply var annotation from training dataset to validation dataset.\n\t(see above Exception for details...)\n\n')
    apply_logicle_to_anndata(sub_v_adata)
    t_end_logicle_2 = time.time()
    t_start_zscore_2 = time.time()
    if normalization_method == 'zscore':
        for (i, infinity_marker) in enumerate(ordered_markers):
            tmp_indices = sub_v_adata.obs.loc[sub_v_adata.obs['batch'] == infinity_marker].index.values
            tmp_backbone = file_handler.handles[infinity_marker]['backbone_channels']
            sub_v_adata[tmp_indices, tmp_backbone].X = zscore(sub_v_adata[tmp_indices, tmp_backbone].X.toarray())
    t_end_zscore_2 = time.time()
    t_start_validation = time.time()
    printv(verbosity, v1='Obtaining validation metrics for regression models...')
    tmp_channels = regression_models.ordered_training_channels
    for infinity_marker in ordered_markers:
        printv(verbosity, v1='\t\tWorking on {}...'.format(infinity_marker))
        out_v_metrics = {}
        tmp_model = regression_models.regression_models[infinity_marker]
        tmp_target_channel = regression_models.infinity_channels[infinity_marker]
        tmp_indices = sub_v_adata.obs.loc[sub_v_adata.obs['batch'] == infinity_marker].index.values
        tmp_predictions = tmp_model.predict(sub_v_adata[tmp_indices, tmp_channels].X.toarray())
        tmp_true = sub_v_adata[tmp_indices, tmp_target_channel].X.toarray().reshape(-1)
        out_v_metrics['pred'] = tmp_predictions
        out_v_metrics['true'] = tmp_true
        out_v_metrics['r2_score'] = r2_score(tmp_true, tmp_predictions)
        out_v_metrics['mean_squared_error'] = mean_squared_error(tmp_true, tmp_predictions)
        regression_models.validation_metrics[infinity_marker] = out_v_metrics
    t_end_validation = time.time()
    tmp_timings = {'file_read_2': t_end_file_read_2 - t_start_file_read_2, 'logicle_2': t_end_logicle_2 - t_start_logicle_2, 'zscore_2': t_end_zscore_2 - t_start_zscore_2, 'validation': t_end_validation - t_start_validation}
    return (regression_models, tmp_timings)

def make_flow_regression_predictions(file_handler, regression_models, separate_backbone_reference=None, use_logicle_scaling=True, normalization_method=None, verbosity=0):
    """
    This function carries out prediction using XGBoost regression models. It will
    use either a separate_backbone_reference .fcs file onto which to make 
    predictions of the InfinityMarker signals, or it will use a subset of the
    validation cells from the InfinityMarker .fcs files themselves. The output
    will be an AnnData object containing the backbone features and the predicted
    signals from the InfinityMarker regression models. 

    Arguments
    ---------
    file_handler: pyInfinityFlow.InfinityFlow_Utilities.InfinityFlowFileHandler
        The InfinityFlowFileHandler that is returned by pyInfinityFlow.
        InfinityFlow_Utilities.check_infinity_flow_annotation_dataframes. 
        (Required)

    regression_models: pyInfinityFlow.InfinityFlow_Utilities.CombinedRegressionModels
        The CombinedRegressionModels that is returned by pyInfinityFlow.
        InfinityFlow_Utilities.single_chunk_training function. (Required)

    separate_backbone_reference: str or None
        If not None, this defines the path to the .fcs file onto which to make 
        predictions for the InfinityMarker signals. 

    use_logicle_scaling: bool
        Whether or not to use Logicle scaling before model fitting. 
        (Default=True)

    normalization_method: None or "zscore"
        The method for normalizing the backbone of different samples in an 
        attempt to remove batch effects. (Default=None)

    verbosity: int (0|1|2|3) 
        Specifies to what verbosity level the function will output progress and 
        debugging statements. (Default=0)


    Returns
    -------
    tuple (AnnData, timings_dict)
        AnnData
            A pyInfinityFlow formatted AnnData object with the original parameter
            values as well as the imputed InfinityMarker values.

        timings_dict
            A dictionary that saves how much time each step of function takes.

    """
    ordered_markers = file_handler.list_infinity_markers
    ordered_files = [file_handler.handles[marker]['file_name'] for marker in ordered_markers]
    t_start_file_read_3 = time.time()
    if separate_backbone_reference is not None:
        printv(verbosity, v1='Reading in data from separate_backbone_reference .fcs file for final Infinity Flow object...')
        sub_p_adata = read_fcs_into_anndata(fcs_file_path=separate_backbone_reference, obs_prefix=f'Ref_', batch_key='Ref')
    else:
        printv(verbosity, v1='Reading in data from .fcs files for pooling into final InfinityFlow object...')
        for (i, marker) in enumerate(ordered_markers):
            printv(verbosity, v3=f'\t\tReading in the data for InfinityMarker {marker}...')
            tmp_path = os.path.join(file_handler.handles[marker]['directory'], file_handler.handles[marker]['file_name'])
            tmp_indices = file_handler.handles[marker]['pool_indices']
            tmp_anndata = read_fcs_into_anndata(fcs_file_path=tmp_path, obs_prefix=f'F{i}', batch_key=marker)
            tmp_anndata = tmp_anndata[tmp_anndata.obs.index.values[tmp_indices], :]
            if i == 0:
                sub_p_adata = tmp_anndata
            else:
                sub_p_adata = anndata.concat([sub_p_adata, tmp_anndata], merge='same')
        sub_p_adata.uns['obs_file_origin'] = pd.DataFrame({'file': ordered_files, 'InfinityMarker': ordered_markers}, index=[f'F{i}' for i in range(len(ordered_markers))])
    t_end_file_read_3 = time.time()
    ordered_backbone_channels = file_handler.ordered_reference_backbone
    t_start_logicle_3 = time.time()
    if use_logicle_scaling:
        printv(verbosity, v1='Applying Logicle normalization to data...')
        try:
            tmp_anno = regression_models.var_annotations
            tmp_logicle_features = ['USE_LOGICLE', 'LOGICLE_T', 'LOGICLE_W', 'LOGICLE_M', 'LOGICLE_A']
            sub_p_adata.var.loc[ordered_backbone_channels, tmp_logicle_features] = tmp_anno.loc[ordered_backbone_channels, tmp_logicle_features]
        except Exception as e:
            printv(verbosity, v3=str(e))
            raise ValueError('Could not apply var annotation from training dataset to pooling dataset.\n\t(see above Exception for details...)\n\n')
        apply_logicle_to_anndata(sub_p_adata)
    t_end_logicle_3 = time.time()
    raw_sub_p_adata = sub_p_adata.copy()
    t_start_zscore_3 = time.time()
    if normalization_method == 'zscore':
        if separate_backbone_reference is None:
            for (i, infinity_marker) in enumerate(ordered_markers):
                tmp_indices = sub_p_adata.obs.loc[sub_p_adata.obs['batch'] == infinity_marker].index.values
                sub_p_adata[tmp_indices, ordered_backbone_channels].X = zscore(sub_p_adata[tmp_indices, ordered_backbone_channels].X.toarray())
        else:
            sub_p_adata[:, ordered_backbone_channels].X = zscore(sub_p_adata[:, ordered_backbone_channels].X.toarray())
    t_end_zscore_3 = time.time()
    printv(verbosity, prefix_debug=False, v1='Making predictions for final InfinityFlow object...')
    t_start_predictions = time.time()
    predicted_data = []
    predicted_var = pd.concat(regression_models.parameter_annotations, axis=1).T.loc[ordered_markers]
    predicted_var.loc[:, 'IMPUTED'] = True
    predicted_var.loc[:, 'name'] = ['InfinityMarker_{}'.format(item) for item in predicted_var.index.values]
    saved_uns = sub_p_adata.uns.copy()
    for infinity_marker in ordered_markers:
        printv(verbosity, v1='\t\tWorking on {}...'.format(infinity_marker))
        tmp_model = regression_models.regression_models[infinity_marker]
        predicted_data.append(tmp_model.predict(sub_p_adata[:, ordered_backbone_channels].X.toarray()))
    sub_p_adata = anndata.AnnData(np.concatenate([raw_sub_p_adata.X, np.array(predicted_data).T], axis=1), obs=sub_p_adata.obs, var=pd.concat([raw_sub_p_adata.var, predicted_var]), uns=saved_uns)
    sub_p_adata.var['USE_LOGICLE'] = sub_p_adata.var['USE_LOGICLE'].astype(bool)
    sub_p_adata.var['LOGICLE_T'] = sub_p_adata.var['LOGICLE_T'].astype(np.float32)
    sub_p_adata.var['LOGICLE_W'] = sub_p_adata.var['LOGICLE_W'].astype(np.float32)
    sub_p_adata.var['LOGICLE_M'] = sub_p_adata.var['LOGICLE_M'].astype(np.float32)
    sub_p_adata.var['LOGICLE_A'] = sub_p_adata.var['LOGICLE_A'].astype(np.float32)
    sub_p_adata.var['LOGICLE_APPLIED'] = sub_p_adata.var['LOGICLE_APPLIED'].astype(bool)
    sub_p_adata.var['IMPUTED'] = sub_p_adata.var['IMPUTED'].astype(bool)
    t_end_predictions = time.time()
    tmp_timings = {'file_read_3': t_end_file_read_3 - t_start_file_read_3, 'logicle_3': t_end_logicle_3 - t_start_logicle_3, 'zscore_3': t_end_zscore_3 - t_start_zscore_3, 'predictions': t_end_predictions - t_start_predictions}
    return (sub_p_adata, tmp_timings)

def perform_background_correction(sub_p_adata, file_handler, infinity_marker_annotation, cores_to_use=1, verbosity=0):
    """
    This function carries out background correction on the signal of a given
    InfinityMarker if that InfinityMarker has a corresponding Isotype
    InfinityMarker. A linear model is applied to regress-out the background
    antibody binding from the theoretical true signal of the InfinityMarker.

    Arguments
    ---------
    sub_p_adata: anndata.AnnData
        A pyInfinityFlow formatted AnnData object with the original parameter
        values as well as the imputed InfinityMarker values. The Isotype 
        controls must be included as InfinityMarkers and annotated in the 
        infinity_marker_annotation DataFrame. (Required)

    file_handler: pyInfinityFlow.InfinityFlow_Utilities.InfinityFlowFileHandler
        The InfinityFlowFileHandler that is returned by pyInfinityFlow.
        InfinityFlow_Utilities.check_infinity_flow_annotation_dataframes. 
        (Required)

    infinity_marker_annotation: pandas.DataFrame
        The annotation DataFrame that specifies the File, Channel to predict, 
        Name of final InfinityMarker, and Isotype InfinityMarker Name for each 
        InfinityMarker. This DataFrame must have 4 columns if background 
        correction is to be done. Each of the values in the last column (Isotype) 
        must be present in the third column (Name of InfinityMarker) as 
        InfinityMarkers. (Required)

    cores_to_use: int
        The number of cores to use for fitting the sklearn.linear_model.
        LinearRegression model. (Default=1)

    verbosity: int (0|1|2|3) 
        Specifies to what verbosity level the function will output progress and 
        debugging statements. (Default=0)


    Returns
    -------
    tuple (background_corrected_data, background_corrected_var, timings_dict)
        background_corrected_data
            A DataFrame specifying the background corrected data, with event 
            names as the index and channel names as columns.

        background_corrected_var
            A DataFrame of the .var field that corresponds to the features in 
            the background_corrected_data.

        timings_dict
            A dictionary that saves how much time each step of function takes.

    """
    background_corrected_data = {}
    t_start_bg_correction = time.time()
    final_features = np.setdiff1d(infinity_marker_annotation.iloc[:, 2].values, file_handler.isotype_control_names)
    tmp_indices = infinity_marker_annotation.iloc[:, 2].isin(final_features).values
    f_to_iso = pd.Series(infinity_marker_annotation.iloc[:, 3].values[tmp_indices], index=infinity_marker_annotation.iloc[:, 2].values[tmp_indices])
    for (infinity_marker, iso) in f_to_iso.items():
        printv(verbosity, v3=f'Feature {infinity_marker} will use isotype {iso}...')
        tmp_x = sub_p_adata[:, iso].X.toarray().reshape(-1)
        tmp_y = sub_p_adata[:, infinity_marker].X.toarray().reshape(-1)
        lm = LinearRegression(n_jobs=cores_to_use)
        lm.fit(tmp_x.reshape(-1, 1), tmp_y)
        (slope, intercept) = (lm.coef_[0], lm.intercept_)
        tmp_bc_vector = (-slope * tmp_x + tmp_y - intercept) / np.sqrt(slope ** 2 + 1)
        background_corrected_data[infinity_marker] = tmp_bc_vector - min(tmp_bc_vector)
    background_corrected_data = pd.DataFrame(background_corrected_data)
    background_corrected_var = sub_p_adata.var.loc[background_corrected_data.columns.values].copy()
    t_end_bg_correction = time.time()
    tmp_timings = {'background_correction': t_end_bg_correction - t_start_bg_correction}
    return (background_corrected_data, background_corrected_var, tmp_timings)

def find_markers_from_anndata(sub_p_adata, output_paths, groups_to_colors, cluster_key='leiden', verbosity=0):
    """
    Attempts to associate each of the clusters present in the AnnData 
    object with the Backbone and InfinityMarkers in the dataset. It applies 
    MarkerFinder to these clusters, generates a marker table, and plots a 
    heatmap with the clustered events as columns and Markers as rows.

    Arguments
    ---------
    sub_p_adata: anndata.AnnData
        A pyInfinityFlow formatted AnnData object with the original parameter
        values as well as the imputed InfinityMarker values. Clusters must be 
        defined in the sub_p_adata.obs DataFrame. (Required)

    output_paths: dict
        The output_paths dictionary created by the pyInfinityFlow.
        InfinityFlow_Utilities.setup_output_directories function (Required)

    groups_to_colors: dict
        Dictionary to specify what color should be used for each cluster in 
        sub_p_adata.obs[cluster_key]. (Eg. {'c1':'red', 'c2': 'blue', ...}) 
        (Required)

    cluster_key: str
        The key in sub_p_adata.obs to use for cluster assignments. By default, 
        it will look for "leiden". (Default="leiden")

    verbosity: int (0|1|2|3) 
        Specifies to what verbosity level the function will output progress and 
        debugging statements. (Default=0)


    Returns
    -------
    tuple (markers_df, cell_assignments)
        markers_df
            A DataFrame of which cluster for which each feature is a best marker
            by Pearson correlation using MarkerFinder. The columns of the 
            DataFrame will be ["marker", "top_cluster", "pearson_r", "p_value"]

        cell_assignments
            A DataFrame specifying the top 50 (or fewer if the cluster is 
            smaller) events that correspond to each cluster, ranked by Pearson 
            correlation of each event to its clusters centroid.
            Contains the following features:
                - ["cell"] - the event name
                - ["top_cluster"] - the cluster to which the event best correlates
                - ["top_corr"] - the Pearson correlation coefficient
                - ["original"] - the original cluster identity provided

    """
    try:
        printv(verbosity, prefix_debug=False, v1='Finding markers for Infinity Flow object...')
        groups = sub_p_adata.obs[cluster_key].astype(str).values
        centroids = calculate_centroids(input_df=anndata_to_df(sub_p_adata, use_raw_feature_names=False), groups=groups)
        Z = linkage(centroids, 'ward')
        cluster_order = np.array([int(item) for item in dendrogram(Z)['ivl']])
        cluster_order = pd.Series(list(range(centroids.shape[0])), index=centroids.index.values[cluster_order])
        markers_df = marker_finder(input_df=anndata_to_df(sub_p_adata, use_raw_feature_names=False), groups=groups)
        markers_df['sort_cluster'] = [cluster_order[item] for item in markers_df['top_cluster'].values]
        markers_df = markers_df.sort_values(by=['sort_cluster', 'pearson_r'], ascending=[True, False]).drop('sort_cluster', axis=1)
        markers_df.to_csv(os.path.join(output_paths['clustering'], 'cluster_markers.csv'), header=True, index=True, index_label='UID')
        printv(verbosity, prefix_debug=False, v1='Plotting markers...')
        r_cells_to_centroids = pearson_corr_df_to_df(anndata_to_df(sub_p_adata, use_raw_feature_names=False).T, centroids.T)
        tmp_top_cluster = r_cells_to_centroids.idxmax(axis=1)
        cell_assignments = pd.DataFrame({'cell': r_cells_to_centroids.index.values, 'top_cluster': tmp_top_cluster, 'sort_order': [cluster_order[item] for item in tmp_top_cluster.values], 'top_corr': r_cells_to_centroids.max(axis=1), 'original': groups}).sort_values(by=['sort_order', 'top_corr'], ascending=[True, False]).drop('sort_order', axis=1)
        cell_assignments = cell_assignments.loc[cell_assignments['top_cluster'] == cell_assignments['original']]
        unique_clusters = cell_assignments['top_cluster'].unique()
        sampled_indices = []
        for tmp_cluster in unique_clusters:
            seg_cells = cell_assignments.loc[cell_assignments['top_cluster'] == tmp_cluster]['cell']
            if len(seg_cells) < 50:
                sampled_indices += list(seg_cells.values)
            else:
                sampled_indices += list(seg_cells.iloc[:50].values)
        cell_assignments = cell_assignments.loc[cell_assignments['cell'].isin(sampled_indices)]
        plot_markers_df(input_df=anndata_to_df(sub_p_adata, use_raw_feature_names=False), ordered_markers_df=markers_df, ordered_cells_df=cell_assignments, groups_to_colors=pd.Series(groups_to_colors), path_to_save_figure=os.path.join(output_paths['clustering'], 'cluster_markers.pdf'))
        return (markers_df, cell_assignments)
    except Exception as e:
        printv(verbosity=verbosity, v3=str(e))
        raise ValueError('Failed to run find_markers_from_anndata.')

def save_umap_figures_all_features(sub_p_adata, file_handler, output_paths, background_corrected_data=None, verbosity=0):
    """
    Plots the 2D-UMAP stored in sub_p_adata and colors using each of the feature
    values in sub_p_adata.var. A .png file will be saved for each feature in 
    the directory specified by output_paths["output_umap_bc_feature_plot_path"] 
    and/or output_paths["output_umap_feature_plot_path"].

    Arguments
    ---------
    sub_p_adata: anndata.AnnData
        A pyInfinityFlow formatted AnnData object. Must have 'umap-x' and 
        'umap-y' in sub_p_adata.obs.columns (Required)

    file_handler: pyInfinityFlow.InfinityFlow_Utilities.InfinityFlowFileHandler
        The InfinityFlowFileHandler that is returned by pyInfinityFlow.
        InfinityFlow_Utilities.check_infinity_flow_annotation_dataframes. 
        (Required)

    output_paths: dict
        The output_paths dictionary created by the pyInfinityFlow.
        InfinityFlow_Utilities.setup_output_directories function (Required)

    background_corrected_data: pandas.DataFrame or None
        The background corrected data generated by pyInfinityFlow.
        InfinityFlow_Utilities.perform_background_correction. (Default=None)

    verbosity: int (0|1|2|3) 
        Specifies to what verbosity level the function will output progress and 
        debugging statements. (Default=0)


    Returns
    -------
    dict
        A dictionary that saves how much time each step of function takes.

    """
    t_start_bc_plotting = time.time()
    if file_handler.use_isotype_controls:
        map_feature_to_name = {}
        for tmp_feature in background_corrected_data.columns.values:
            map_feature_to_name[tmp_feature] = sub_p_adata.var.loc[tmp_feature, 'name']
        background_corrected_data.apply(lambda x: plot_feature_over_x_y_coordinates_and_save_fig(feature_vector=x.values, x=sub_p_adata.obs['umap-x'].values, y=sub_p_adata.obs['umap-y'].values, feature_name=map_feature_to_name[x.name], file_path=os.path.join(output_paths['output_umap_bc_feature_plot_path'], f"{map_feature_to_name[x.name].replace('/', '-')}_feature_plot.png")))
    t_end_bc_plotting = time.time()
    t_start_plotting = time.time()
    map_feature_to_name = {}
    map_feature_to_filepath = {}
    for tmp_feature in sub_p_adata.var.index.values:
        print(f'Working on plotting feature {tmp_feature}...')
        if sub_p_adata.var.loc[tmp_feature, 'IMPUTED']:
            tmp_output_name = sub_p_adata.var.loc[tmp_feature, 'name']
        elif len(sub_p_adata.var.loc[tmp_feature, 'name']) > 0:
            tmp_output_name = f"{tmp_feature}_{sub_p_adata.var.loc[tmp_feature, 'name']}"
        else:
            tmp_output_name = tmp_feature
        map_feature_to_name[tmp_feature] = tmp_output_name
        map_feature_to_filepath[tmp_feature] = os.path.join(output_paths['output_umap_feature_plot_path'], f"{tmp_output_name.replace('/', '-')}_feature_plot.png")
    anndata_to_df(sub_p_adata).apply(lambda x: plot_feature_over_x_y_coordinates_and_save_fig(feature_vector=x.values, x=sub_p_adata.obs['umap-x'].values, y=sub_p_adata.obs['umap-y'].values, feature_name=map_feature_to_name[x.name], file_path=map_feature_to_filepath[x.name]))
    t_end_plotting = time.time()
    tmp_timings = {'bc_plotting': t_end_bc_plotting - t_start_bc_plotting, 'plotting': t_end_plotting - t_start_plotting}
    return tmp_timings

def save_fcs_flow_anndata(sub_p_adata, file_handler, output_paths, background_corrected_data=None, background_corrected_var=None, add_umap=False, use_logicle=True, verbosity=0):
    """
    Save the pyInfinityFlow structured AnnData object to an .fcs file.

    Arguments
    ---------
    sub_p_adata: anndata.AnnData
        A pyInfinityFlow formatted AnnData object with the original parameter
        values as well as the imputed InfinityMarker values. Clusters must be 
        defined in the sub_p_adata.obs DataFrame. (Required)

    file_handler: pyInfinityFlow.InfinityFlow_Utilities.InfinityFlowFileHandler
        The InfinityFlowFileHandler that is returned by pyInfinityFlow.
        InfinityFlow_Utilities.check_infinity_flow_annotation_dataframes. 
        (Required)

    output_paths: dict
        The output_paths dictionary created by the pyInfinityFlow.
        InfinityFlow_Utilities.setup_output_directories function (Required)

    background_corrected_data: pandas.DataFrame or None
        The background corrected data generated by pyInfinityFlow.
        InfinityFlow_Utilities.perform_background_correction. (Default=None)

    background_corrected_var: pandas.DataFrame or None
        The background_corrected_var DataFrame generated by pyInfinityFlow.
        InfinityFlow_Utilities.perform_background_correction. (Default=None)

    add_umap: bool
        If True, will add the 'umap-x' and 'umap-y' features from sub_p_adata.obs 
        to sub_p_adata.X. Requires that the 2D-UMAP has been generated for 
        sub_p_adata and is specified in the 'umap-x' and 'umap-y' features of 
        sub_p_adata.obs (Default=False)

    use_logicle: bool
        If True, the function will attempt to inver the logicle normalization 
        before the data is saved.

    verbosity: int (0|1|2|3) 
        Specifies to what verbosity level the function will output progress and 
        debugging statements. (Default=0)


    Returns
    -------
    dict
        A dictionary that saves how much time each step of function takes.

    """
    t_start_file_export = time.time()
    printv(verbosity, v1='Writing out base prediction values to fcs file...')
    if use_logicle:
        apply_inverse_logicle_to_anndata(sub_p_adata)
    write_anndata_to_fcs(sub_p_adata, os.path.join(output_paths['output_regression_path'], 'infinity_flow_results.fcs'), add_umap=add_umap)
    if file_handler.use_isotype_controls:
        printv(verbosity, v1='Writing out background-corrected prediction values to fcs file...')
        tmp_var_index = background_corrected_var.index.values
        tmp_data_cols = background_corrected_data.columns.values
        tmp_data = sub_p_adata[:, tmp_data_cols].X.copy()
        tmp_var = sub_p_adata.var.loc[tmp_var_index, :].copy()
        tmp_var['name'] = tmp_var['name'].astype(str)
        sub_p_adata[:, tmp_data_cols].X = background_corrected_data.values
        sub_p_adata.var.loc[tmp_var_index, :] = background_corrected_var.values
        sub_p_adata.var['name'] = sub_p_adata.var['name'].astype(str)
        sub_p_adata.var.loc[tmp_var_index, 'name'] = 'bc_' + sub_p_adata.var.loc[tmp_var_index, 'name']
        sub_p_adata.var['name'] = sub_p_adata.var['name'].astype(str)
        if use_logicle:
            apply_inverse_logicle_to_anndata(sub_p_adata)
        write_anndata_to_fcs(sub_p_adata, os.path.join(output_paths['output_regression_path'], 'infinity_flow_results_with_background_correction.fcs'), add_umap=add_umap)
        sub_p_adata[:, tmp_data_cols].X = tmp_data
        sub_p_adata.var['name'] = sub_p_adata.var['name'].astype('str')
        sub_p_adata.var.loc[tmp_var_index, :] = tmp_var.values
    t_end_file_export = time.time()
    tmp_timings = {'file_export': t_end_file_export - t_start_file_export}
    return tmp_timings