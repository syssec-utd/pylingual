import pandas as pd
import re

def df_transform(df: pd.DataFrame) -> pd.DataFrame:
    df = fix_csv_tsv_mix_format_issues(df)
    df = df[df['unit'].str.contains('NR')]
    df = df.drop(columns=['unit', 'wstatus', 'line_number'])
    df = df.melt(id_vars=['isco08', 'geo\\time', 'file'], var_name='year', value_name='number_of_hospital_staff')
    df.reset_index(drop=True)
    df = remove_letters_in_numeric_columns(df)
    df = df[~df['geo\\time'].isin(['NO', 'RS', 'LI', 'IS', 'TR', 'ME', 'MK', 'CH', 'AL', 'FX'])]
    df = df[df['isco08'].str.contains('2221')]
    df = separate_multiple_isco_codes(df)
    df = df[df['isco08'].str.contains('2221')]
    df['line_number'] = range(1, len(df) + 1)
    return df

def fix_csv_tsv_mix_format_issues(df: pd.DataFrame) -> pd.DataFrame:
    df = df.applymap(lambda x: re.sub('\\s+', ' ', x) if isinstance(x, str) else x)
    df = df.apply(lambda x: x.astype(str).str.strip() if isinstance(x, object) else x)
    df = df.replace([':', ': b', ': d'], pd.NA)
    df = df.dropna(subset=df.columns[3:], how='all')
    df.columns = df.columns.str.replace(' ', '')
    return df

def remove_letters_in_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.astype({'isco08': str, 'number_of_hospital_staff': str})
    check_if_number_or_punctuation = lambda char: char.isdigit() or char in ['_', '.']
    df['number_of_hospital_staff'] = df['number_of_hospital_staff'].apply(lambda x: ''.join(filter(check_if_number_or_punctuation, x)))
    df['isco08'] = df['isco08'].apply(lambda x: ''.join(filter(check_if_number_or_punctuation, x)))
    df['number_of_hospital_staff'] = pd.to_numeric(df['number_of_hospital_staff'])
    return df

def separate_multiple_isco_codes(df: pd.DataFrame) -> pd.DataFrame:
    rows_with_multiple_isco_codes = df[df['isco08'].str.contains('_')]
    data = []
    for (index, row) in rows_with_multiple_isco_codes.iterrows():
        isco08_codes = row['isco08'].split('_')
        for code in isco08_codes:
            data.append([code, row['geo\\time'], row['file'], row['year'], row['number_of_hospital_staff']])
        df = df.drop(index=index)
    new_df = pd.DataFrame(data, columns=['isco08', 'geo\\time', 'file', 'year', 'number_of_hospital_staff'])
    df = pd.concat([new_df, df], ignore_index=True, sort=False)
    return df.drop_duplicates()