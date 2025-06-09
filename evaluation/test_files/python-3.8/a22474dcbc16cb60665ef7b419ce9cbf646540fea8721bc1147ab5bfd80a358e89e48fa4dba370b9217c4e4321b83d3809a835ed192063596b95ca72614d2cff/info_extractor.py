"""
Module contains objects and functions to support extracting information from email
"""
from time import time
import pandas as pd
from halo import Halo
from preprocessing_pgp.utils import parallelize_dataframe, sep_display
from preprocessing_pgp.email.validator import process_validate_email
from preprocessing_pgp.email.extractors.email_name_extractor import EmailNameExtractor
from preprocessing_pgp.email.extractors.email_yob_extractor import EmailYOBExtractor
from preprocessing_pgp.email.extractors.email_phone_extractor import EmailPhoneExtractor
from preprocessing_pgp.email.extractors.email_address_extractor import EmailAddressExtractor

class EmailInfoExtractor:
    """
    Class contains function to extract for email information
    """

    def __init__(self):
        self.name_extractor = EmailNameExtractor()
        self.yob_extractor = EmailYOBExtractor()
        self.phone_extractor = EmailPhoneExtractor()
        self.address_extractor = EmailAddressExtractor()

    @Halo(text='Extracting information from email', color='cyan', spinner='dots7', text_color='magenta')
    def extract_info(self, data: pd.DataFrame, email_name_col: str='email_name') -> pd.DataFrame:
        """
        Extract any information from email's name if possible

        Parameters
        ----------
        data : pd.DataFrame
            The input data contains an email_name column
        email_name_col : str, optional
            The name of the column contains email's name, by default 'email_name'

        Returns
        -------
        pd.DataFrame
            Data with additional info columns:
            * `username_extracted` : Extracted username from email name
            * `gender_extracted` : Extracted gender from username
            * `yob_extracted` : Extracted year of birth from email name
            * `phone_extracted` : Extracted phone number from email name
            * `address_extracted` : Extracted address from email name
        """
        extracted_data = self.name_extractor.extract_username(data, email_name_col)
        extracted_data = self.yob_extractor.extract_yob(extracted_data, email_name_col)
        extracted_data = self.phone_extractor.extract_phone(extracted_data, email_name_col)
        extracted_data = self.address_extractor.extract_address(extracted_data, email_name_col)
        return extracted_data

def process_extract_email_info(data: pd.DataFrame, email_col: str='email', n_cores: int=1) -> pd.DataFrame:
    """
    Process extracting information from email, extracted information may conclude:
    1. Username -- with accent
    2. Customer type -- derived from username
    3. Year of birth
    4. Address -- 3 levels
    5. Email group
    6. Auto-email

    Parameters
    ----------
    data : pd.DataFrame
        The input data contains an email column
    email_col : str
        The name of the column contains email's records, by default `email`
    n_cores

    Returns
    -------
    pd.DataFrame
        Original data with additional columns contains 6 additional information as above
    """
    email_data = data[[email_col]]
    orig_cols = data.columns
    info_extractor = EmailInfoExtractor()
    validated_data = process_validate_email(email_data, email_col=email_col, n_cores=n_cores)
    valid_email = validated_data.query('is_email_valid').copy()
    invalid_email = validated_data.query('~is_email_valid').copy()
    valid_email[f'{email_col}_name'] = valid_email[email_col].str.split('@').str[0]
    start_time = time()
    extracted_valid_email = parallelize_dataframe(valid_email, info_extractor.extract_info, n_cores=n_cores, email_name_col=f'{email_col}_name')
    extract_time = time() - start_time
    print(f'Extracting information from email takes {int(extract_time) // 60}m{int(extract_time) % 60}s')
    sep_display()
    final_data = pd.concat([extracted_valid_email, invalid_email])
    extracted_cols = ['is_email_valid', 'email_domain', 'private_email', 'customer_type', 'username_extracted', 'gender_extracted', 'yob_extracted', 'phone_extracted', 'address_extracted']
    final_data = pd.concat([data[orig_cols], final_data[extracted_cols]], axis=1)
    return final_data