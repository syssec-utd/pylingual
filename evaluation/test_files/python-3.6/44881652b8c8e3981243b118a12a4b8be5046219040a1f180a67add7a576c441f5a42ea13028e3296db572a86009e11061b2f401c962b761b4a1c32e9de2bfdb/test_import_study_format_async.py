import pytest
from castoredc_api import CastorException
from castoredc_api.importer.import_data import import_data

class TestImportStudyFormatAsync:
    """Tests uploading data to Castor."""

    def test_import_study_value_success_format(self, import_study):
        """Tests if uploading value data is successful"""
        imported_data = import_data(data_source_path='tests/test_import/data_files_for_import_tests/data_file_study_values_format.xlsx', column_link_path='tests/test_import/link_files_for_import_tests/study_link_file.xlsx', study=import_study, label_data=False, target='Study', format_options={'date': '%B %d %Y', 'datetime': '%B %d %Y %I:%M %p', 'time': '%I:%M %p'}, use_async=True)
        assert imported_data == self.study_success

    def test_import_study_value_missing_format(self, import_study):
        """Tests if uploading value data with missings is successful"""
        imported_data = import_data(data_source_path='tests/test_import/data_files_for_import_tests/data_file_study_values_missings_format.xlsx', column_link_path='tests/test_import/link_files_for_import_tests/study_link_file.xlsx', study=import_study, label_data=False, target='Study', format_options={'date': '%B %d %Y', 'datetime': '%B %d %Y %I:%M %p', 'time': '%I:%M %p'}, use_async=True)
        assert imported_data == self.study_missing

    def test_import_study_value_error_format(self, import_study):
        """Tests if uploading value data with errors is successful"""
        with pytest.raises(CastorException) as e:
            import_data(data_source_path='tests/test_import/data_files_for_import_tests/data_file_study_values_errors_format.xlsx', column_link_path='tests/test_import/link_files_for_import_tests/study_link_file.xlsx', study=import_study, label_data=False, target='Study', format_options={'date': '%B %d %Y', 'datetime': '%B %d %Y %I:%M %p', 'time': '%I:%M %p'}, use_async=True)
        assert str(e.value) == self.study_error

    def test_import_study_error_during_upload_format(self, import_study):
        """Tests if uploading data with an error during the upload process fails properly"""
        with pytest.raises(CastorException) as e:
            import_data(data_source_path='tests/test_import/data_files_for_import_tests/data_file_study_values_errors_upload_format.xlsx', column_link_path='tests/test_import/link_files_for_import_tests/study_link_file.xlsx', study=import_study, label_data=False, target='Study', format_options={'date': '%B %d %Y', 'datetime': '%B %d %Y %I:%M %p', 'time': '%I:%M %p'}, use_async=True)
        assert str(e.value) == self.study_error
    study_success = {'110001': [{'success': {'base_bl_date': '16-03-2021', 'base_hb': '8.3', 'fac_V_leiden': '55;16-03-2021', 'onset_stroke': '16-03-2021;07:30', 'onset_trombectomy': '09:25', 'pat_birth_year': '1999', 'pat_sex': '0', 'pat_race': '1', 'his_family': '2;3;4'}, 'failed': {}, 'error': {}}], '110002': [{'success': {'base_bl_date': '17-03-2021', 'base_hb': '7.2', 'fac_V_leiden': '33;17-03-2021', 'onset_stroke': '17-03-2021;15:30', 'onset_trombectomy': '06:33', 'pat_birth_year': '1956', 'pat_sex': '0', 'pat_race': '2', 'his_family': '1;2'}, 'failed': {}, 'error': {}}], '110003': [{'success': {'base_bl_date': '16-03-2022', 'base_hb': '9.1', 'fac_V_leiden': '-45;18-03-2022', 'onset_stroke': '18-03-2022;02:00', 'onset_trombectomy': '12:24', 'pat_birth_year': '1945', 'pat_sex': '1', 'pat_race': '3', 'his_family': '0'}, 'failed': {}, 'error': {}}], '110004': [{'success': {'base_bl_date': '17-03-2022', 'base_hb': '3.2', 'fac_V_leiden': '28;19-03-2022', 'onset_stroke': '17-03-2022;21:43', 'onset_trombectomy': '23:23', 'pat_birth_year': '1933', 'pat_sex': '1', 'pat_race': '4', 'his_family': '5;7'}, 'failed': {}, 'error': {}}], '110005': [{'success': {'base_bl_date': '16-03-2023', 'base_hb': '10.3', 'fac_V_leiden': '5;20-03-2023', 'onset_stroke': '16-03-2023;07:22', 'onset_trombectomy': '08:14', 'pat_birth_year': '1921', 'pat_sex': '0', 'pat_race': '5', 'his_family': '8'}, 'failed': {}, 'error': {}}]}
    study_missing = {'110001': [{'success': {'base_bl_date': '16-03-2021', 'base_hb': '8.3', 'fac_V_leiden': '55;16-03-2021', 'onset_trombectomy': '09:25', 'pat_birth_year': '1999', 'pat_sex': '0', 'pat_race': '1'}, 'failed': {}, 'error': {}}], '110002': [{'success': {'base_bl_date': '17-03-2021', 'fac_V_leiden': '33;17-03-2021', 'onset_stroke': '17-03-2021;15:30', 'onset_trombectomy': '06:33', 'pat_sex': '0', 'pat_race': '2'}, 'failed': {}, 'error': {}}], '110003': [{'success': {'base_hb': '9.1', 'fac_V_leiden': '-45;18-03-2022', 'onset_stroke': '18-03-2022;02:00', 'onset_trombectomy': '12:24', 'his_family': '0'}, 'failed': {}, 'error': {}}], '110004': [{'success': {'base_bl_date': '17-03-2022', 'base_hb': '3.2', 'onset_stroke': '17-03-2022;21:43', 'pat_sex': '1', 'pat_race': '4', 'his_family': '5;7'}, 'failed': {}, 'error': {}}], '110005': [{'success': {'base_bl_date': '16-03-2023', 'base_hb': '10.3', 'fac_V_leiden': '5;20-03-2023', 'onset_stroke': '16-03-2023;07:22', 'onset_trombectomy': '08:14', 'pat_birth_year': '1921', 'pat_sex': '0', 'pat_race': '5', 'his_family': '8'}, 'failed': {}, 'error': {}}]}
    study_error = 'Non-viable data found in dataset to be imported. See output folder for details'
    study_error_wrong_field = "{'med_name': ['BAD_REQUEST', 'Unsupported field type']} caused at {'record_id': '110001', 'base_bl_date': '16-03-2021', 'base_hb': '8.3', 'fac_V_leiden': '55;16-03-2021', 'onset_stroke': '16-03-2021;07:30', 'onset_trombectomy': '09:25', 'pat_birth_year': '1999', 'pat_sex': '0', 'pat_race': '1', 'his_family': '2;3;4', 'med_name': 'Infliximab'}.\n See output folder for successful imports"