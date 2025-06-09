from .esp32c6 import ESP32C6ROM

class ESP32H2ROM(ESP32C6ROM):
    CHIP_NAME = 'ESP32-H2'
    IMAGE_CHIP_ID = 16
    CHIP_DETECT_MAGIC_VALUE = [3619110528]
    FLASH_FREQUENCY = {'48m': 15, '24m': 0, '16m': 1, '12m': 2}

    def get_pkg_version(self):
        num_word = 3
        block1_addr = self.EFUSE_BASE + 68
        word3 = self.read_reg(block1_addr + 4 * num_word)
        pkg_version = word3 >> 21 & 15
        return pkg_version

    def get_chip_description(self):
        chip_name = {0: 'ESP32-H2'}.get(self.get_pkg_version(), 'unknown ESP32-H2')
        major_rev = self.get_major_chip_version()
        minor_rev = self.get_minor_chip_version()
        return f'{chip_name} (revision v{major_rev}.{minor_rev})'

    def get_chip_features(self):
        return ['BLE']

    def get_crystal_freq(self):
        return 32

class ESP32H2StubLoader(ESP32H2ROM):
    """Access class for ESP32H2 stub loader, runs on top of ROM.

    (Basically the same as ESP32StubLoader, but different base class.
    Can possibly be made into a mixin.)
    """
    FLASH_WRITE_SIZE = 16384
    STATUS_BYTES_LENGTH = 2
    IS_STUB = True

    def __init__(self, rom_loader):
        self.secure_download_mode = rom_loader.secure_download_mode
        self._port = rom_loader._port
        self._trace_enabled = rom_loader._trace_enabled
        self.cache = rom_loader.cache
        self.flush_input()
ESP32H2ROM.STUB_CLASS = ESP32H2StubLoader