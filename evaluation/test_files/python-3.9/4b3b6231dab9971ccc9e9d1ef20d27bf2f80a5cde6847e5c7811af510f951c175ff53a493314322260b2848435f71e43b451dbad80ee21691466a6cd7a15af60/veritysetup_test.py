import io
from textwrap import dedent
from pytest import raises
from mock import patch, Mock, MagicMock, call
from kiwi.utils.veritysetup import VeritySetup
from kiwi.exceptions import KiwiOffsetError
import kiwi.defaults as defaults

class TestVeritySetup:

    @patch('os.path.getsize')
    def setup(self, mock_os_path_getsize):
        mock_os_path_getsize.return_value = 4096
        self.veritysetup = VeritySetup('image_file', data_blocks=10)
        self.veritysetup_full = VeritySetup('image_file')
        self.verity_dict = {'UUID': '', 'Hashtype': '1', 'Datablocks': '10', 'Datablocksize': '4096', 'Hashblocksize': '4096', 'Hashalgorithm': 'sha256', 'Salt': 'fb074d1db50...', 'Roothash': 'e2728628377...'}

    @patch('os.path.getsize')
    def setup_method(self, cls, mock_os_path_getsize):
        self.setup()

    @patch('kiwi.utils.veritysetup.Command.run')
    def test_format(self, mock_Command_run):
        self.veritysetup.format()
        mock_Command_run.assert_called_once_with(['veritysetup', 'format', 'image_file', 'image_file', '--no-superblock', '--hash-offset=4096', '--hash-block-size=4096', '--data-blocks=10', '--data-block-size=4096'])

    @patch('kiwi.utils.veritysetup.Command.run')
    @patch('kiwi.utils.veritysetup.Temporary.new_file')
    @patch('os.path.getsize')
    def test_get_hash_byte_size(self, mock_os_path_getsize, mock_Temporary_new_file, mock_Command_run):
        tempfile = Mock()
        tempfile.name = 'tempfile'
        mock_Temporary_new_file.return_value = tempfile
        assert self.veritysetup.get_hash_byte_size() == mock_os_path_getsize.return_value
        mock_Command_run.assert_called_once_with(['veritysetup', 'format', 'image_file', 'tempfile', '--no-superblock', '--hash-block-size=4096', '--data-blocks=10', '--data-block-size=4096'])

    @patch('kiwi.utils.veritysetup.Command.run')
    def test_format_full(self, mock_Command_run):
        verity_call = Mock()
        verity_call.output = dedent('\n\n            VERITY header information for mysquash.img\n            UUID:\n            Hash type:\t\t\t1\n            Data blocks:        10\n            Data block size:\t4096\n            Hash block size:    4096\n            Hash algorithm:     sha256\n            Salt:               fb074d1db50...\n            Root hash:          e2728628377...\n        ')
        mock_Command_run.return_value = verity_call
        assert self.veritysetup_full.format() == self.verity_dict
        mock_Command_run.assert_called_once_with(['veritysetup', 'format', 'image_file', 'image_file', '--no-superblock', '--hash-offset=4096', '--hash-block-size=4096'])

    def test_store_credentials(self):
        self.veritysetup.verity_call = Mock()
        self.veritysetup.verity_dict = self.verity_dict
        target_block_id = Mock()
        target_block_id.get_blkid.return_value = 'uuid'
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value = MagicMock(spec=io.IOBase)
            file_handle = mock_open.return_value.__enter__.return_value
            self.veritysetup.store_credentials('credentials_file', target_block_id)
        assert file_handle.write.call_args_list == [call('Datablocks: 10\n'), call('Datablocksize: 4096\n'), call('Hashalgorithm: sha256\n'), call('Hashblocksize: 4096\n'), call('Hashtype: 1\n'), call('Roothash: e2728628377...\n'), call('Salt: fb074d1db50...\n'), call('UUID: \n'), call('Root hashoffset: 4096'), call('\n'), call('Superblock: --no-superblock'), call('\n')]

    @patch('kiwi.utils.veritysetup.BlockID')
    def test_get_block_storage_filesystem(self, mock_BlockID):
        block_id = Mock()
        mock_BlockID.return_value = block_id
        block_id.get_filesystem.return_value = 'ext3'
        assert self.veritysetup.get_block_storage_filesystem() == 'ext3'
        block_id.get_filesystem.side_effect = Exception
        assert self.veritysetup.get_block_storage_filesystem() == ''

    @patch('os.path.getsize')
    def test_write_verification_metadata_raises(self, mock_os_path_getsize):
        mock_os_path_getsize.return_value = 8192
        metadata_file = Mock()
        self.veritysetup.verification_metadata_file = metadata_file
        with raises(KiwiOffsetError):
            self.veritysetup.write_verification_metadata('/some/device')

    @patch('os.path.getsize')
    def test_write_verification_metadata(self, mock_os_path_getsize):
        mock_os_path_getsize.return_value = 4096
        metadata_file = Mock()
        metadata_file.name = 'metadata_file'
        self.veritysetup.verification_metadata_file = metadata_file
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value = MagicMock(spec=io.IOBase)
            file_handle = mock_open.return_value.__enter__.return_value
            self.veritysetup.write_verification_metadata('/some/device')
        assert mock_open.call_args_list == [call('metadata_file', 'rb'), call('/some/device', 'r+b')]
        file_handle.seek.assert_called_once_with(-defaults.DM_METADATA_OFFSET, 2)
        file_handle.write.assert_called_once_with(file_handle.read.return_value)

    @patch.object(VeritySetup, 'get_block_storage_filesystem')
    def test_create_verity_verification_metadata(self, mock_get_block_storage_filesystem):
        mock_get_block_storage_filesystem.return_value = 'ext4'
        self.veritysetup.verity_dict = self.verity_dict
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value = MagicMock(spec=io.IOBase)
            file_handle = mock_open.return_value.__enter__.return_value
            self.veritysetup.create_verity_verification_metadata()
        assert file_handle.write.call_args_list == [call(b'1 ext4 rw verity'), call(b'\xff'), call(b'1 4096 4096 10 1 sha256 e2728628377... fb074d1db50...'), call(b'\xff'), call(b'\x00')]

    @patch('kiwi.utils.veritysetup.Signature')
    def test_sign_verification_metadata(self, mock_Signature):
        metadata_file = Mock()
        metadata_file.name = 'metadata_file'
        self.veritysetup.verification_metadata_file = metadata_file
        self.veritysetup.sign_verification_metadata()
        mock_Signature.return_value.sign.assert_called_once_with()