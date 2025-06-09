import logging
from pathlib import Path
import pandas as pd
from datetime import datetime
import numpy as np
log = logging.getLogger(__name__)

def read_file(input, dates):
    """
    Reads the csv file as a pandas DataFrame
    """
    flatfile = pd.read_csv(input, parse_dates=dates, dayfirst=True)
    return flatfile

def _merge_dfs(flatfile, old_df, la_name):
    """
    Deletes existing data for new LA from pan file
    Merges new LA data to pan file
    """
    old_df = old_df.drop(old_df[old_df['LA'] == la_name].index)
    flatfile = pd.concat([flatfile, old_df], axis=0, ignore_index=True)
    return flatfile

def merge_agg_files(flat_output, dates, la_name, flatfile):
    """
    Checks if pan file exists
    Passes old and new file to function to be merged
    """
    output_file = Path(flat_output, f'pan_London_CIN_flatfile.csv')
    if output_file.is_file():
        old_df = pd.read_csv(output_file, parse_dates=dates, dayfirst=True)
        flatfile = _merge_dfs(flatfile, old_df, la_name)
    return flatfile

def export_flatfile(flat_output, flatfile):
    output_path = Path(flat_output, f'pan_London_CIN_flatfile.csv')
    flatfile.to_csv(output_path, index=False)

def filter_flatfile(flatfile, filter):
    """
    Filters rows to specified events
    Removes redundant columns that relate to other types of event
    """
    filtered_flatfile = flatfile[flatfile['Type'] == filter]
    filtered_flatfile = filtered_flatfile.dropna(axis=1, how='all')
    return filtered_flatfile

def split_factors(factors):
    """
    Creates a new set of columns from the flatfile with a column for each assessment factor
    Rows correspond the the rows of the flatfile and should have a value of 0 or 1 for each column
    """
    factor_cols = factors.Factors
    factor_cols = factor_cols.str.split(',', expand=True)
    factor_cols = factor_cols.stack()
    factor_cols = factor_cols.str.get_dummies()
    factor_cols = factor_cols.groupby(level=0).sum()
    assert factor_cols.isin([0, 1]).all(axis=None)
    factors = pd.concat([factors, factor_cols], axis=1)
    return factors

def export_factfile(analysis_output, factors):
    """
    Writes the factors output as a csv
    """
    output_path = Path(analysis_output, f'CIN_Census_factors.csv')
    factors.to_csv(output_path, index=False)

def referral_inputs(flatfile):
    """
    Creates three inputs for referral journeys analysis file
    """
    ref = filter_flatfile(flatfile, filter='CINreferralDate')
    s17 = filter_flatfile(flatfile, filter='AssessmentActualStartDate')
    s47 = filter_flatfile(flatfile, filter='S47ActualStartDate')
    return (ref, s17, s47)

def _time_between_date_series(later_date_series, earlier_date_series, years=0, days=0):
    days_series = later_date_series - earlier_date_series
    days_series = days_series.dt.days
    if days == 1:
        return days_series
    elif years == 1:
        years_series = (days_series / 365).apply(np.floor)
        years_series = years_series.astype('Int32')
        return years_series

def _filter_event_series(dataset, days_series, max_days):
    dataset = dataset[(dataset[days_series] <= max_days) & (dataset[days_series] >= 0)]
    return dataset

def merge_ref_s17(ref, s17, ref_assessment):
    """
    Merges ref and s17 views together, keeping only logically valid matches
    """
    ref_s17 = ref.merge(s17[['LAchildID', 'AssessmentActualStartDate']], how='left', on='LAchildID')
    ref_s17['days_to_s17'] = _time_between_date_series(ref_s17['AssessmentActualStartDate'], ref_s17['CINreferralDate'], days=1)
    ref_s17 = _filter_event_series(ref_s17, 'days_to_s17', ref_assessment)
    ref_s17 = ref_s17[['Date', 'LAchildID', 'AssessmentActualStartDate', 'days_to_s17']]
    return ref_s17

def merge_ref_s47(ref, s47, ref_assessment):
    """
    Merges ref and s47 views together, keeping only logically valid matches
    """
    ref_s47 = ref.merge(s47[['LAchildID', 'S47ActualStartDate']], how='left', on='LAchildID')
    ref_s47['days_to_s47'] = _time_between_date_series(ref_s47['S47ActualStartDate'], ref_s47['CINreferralDate'], days=1)
    ref_s47 = _filter_event_series(ref_s47, 'days_to_s47', ref_assessment)
    ref_s47 = ref_s47[['Date', 'LAchildID', 'S47ActualStartDate', 'days_to_s47']]
    return ref_s47

def ref_outcomes(ref, ref_s17, ref_s47):
    """
    Merges views together to give all outcomes of referrals in one place
    Outcomes column defaults to NFA unless there is a relevant S17 or S47 event to match
    Calculates age of child at referral
    """
    ref_outs = ref.merge(ref_s17, on=['Date', 'LAchildID'], how='left')
    ref_outs = ref_outs.merge(ref_s47, on=['Date', 'LAchildID'], how='left')
    ref_outs['referral_outcome'] = 'NFA'
    ref_outs.loc[ref_outs['AssessmentActualStartDate'].notnull(), 'referral_outcome'] = 'S17'
    ref_outs.loc[ref_outs['S47ActualStartDate'].notnull(), 'referral_outcome'] = 'S47'
    ref_outs.loc[ref_outs['AssessmentActualStartDate'].notnull() & ref_outs['S47ActualStartDate'].notnull(), 'referral_outcome'] = 'Both S17 & S47'
    ref_outs['Age at referral'] = _time_between_date_series(ref_outs['CINreferralDate'], ref_outs['PersonBirthDate'], years=1)
    return ref_outs

def export_reffile(analysis_output, ref_outs):
    """
    Writes the referral journeys output as a csv
    """
    output_path = Path(analysis_output, f'CIN_Census_referrals.csv')
    ref_outs.to_csv(output_path, index=False)

def journey_inputs(flatfile):
    """
    Creates the input for the journey analysis file
    """
    s47_j = filter_flatfile(flatfile, 'S47ActualStartDate')
    cpp = filter_flatfile(flatfile, 'CPPstartDate')
    return (s47_j, cpp)

def journey_merge(s47_j, cpp, icpc_cpp_days, s47_cpp_days):
    """
    Merges inputs to produce outcomes file
    """
    s47_cpp = s47_j.merge(cpp[['LAchildID', 'CPPstartDate']], how='left', on='LAchildID')
    s47_cpp['icpc_to_cpp'] = _time_between_date_series(s47_cpp['CPPstartDate'], s47_cpp['DateOfInitialCPC'], days=1)
    s47_cpp['s47_to_cpp'] = _time_between_date_series(s47_cpp['CPPstartDate'], s47_cpp['S47ActualStartDate'], days=1)
    s47_cpp = s47_cpp[(s47_cpp['icpc_to_cpp'] >= 0) & (s47_cpp['icpc_to_cpp'] <= icpc_cpp_days) | (s47_cpp['s47_to_cpp'] >= 0) & (s47_cpp['s47_to_cpp'] <= s47_cpp_days)]
    s47_outs = s47_j.merge(s47_cpp[['Date', 'LAchildID', 'CPPstartDate', 'icpc_to_cpp', 's47_to_cpp']], how='left', on=['Date', 'LAchildID'])
    return s47_outs

def s47_paths(s47_outs, s47_day_limit, icpc_day_limit):
    """
    Creates an output that can generate a Sankey diagram of outcomes from S47 events
    """
    for y in s47_outs['YEAR']:
        s47_outs['cin_census_close'] = datetime(int(y), 3, 31)
    s47_outs['s47_max_date'] = s47_outs['cin_census_close'] - pd.Timedelta(s47_day_limit)
    s47_outs['icpc_max_date'] = s47_outs['cin_census_close'] - pd.Timedelta(icpc_day_limit)
    step1 = s47_outs.copy()
    step1['Source'] = 'S47 strategy discussion'
    step1['Destination'] = np.nan
    step1.loc[step1['DateOfInitialCPC'].notnull(), 'Destination'] = 'ICPC'
    step1.loc[step1['DateOfInitialCPC'].isnull() & step1['CPPstartDate'].notnull(), 'Destination'] = 'CPP start'
    step1.loc[step1['Destination'].isnull() & (step1['S47ActualStartDate'] >= step1['s47_max_date']), 'Destination'] = 'TBD - S47 too recent'
    step1.loc[step1['Destination'].isnull(), 'Destination'] = 'No ICPC or CPP'
    step2 = step1[step1['Destination'] == 'ICPC']
    step2['Source'] = 'ICPC'
    step2['Destination'] = np.nan
    step2.loc[step2['CPPstartDate'].notnull(), 'Destination'] = 'CPP start'
    step2.loc[step2['Destination'].isnull() & (step2['DateOfInitialCPC'] >= step2['icpc_max_date']), 'Destination'] = 'TBD - ICPC too recent'
    step2.loc[step2['Destination'].isnull(), 'Destination'] = 'No CPP'
    s47_journey = pd.concat([step1, step2])
    s47_journey['Age at S47'] = _time_between_date_series(s47_journey['S47ActualStartDate'], s47_journey['PersonBirthDate'], years=1)
    return s47_journey

def export_journeyfile(analysis_output, s47_journey):
    """
    Writes the S47 journeys output as a csv
    """
    output_path = Path(analysis_output, f'CIN_Census_S47_journey.csv')
    s47_journey.to_csv(output_path, index=False)