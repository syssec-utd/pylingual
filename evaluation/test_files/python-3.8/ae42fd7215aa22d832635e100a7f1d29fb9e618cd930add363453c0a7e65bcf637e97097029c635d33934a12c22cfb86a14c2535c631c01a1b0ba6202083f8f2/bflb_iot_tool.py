import re
import os
import sys
import shutil
import argparse
import subprocess
import traceback
import hashlib
import lzma
from importlib import reload
from os.path import expanduser
try:
    import bflb_path
except ImportError:
    from libs import bflb_path
import config as gol
from libs import bflb_utils
from libs import bflb_eflash_loader
from libs import bflb_toml as toml
from libs import bflb_flash_select
from libs.bflb_utils import verify_hex_num, get_eflash_loader, get_serial_ports, convert_path
from libs.bflb_configobj import BFConfigParser
import libs.bflb_pt_creater as partition
import libs.bflb_eflash_loader as eflash_loader
import libs.bflb_efuse_boothd_create as eb_create
import libs.bflb_img_create as img_create
import libs.bflb_ro_params_device_tree as bl_ro_device_tree
parser_eflash = bflb_utils.eflash_loader_parser_init()
if getattr(sys, 'frozen', False):
    app_path = os.path.dirname(sys.executable)
else:
    app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(app_path)
chip_path = os.path.join(app_path, 'chips')
try:
    import changeconf as cgc
    conf_sign = True
except ImportError:
    conf_sign = False

def find_boot2(path, boot2):
    for (root, dirs, files) in os.walk(path, True):
        for item in files:
            if item == boot2:
                filepath = os.path.join(root, item)
                return filepath
    return None

def parse_rfpa(bin):
    with open(bin, 'rb') as fp:
        content = fp.read()
        return content[1024:1032]

def flash_type(chip_flash_name):
    cfg_file_name_list = chip_flash_name.split('_')
    _type = cfg_file_name_list[1]
    vendor = cfg_file_name_list[2]
    size = cfg_file_name_list[3]
    return (_type, vendor, size)

def img_create_sha256_data(data_bytearray):
    hashfun = hashlib.sha256()
    hashfun.update(data_bytearray)
    return bflb_utils.hexstr_to_bytearray(hashfun.hexdigest())

def bl_get_largest_addr(addrs, files):
    maxlen = 0
    datalen = 0
    for i in range(len(addrs)):
        if int(addrs[i], 16) > maxlen:
            maxlen = int(addrs[i], 16)
            datalen = os.path.getsize(os.path.join(app_path, files[i]))
    return maxlen + datalen

def bl_get_file_data(files):
    datas = []
    for file in files:
        with open(os.path.join(app_path, file), 'rb') as fp:
            data = fp.read()
        datas.append(data)
    return datas

def bl_create_flash_default_data(length):
    datas = bytearray(length)
    for i in range(length):
        datas[i] = 255
    return datas

def generate_romfs_img(romfs_dir, dst_img_name):
    exe = None
    if os.name == 'nt':
        exe = os.path.join(app_path, 'utils/genromfs', 'genromfs.exe')
    elif os.name == 'posix':
        machine = os.uname().machine
        if machine == 'x86_64':
            exe = os.path.join(app_path, 'utils/genromfs', 'genromfs_amd64')
        elif machine == 'armv7l':
            exe = os.path.join(app_path, 'utils/genromfs', 'genromfs_armel')
        elif machine == 'arm64':
            exe = os.path.join(app_path, 'utils/genromfs', 'genromfs_arm64')
    if exe is None:
        bflb_utils.printf('NO supported genromfs exe for your platform!')
        return -1
    dir = os.path.abspath(romfs_dir)
    dst = os.path.abspath(dst_img_name)
    bflb_utils.printf('Generating romfs image %s using directory %s ... ' % (dst, dir))
    try:
        ret = subprocess.call([exe, '-d', dir, '-f', dst, '-a', '64'])
    except Exception as e:
        exe = os.path.join(app_path, 'utils/genromfs', 'genromfs_arm64')
        ret = subprocess.call([exe, '-d', dir, '-f', dst, '-a', '64'])
    return ret

def check_pt_table(pt_parcel, file, name_list):
    if len(file) > 0:
        try:
            for file_name in file:
                file_size = os.path.getsize(os.path.join(app_path, file_name))
                if 'whole_img_boot2.bin' in file_name:
                    if file_size > pt_parcel['pt_addr0']:
                        bflb_utils.printf('Error: boot2 bin size is overflow with partition table')
                        return False
                for name in name_list:
                    new_name = name.lower()
                    if new_name == 'factory':
                        continue
                    elif new_name == 'fw':
                        if 'whole_img.bin' in file_name:
                            if file_size > pt_parcel['fw_len']:
                                bflb_utils.printf('Error: fw bin size is overflow with partition table')
                                bflb_utils.printf('whole_img.bin szie=', file_size)
                                bflb_utils.printf('fw_len=', pt_parcel['fw_len'])
                                return False
                        continue
                    if 'whole_img_' + new_name + '.bin' in file_name or new_name + '.bin' in file_name:
                        if file_size > pt_parcel[new_name + '_len']:
                            bflb_utils.printf('Error: %s bin size is overflow with partition table' % new_name)
                            return False
        except Exception as e:
            bflb_utils.printf(e)
            return False
    return True

def check_pt_table_old(pt_parcel, file):
    if len(file) > 0:
        i = 0
        try:
            while i < len(file):
                file_name = file[i]
                file_size = os.path.getsize(os.path.join(app_path, file_name))
                if 'whole_img_boot2.bin' in file_name:
                    if file_size > pt_parcel['pt_addr0']:
                        bflb_utils.printf('Error: boot2 bin size is overflow with partition table')
                        return False
                if 'whole_img_cpu0.bin' in file_name:
                    if file_size > pt_parcel['fw_cpu0_len']:
                        bflb_utils.printf('Error: cpu0 fw bin size is overflow with partition table')
                        return False
                if 'whole_img.bin' in file_name:
                    if file_size > pt_parcel['fw_len']:
                        bflb_utils.printf('Error: fw bin size is overflow with partition table')
                        return False
                if 'whole_img_mfg.bin' in file_name:
                    if file_size > pt_parcel['mfg_len']:
                        bflb_utils.printf('Error: mfg bin size is overflow with partition table')
                        return False
                if 'media.bin' in file_name:
                    if file_size > pt_parcel['media_len']:
                        bflb_utils.printf('Error: media bin size is overflow with partition table')
                        return False
                if 'whole_img_d0fw.bin' in file_name:
                    if file_size > pt_parcel['fw_d0_len']:
                        bflb_utils.printf('Error: d0fw bin size is overflow with partition table')
                        return False
                if 'imtb.bin' in file_name:
                    if file_size > pt_parcel['imtb_len']:
                        bflb_utils.printf('Error: imtb bin size is overflow with partition table')
                        return False
                if 'kv.bin' in file_name:
                    if file_size > pt_parcel['kv_len']:
                        bflb_utils.printf('Error: kv bin size is overflow with partition table')
                        return False
                if 'dtb.bin' in file_name:
                    if file_size > pt_parcel['dtb_len']:
                        bflb_utils.printf('Error: dtb bin size is overflow with partition table')
                        return False
                i += 1
        except Exception as e:
            bflb_utils.printf(e)
            return False
    return True

def exe_genitor(list_args):
    p = subprocess.Popen(list_args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while subprocess.Popen.poll(p) is None:
        try:
            r = p.stdout.readline().strip().decode('utf-8')
            if r == '':
                break
            bflb_utils.printf(r)
        except UnicodeDecodeError:
            continue

class BflbIotTool(object):

    def __init__(self, chipname='bl60x', chiptype='bl60x'):
        self.efuse_load_en = False
        self.config = {}
        self.chipname = chipname
        self.chiptype = chiptype
        self.eflash_loader_t = bflb_eflash_loader.BflbEflashLoader(chipname, chiptype)
        eflash_loader_cfg_org = os.path.join(chip_path, chipname, 'eflash_loader/eflash_loader_cfg.conf')
        self.eflash_loader_cfg = os.path.join(chip_path, chipname, 'eflash_loader/eflash_loader_cfg.ini')
        if os.path.isfile(self.eflash_loader_cfg) is False:
            shutil.copyfile(eflash_loader_cfg_org, self.eflash_loader_cfg)
        if chiptype == 'bl60x':
            bh_cfg_file_org = os.path.join(chip_path, chipname, 'efuse_bootheader/efuse_bootheader_cfg_dp.conf')
        else:
            bh_cfg_file_org = os.path.join(chip_path, chipname, 'efuse_bootheader/efuse_bootheader_cfg.conf')
        self.bh_cfg_file = os.path.join(chip_path, chipname, 'img_create_iot/efuse_bootheader_cfg.ini')
        if os.path.isfile(self.bh_cfg_file) is False:
            shutil.copyfile(bh_cfg_file_org, self.bh_cfg_file)

    def bl60x_fw_boot_head_gen(self, boot2, xtal, config, encrypt=False, sign=False, chipname='bl60x', chiptype='bl60x', cpu_type=None, boot2_en=False):
        cfg = BFConfigParser()
        cfg.read(config)
        dict_xtal = gol.xtal_type[chiptype]
        if cpu_type is not None:
            bootheader_section_name = 'BOOTHEADER_' + cpu_type.upper() + '_CFG'
        elif 'BOOTHEADER_CPU0_CFG' in cfg.sections():
            bootheader_section_name = 'BOOTHEADER_CPU0_CFG'
        elif 'BOOTHEADER_GROUP0_CFG' in cfg.sections():
            bootheader_section_name = 'BOOTHEADER_GROUP0_CFG'
        else:
            bootheader_section_name = 'BOOTHEADER_CFG'
        if chiptype == 'bl702':
            if boot2_en is True:
                cfg.set(bootheader_section_name, 'boot2_enable', 1)
            else:
                cfg.set(bootheader_section_name, 'boot2_enable', 0)
        if boot2 is True:
            if chiptype == 'bl808':
                cfg.set(bootheader_section_name, 'group_image_offset', '0x2000')
                cfg.set(bootheader_section_name, 'd0_config_enable', '0')
                cfg.set(bootheader_section_name, 'lp_config_enable', '0')
            elif chiptype == 'bl616' or chiptype == 'wb03':
                cfg.set(bootheader_section_name, 'group_image_offset', '0x2000')
                cfg.set(bootheader_section_name, 'custom_vendor_boot_offset', '0x2000')
            else:
                cfg.set(bootheader_section_name, 'img_start', '0x2000')
                cfg.set(bootheader_section_name, 'cache_enable', '1')
                if cpu_type is not None:
                    cfg.set(bootheader_section_name, 'halt_cpu1', '1')
        elif chiptype == 'bl60x':
            cfg.set(bootheader_section_name, 'halt_cpu1', '0')
        if encrypt:
            cfg.set(bootheader_section_name, 'encrypt_type', '1')
        else:
            cfg.set(bootheader_section_name, 'encrypt_type', '0')
        if sign:
            cfg.set(bootheader_section_name, 'sign', '1')
        else:
            cfg.set(bootheader_section_name, 'sign', '0')
        if chiptype == 'bl60x' or chiptype == 'bl602' or chiptype == 'bl702':
            bflb_utils.printf('bl60x_fw_boot_head_gen xtal: %s' % xtal)
            cfg.set(bootheader_section_name, 'xtal_type', dict_xtal.index(xtal))
        cfg.write(config)
        eb_create.efuse_boothd_create_process(chipname, chiptype, config)

    def bl60x_mfg_boot_head_gen(self, mfg_addr, xtal, config, chipname='bl60x', chiptype='bl60x', cpu_type=None, encrypt=False, sign=False):
        cfg = BFConfigParser()
        cfg.read(config)
        bflb_utils.printf(mfg_addr)
        dict_xtal = gol.xtal_type[chiptype]
        if cpu_type is not None:
            bootheader_section_name = 'BOOTHEADER_' + cpu_type.upper() + '_CFG'
        elif 'BOOTHEADER_CPU0_CFG' in cfg.sections():
            bootheader_section_name = 'BOOTHEADER_CPU0_CFG'
        elif 'BOOTHEADER_GROUP0_CFG' in cfg.sections():
            bootheader_section_name = 'BOOTHEADER_GROUP0_CFG'
        else:
            bootheader_section_name = 'BOOTHEADER_CFG'
        if chiptype == 'bl808':
            cfg.set(bootheader_section_name, 'group_image_offset', hex(int(mfg_addr, 16) + 4096))
            cfg.set(bootheader_section_name, 'd0_config_enable', '0')
            cfg.set(bootheader_section_name, 'lp_config_enable', '0')
        elif chiptype == 'bl616' or chiptype == 'wb03':
            cfg.set(bootheader_section_name, 'group_image_offset', hex(int(mfg_addr, 16) + 4096))
        else:
            cfg.set(bootheader_section_name, 'img_start', mfg_addr)
            cfg.set(bootheader_section_name, 'cache_enable', '1')
            if cpu_type is not None:
                cfg.set(bootheader_section_name, 'halt_cpu1', '1')
        if encrypt:
            cfg.set(bootheader_section_name, 'encrypt_type', '1')
        else:
            cfg.set(bootheader_section_name, 'encrypt_type', '0')
        if sign:
            cfg.set(bootheader_section_name, 'sign', '1')
        else:
            cfg.set(bootheader_section_name, 'sign', '0')
        bflb_utils.printf('bl60x_mfg_boot_head_gen xtal: %s' % xtal)
        cfg.set(bootheader_section_name, 'xtal_type', dict_xtal.index(xtal))
        cfg.write(config)
        eb_create.efuse_boothd_create_process(chipname, chiptype, config)

    def bl60x_image_gen_cfg(self, chipname, chiptype, raw_bin_name, bintype, key=None, iv=None, publickey=None, privatekey=None, cfg_ini=None, group_type=None):
        efuse_file = os.path.join(chip_path, chipname, 'efuse_bootheader/efusedata.bin')
        efuse_mask_file = os.path.join(chip_path, chipname, 'efuse_bootheader/efusedata_mask.bin')
        if chiptype == 'bl60x':
            bh_file = os.path.join(chip_path, chipname, 'efuse_bootheader/bootheader_cpu0.bin')
        elif chiptype == 'bl808' or chiptype == 'bl616' or chiptype == 'wb03':
            bh_file = os.path.join(chip_path, chipname, 'efuse_bootheader/bootheader_group0.bin')
        else:
            bh_file = os.path.join(chip_path, chipname, 'efuse_bootheader/bootheader.bin')
        cfg = BFConfigParser()
        if cfg_ini in [None, '']:
            if chiptype == 'bl60x':
                f_org = os.path.join(chip_path, chipname, 'img_create_iot', 'img_create_cfg_dp.conf')
            else:
                f_org = os.path.join(chip_path, chipname, 'img_create_iot', 'img_create_cfg.conf')
            f = os.path.join(chip_path, chipname, 'img_create_iot', 'img_create_cfg.ini')
            if os.path.isfile(f) is False:
                shutil.copyfile(f_org, f)
        else:
            f = cfg_ini
        cfg.read(f)
        if bintype == 'fw':
            if group_type is None or group_type == 'Group0':
                bootinfo_file = os.path.join(chip_path, chipname, 'img_create_iot', 'bootinfo.bin')
                img_file = os.path.join(chip_path, chipname, 'img_create_iot', 'img.bin')
            else:
                bootinfo_file = os.path.join(chip_path, chipname, 'img_create_iot', 'bootinfo_{0}.bin'.format(group_type.lower()))
                img_file = os.path.join(chip_path, chipname, 'img_create_iot', 'img_{0}.bin'.format(group_type.lower()))
        else:
            bootinfo_file = os.path.join(chip_path, chipname, 'img_create_iot', 'bootinfo_{0}.bin'.format(bintype))
            img_file = os.path.join(chip_path, chipname, 'img_create_iot', 'img_{0}.bin'.format(bintype))
        if group_type is not None:
            img_section_name = 'Img_' + group_type + '_Cfg'
        elif 'Img_CPU0_Cfg' in cfg.sections():
            img_section_name = 'Img_CPU0_Cfg'
        elif 'Img_Group0_Cfg' in cfg.sections():
            img_section_name = 'Img_Group0_Cfg'
        else:
            img_section_name = 'Img_Cfg'
        cfg.set(img_section_name, 'boot_header_file', bh_file)
        cfg.set(img_section_name, 'efuse_file', efuse_file)
        cfg.set(img_section_name, 'efuse_mask_file', efuse_mask_file)
        cfg.set(img_section_name, 'segdata_file', raw_bin_name)
        cfg.set(img_section_name, 'bootinfo_file', bootinfo_file)
        cfg.set(img_section_name, 'img_file', img_file)
        if key:
            cfg.set(img_section_name, 'aes_key_org', key)
        if iv:
            cfg.set(img_section_name, 'aes_iv', iv)
        if publickey:
            cfg.set(img_section_name, 'publickey_file', publickey)
        if privatekey:
            cfg.set(img_section_name, 'privatekey_file_uecc', privatekey)
        cfg.write(f, 'w')
        return f

    def bl60x_mfg_ota_header(self, chipname, file_bytearray, use_xz):
        ota_cfg = os.path.join(chip_path, chipname, 'conf/ota.toml')
        parsed_toml = toml.load(ota_cfg)
        header_len = 512
        header = bytearray()
        file_len = len(file_bytearray)
        m = hashlib.sha256()
        if 'version_header' in parsed_toml['ota']:
            data = bytearray(parsed_toml['ota']['version_header'].encode())
        else:
            data = b'BL60X_OTA_Ver1.0'
        bflb_utils.printf(data.decode())
        for b in data:
            header.append(b)
        if use_xz:
            data = b'XZ  '
        else:
            data = b'RAW '
        for b in data:
            header.append(b)
        file_len_bytes = file_len.to_bytes(4, byteorder='little')
        for b in file_len_bytes:
            header.append(b)
        header.append(1)
        header.append(2)
        header.append(3)
        header.append(4)
        header.append(5)
        header.append(6)
        header.append(7)
        header.append(8)
        data = bytearray(parsed_toml['ota']['version_hardware'].encode())
        data_len = 16 - len(data)
        for b in data:
            header.append(b)
        while data_len > 0:
            header.append(0)
            data_len = data_len - 1
        data = bytearray(parsed_toml['ota']['version_software'].encode())
        data_len = 16 - len(data)
        for b in data:
            header.append(b)
        while data_len > 0:
            header.append(0)
            data_len = data_len - 1
        m.update(file_bytearray)
        hash_bytes = m.digest()
        for b in hash_bytes:
            header.append(b)
        header_len = header_len - len(header)
        while header_len > 0:
            header.append(255)
            header_len = header_len - 1
        return header

    def bl60x_mfg_ota_header_haier(self, fw_ota_bin, chipname='bl60x', version='', dir_ota=None):
        fw_ota_bin_ver_haier = 'M_1.0.00-e-UDISCOVERY_UWT'
        fw_ota_bin_sn_haier = '00' * 16
        fw_ota_bin_md5 = hashlib.md5(fw_ota_bin).hexdigest()
        fw_ota_bin_haier = bytes.fromhex(fw_ota_bin_ver_haier.encode('utf-8').hex() + '00' * 7 + fw_ota_bin_sn_haier + fw_ota_bin_md5.encode('utf-8').hex() + version.encode('utf-8').hex() + '00' * (48 - len(version)))
        if dir_ota:
            fw_ota_path_haier = os.path.join(dir_ota, 'FW_OTA_Haier.bin.ota')
        else:
            fw_ota_path_haier = os.path.join(chip_path, chipname, 'ota', 'FW_OTA_Haier.bin.ota')
        with open(fw_ota_path_haier, mode='wb') as f:
            f.write(fw_ota_bin_haier + fw_ota_bin)

    def bl60x_mfg_ota_xz_gen(self, ota_path, chipname='bl60x', chiptype='bl60x', cpu_type=None, fw_len=0):
        bl60x_xz_filters = [{'id': lzma.FILTER_LZMA2, 'dict_size': 32768}]
        fw_ota_bin = bytearray()
        fw_ota_bin_xz = bytearray()
        if cpu_type is None or cpu_type == 'Group0':
            fw_ota_path = os.path.join(ota_path, 'FW_OTA.bin')
        else:
            fw_ota_path = os.path.join(ota_path, cpu_type + '_OTA.bin')
        with open(fw_ota_path, mode='rb') as bin_f:
            file_bytes = bin_f.read()
            for b in file_bytes:
                fw_ota_bin.append(b)
        if cpu_type is None or cpu_type == 'Group0':
            fw_ota_path = os.path.join(ota_path, 'FW_OTA.bin.xz')
        else:
            fw_ota_path = os.path.join(ota_path, cpu_type + '_OTA.bin.xz')
        with lzma.open(fw_ota_path, mode='wb', check=lzma.CHECK_CRC32, filters=bl60x_xz_filters) as xz_f:
            xz_f.write(fw_ota_bin)
        with open(fw_ota_path, mode='rb') as f:
            file_bytes = f.read()
            for b in file_bytes:
                fw_ota_bin_xz.append(b)
        bflb_utils.printf('OTA XZ file len = ', len(fw_ota_bin_xz))
        bflb_utils.printf('Partiton len = ', fw_len)
        if len(fw_ota_bin_xz) > fw_len:
            bflb_utils.printf("Error: fw1 xz bin size is overflow with partition table, don't create ota bin")
            return False
        fw_ota_bin_xz_ota = self.bl60x_mfg_ota_header(chipname, fw_ota_bin_xz, use_xz=1)
        for b in fw_ota_bin_xz:
            fw_ota_bin_xz_ota.append(b)
        if cpu_type is None or cpu_type == 'Group0':
            fw_ota_path = os.path.join(ota_path, 'FW_OTA.bin.xz.ota')
            fw_ota_path1 = os.path.join(ota_path, 'FW_OTA.bin.hash')
        else:
            fw_ota_path = os.path.join(ota_path, cpu_type + '_OTA.bin.xz.ota')
            fw_ota_path1 = os.path.join(ota_path, cpu_type + '_OTA.bin.hash')
        with open(fw_ota_path, mode='wb') as f:
            f.write(fw_ota_bin_xz_ota)
        with open(fw_ota_path.replace('.ota', '.hash'), mode='wb') as f:
            f.write(fw_ota_bin_xz + img_create_sha256_data(fw_ota_bin_xz))
        with open(fw_ota_path1, mode='wb') as f:
            f.write(fw_ota_bin + img_create_sha256_data(fw_ota_bin))
        return True

    def bl60x_mfg_ota_bin_gen(self, chipname='bl60x', chiptype='bl60x', pt_parcel=None, cpu_type=None, version='', dir_ota=None):
        fw_header_len = 4096
        fw_ota_bin = bytearray()
        pt_fwlen_name = 'fw_len'
        pt_fw1len_name = 'fw1_len'
        if dir_ota:
            ota_path = dir_ota
        else:
            ota_path = os.path.join(chip_path, chipname, 'ota')
        if os.path.isdir(ota_path) is True:
            shutil.rmtree(ota_path)
        if os.path.isdir(ota_path) is False:
            os.mkdir(ota_path)
        if cpu_type is None or cpu_type == 'Group0':
            bootinfo_fw_path = os.path.join(chip_path, chipname, 'img_create_iot', 'bootinfo.bin')
        else:
            bootinfo_fw_path = os.path.join(chip_path, chipname, 'img_create_iot', 'bootinfo_' + cpu_type.lower() + '.bin')
            pt_fwlen_name = 'fw_' + cpu_type.lower() + '_len'
            pt_fw1len_name = 'fw1_' + cpu_type.lower() + '_len'
        with open(bootinfo_fw_path, mode='rb') as f:
            if chiptype == 'bl808':
                fw_header_len = 4096
            file_bytes = f.read(fw_header_len)
            for b in file_bytes:
                fw_ota_bin.append(b)
        i = fw_header_len - len(fw_ota_bin)
        bflb_utils.printf('FW Header is %d, %d still needed' % (len(fw_ota_bin), i))
        while i > 0:
            fw_ota_bin.append(255)
            i = i - 1
        bflb_utils.printf('FW OTA bin header is Done. Len is %d' % len(fw_ota_bin))
        if cpu_type is None or cpu_type == 'Group0':
            img_fw_path = os.path.join(chip_path, chipname, 'img_create_iot', 'img.bin')
        else:
            img_fw_path = os.path.join(chip_path, chipname, 'img_create_iot', 'img_' + cpu_type.lower() + '.bin')
        with open(img_fw_path, mode='rb') as f:
            file_bytes = f.read()
            for b in file_bytes:
                fw_ota_bin.append(b)
        if len(fw_ota_bin) > pt_parcel[pt_fwlen_name]:
            bflb_utils.printf("Error: fw bin size is overflow with partition table, don't create ota bin")
            return False
        if gol.ENABLE_HAIER:
            self.bl60x_mfg_ota_header_haier(fw_ota_bin, chipname, version, dir_ota)
        fw_ota_bin_header = self.bl60x_mfg_ota_header(chipname, fw_ota_bin, use_xz=0)
        if cpu_type is None or cpu_type == 'Group0':
            fw_ota_path = os.path.join(ota_path, 'FW_OTA.bin')
        else:
            fw_ota_path = os.path.join(ota_path, cpu_type + '_OTA.bin')
        with open(fw_ota_path, mode='wb') as f:
            f.write(fw_ota_bin)
        for b in fw_ota_bin:
            fw_ota_bin_header.append(b)
        if cpu_type is None or cpu_type == 'Group0':
            fw_ota_path = os.path.join(ota_path, 'FW_OTA.bin.ota')
        else:
            fw_ota_path = os.path.join(ota_path, cpu_type + '_OTA.bin.ota')
        with open(fw_ota_path, mode='wb') as f:
            f.write(fw_ota_bin_header)
        bflb_utils.printf('FW OTA bin is Done. Len is %d' % len(fw_ota_bin))
        if self.bl60x_mfg_ota_xz_gen(ota_path, chipname, chiptype, cpu_type, pt_parcel[pt_fw1len_name]) == False:
            bflb_utils.printf('Remove OTA directory due to xz image fail')
            shutil.rmtree(ota_path)
        bflb_utils.printf('FW OTA xz is Done')
        return True

    def bl60x_image_gen(self, chipname, chiptype, cpu_type, bintype, raw_bin_name, key=None, iv=None, publickey=None, privarekey=None, cfg_ini=None):
        f = self.bl60x_image_gen_cfg(chipname, chiptype, raw_bin_name, bintype, key, iv, publickey, privarekey, cfg_ini, cpu_type)
        if key or (publickey and privarekey):
            img_cfg = BFConfigParser()
            img_cfg.read(f)
            if chiptype == 'bl60x':
                efusefile = img_cfg.get('Img_CPU0_Cfg', 'efuse_file')
                efusemaskfile = img_cfg.get('Img_CPU0_Cfg', 'efuse_mask_file')
            elif chiptype == 'bl808' or chiptype == 'bl616' or chiptype == 'wb03':
                efusefile = img_cfg.get('Img_Group0_Cfg', 'efuse_file')
                efusemaskfile = img_cfg.get('Img_Group0_Cfg', 'efuse_mask_file')
            else:
                efusefile = img_cfg.get('Img_Cfg', 'efuse_file')
                efusemaskfile = img_cfg.get('Img_Cfg', 'efuse_mask_file')
            cfg = BFConfigParser()
            cfg.read(self.eflash_loader_cfg)
            cfg.set('EFUSE_CFG', 'file', convert_path(os.path.relpath(efusefile, app_path)))
            cfg.set('EFUSE_CFG', 'maskfile', convert_path(os.path.relpath(efusemaskfile, app_path)))
            cfg.write(self.eflash_loader_cfg, 'w')
            self.efuse_load_en = True
        else:
            self.efuse_load_en = False
        return img_create.create_sp_media_image_file(f, chiptype, cpu_type)

    def bl60x_mfg_flasher_cfg(self, uart, baudrate='57600', cfg_ini=None):
        cfg = BFConfigParser()
        if cfg_ini in [None, '']:
            f = self.eflash_loader_cfg
        else:
            f = cfg_ini
        cfg.read(f)
        cfg.set('LOAD_CFG', 'interface', 'uart')
        cfg.set('LOAD_CFG', 'device', uart)
        cfg.set('LOAD_CFG', 'speed_uart_load', baudrate)
        cfg.write(f, 'w')

    def bl60x_mfg_flasher_jlink_cfg(self, rate='1000', cfg_ini=None):
        cfg = BFConfigParser()
        if cfg_ini in [None, '']:
            f = self.eflash_loader_cfg
        else:
            f = cfg_ini
        cfg.read(f)
        cfg.set('LOAD_CFG', 'interface', 'jlink')
        cfg.set('LOAD_CFG', 'speed_jlink', rate)
        cfg.write(f, 'w')

    def bl60x_mfg_flasher_cklink_cfg(self, rate='1000', cfg_ini=None):
        cfg = BFConfigParser()
        if cfg_ini in [None, '']:
            f = self.eflash_loader_cfg
        else:
            f = cfg_ini
        cfg.read(f)
        cfg.set('LOAD_CFG', 'interface', 'cklink')
        cfg.set('LOAD_CFG', 'speed_jlink', rate)
        cfg.write(f, 'w')

    def bl60x_mfg_flasher_openocd_cfg(self, rate='8000', cfg_ini=None):
        cfg = BFConfigParser()
        if cfg_ini in [None, '']:
            f = self.eflash_loader_cfg
        else:
            f = cfg_ini
        cfg.read(f)
        cfg.set('LOAD_CFG', 'interface', 'openocd')
        cfg.set('LOAD_CFG', 'speed_jlink', rate)
        cfg.write(f, 'w')

    def bl60x_mfg_flasher_erase_all(self, erase, cfg_ini=None):
        cfg = BFConfigParser()
        if cfg_ini in [None, '']:
            f = self.eflash_loader_cfg
        else:
            f = cfg_ini
        if self.chiptype == 'bl60x' or self.chiptype == 'bl602' or self.chiptype == 'bl702':
            cfg.read(f)
            if erase is True:
                cfg.set('LOAD_CFG', 'erase', '2')
            else:
                cfg.set('LOAD_CFG', 'erase', '1')
            cfg.write(f, 'w')

    def bl_write_flash_img(self, d_addrs, d_files, flash_size):
        whole_img_len = bl_get_largest_addr(d_addrs, d_files)
        whole_img_data = bl_create_flash_default_data(whole_img_len)
        whole_img_file = os.path.join(chip_path, self.chipname, 'img_create_iot', 'whole_flash_data.bin')
        filedatas = bl_get_file_data(d_files)
        for i in range(len(d_addrs)):
            start_addr = int(d_addrs[i], 16)
            whole_img_data[start_addr:start_addr + len(filedatas[i])] = filedatas[i]
        fp = open(whole_img_file, 'wb+')
        fp.write(whole_img_data)
        fp.close()

    def bl60x_mfg_flasher_eflash_loader_cfg(self, chipname, chiptype, boot2, pt_parcel, bin_d_list, name_list, flash_opt='1M'):
        bflb_utils.printf('========= eflash loader config =========')
        d_files = []
        d_addrs = []
        bind_bootinfo = True
        chipnamedir = os.path.join(chip_path, chipname)
        if pt_parcel is None:
            bflb_utils.set_error_code('007B')
            return bflb_utils.errorcode_msg()
        if boot2 is True:
            if bind_bootinfo is True:
                if 'boot2_header' not in pt_parcel or pt_parcel['boot2_header'] == 1:
                    whole_img = chipnamedir + '/img_create_iot/whole_img_boot2.bin'
                    whole_img_len = 8192 + os.path.getsize(chipnamedir + '/img_create_iot/img_boot2.bin')
                    whole_img_data = bl_create_flash_default_data(whole_img_len)
                    filedata = bl_get_file_data(['chips/' + chipname + '/img_create_iot/bootinfo_boot2.bin'])[0]
                    whole_img_data[0:len(filedata)] = filedata
                    filedata = bl_get_file_data(['chips/' + chipname + '/img_create_iot/img_boot2.bin'])[0]
                    whole_img_data[8192:8192 + len(filedata)] = filedata
                    fp = open(whole_img, 'wb+')
                    fp.write(whole_img_data)
                    fp.close()
                    d_files.append('chips/' + chipname + '/img_create_iot/whole_img_boot2.bin')
                    d_addrs.append('00000000')
                elif 'boot2_header' in pt_parcel and (not pt_parcel['boot2_header']):
                    if 'boot2_addr' in pt_parcel:
                        d_files.append('chips/' + chipname + '/img_create_iot/boot2.bin')
                        d_addrs.append('00000000')
                    else:
                        bflb_utils.printf('Error: boot2 is not in partition table')
            else:
                d_files.append('chips/' + chipname + '/img_create_iot/bootinfo_boot2.bin')
                d_addrs.append('00000000')
                d_files.append('chips/' + chipname + '/img_create_iot/img_boot2.bin')
                d_addrs.append('00002000')
        elif chiptype == 'bl702':
            bflb_utils.printf('========= copy bootinfo_boot2.bin =========')
            bflb_utils.copyfile(chipnamedir + '/img_create_iot/bootinfo.bin', chipnamedir + '/img_create_iot/bootinfo_boot2.bin')
            d_files.append('chips/' + chipname + '/img_create_iot/bootinfo_boot2.bin')
            d_addrs.append('00000000')
        if pt_parcel is not None and len(pt_parcel) > 0 and (pt_parcel['pt_new'] is True):
            d_files.append('chips/' + chipname + '/partition/partition.bin')
            d_addrs.append(hex(pt_parcel['pt_addr0'])[2:])
            d_files.append('chips/' + chipname + '/partition/partition.bin')
            d_addrs.append(hex(pt_parcel['pt_addr1'])[2:])
        for i in range(len(name_list)):
            name = name_list[i].lower().replace(' ', '_')
            if name == 'boot2':
                continue
            elif name == 'factory':
                if bin_d_list[i] is not None and len(bin_d_list[i]) > 0:
                    if 'factory_addr' in pt_parcel:
                        bl_ro_device_tree.bl_ro_params_device_tree(bin_d_list[i], chipnamedir + '/device_tree/ro_params.dtb')
                        d_files.append('chips/' + chipname + '/device_tree/ro_params.dtb')
                        d_addrs.append(hex(pt_parcel['factory_addr'])[2:])
                    else:
                        bflb_utils.printf('Warning: factory is not in partition table')
                continue
            if bin_d_list[i]:
                if pt_parcel[name + '_header'] == 1:
                    if name + '_addr' in pt_parcel:
                        offset = 4096
                        if chiptype == 'bl808':
                            offset = 4096
                        if bind_bootinfo is True:
                            if name == 'fw':
                                whole_img = chipnamedir + '/img_create_iot/whole_img.bin'
                                whole_img_len = offset + os.path.getsize(chipnamedir + '/img_create_iot/img.bin')
                                whole_img_data = bl_create_flash_default_data(whole_img_len)
                                filedata = bl_get_file_data(['chips/' + chipname + '/img_create_iot/bootinfo.bin'])[0]
                                whole_img_data[0:len(filedata)] = filedata
                                filedata = bl_get_file_data(['chips/' + chipname + '/img_create_iot/img.bin'])[0]
                                whole_img_data[offset:offset + len(filedata)] = filedata
                                fp = open(whole_img, 'wb+')
                                fp.write(whole_img_data)
                                fp.close()
                                d_files.append('chips/' + chipname + '/img_create_iot/whole_img.bin')
                            else:
                                whole_img = chipnamedir + '/img_create_iot/whole_img_' + name + '.bin'
                                whole_img_len = offset + os.path.getsize(chipnamedir + '/img_create_iot/img_' + name + '.bin')
                                whole_img_data = bl_create_flash_default_data(whole_img_len)
                                filedata = bl_get_file_data(['chips/' + chipname + '/img_create_iot/bootinfo_' + name + '.bin'])[0]
                                whole_img_data[0:len(filedata)] = filedata
                                filedata = bl_get_file_data(['chips/' + chipname + '/img_create_iot/img_' + name + '.bin'])[0]
                                whole_img_data[offset:offset + len(filedata)] = filedata
                                fp = open(whole_img, 'wb+')
                                fp.write(whole_img_data)
                                fp.close()
                                d_files.append('chips/' + chipname + '/img_create_iot/whole_img_' + name + '.bin')
                            d_addrs.append(hex(pt_parcel[name + '_addr'])[2:])
                        else:
                            d_files.append('chips/' + chipname + '/img_create_iot/bootinfo_' + name + '.bin')
                            d_addrs.append(hex(pt_parcel[name + '_addr'])[2:])
                            d_files.append('chips/' + chipname + '/img_create_iot/img_' + name + '.bin')
                            d_addrs.append(hex(pt_parcel[name + '_addr'] + offset)[2:])
                    else:
                        bflb_utils.printf('Error: FW/FW_CPU0/FW_GRP0 is not in partition table')
                elif name + '_addr' in pt_parcel:
                    d_files.append('chips/' + chipname + '/img_create_iot/' + name + '.bin')
                    d_addrs.append(hex(pt_parcel[name + '_addr'])[2:])
                else:
                    bflb_utils.printf('Error: %s is not in partition table' % name)
        if len(d_files) > 0 and len(d_addrs) > 0:
            if check_pt_table(pt_parcel, d_files, name_list) != True:
                bflb_utils.set_error_code('0082')
                return bflb_utils.errorcode_msg()
            cfg = BFConfigParser()
            cfg.read(self.eflash_loader_cfg)
            self.bl_write_flash_img(d_addrs, d_files, flash_opt)
            files_str = ' '.join(d_files)
            addrs_str = ' '.join(d_addrs)
            cfg.set('FLASH_CFG', 'file', files_str)
            cfg.set('FLASH_CFG', 'address', addrs_str)
            cfg.write(self.eflash_loader_cfg, 'w')
            ret = img_create.compress_dir(chipname, 'img_create_iot', self.efuse_load_en)
            if ret is not True:
                return bflb_utils.errorcode_msg()
            return True
        else:
            bflb_utils.set_error_code('0060')
            return bflb_utils.errorcode_msg()

    def bl60x_mfg_flasher_eflash_loader_cfg_old(self, chipname, chiptype, bin_file, boot2, ro_params, pt_parcel, media, mfg, d0fw=False, imtb=False, kv=False, yocboot=False, dtb=False, flash_opt='1M'):
        bflb_utils.printf('========= eflash loader config =========')
        d_files = []
        d_addrs = []
        bind_bootinfo = True
        chipnamedir = os.path.join(chip_path, chipname)
        if pt_parcel is None:
            bflb_utils.set_error_code('007B')
            return bflb_utils.errorcode_msg()
        if boot2 is True:
            if bind_bootinfo is True:
                whole_img = chipnamedir + '/img_create_iot/whole_img_boot2.bin'
                whole_img_len = 8192 + os.path.getsize(chipnamedir + '/img_create_iot/img_boot2.bin')
                whole_img_data = bl_create_flash_default_data(whole_img_len)
                filedata = bl_get_file_data(['chips/' + chipname + '/img_create_iot/bootinfo_boot2.bin'])[0]
                whole_img_data[0:len(filedata)] = filedata
                filedata = bl_get_file_data(['chips/' + chipname + '/img_create_iot/img_boot2.bin'])[0]
                whole_img_data[8192:8192 + len(filedata)] = filedata
                fp = open(whole_img, 'wb+')
                fp.write(whole_img_data)
                fp.close()
                d_files.append('chips/' + chipname + '/img_create_iot/whole_img_boot2.bin')
                d_addrs.append('00000000')
            else:
                d_files.append('chips/' + chipname + '/img_create_iot/bootinfo_boot2.bin')
                d_addrs.append('00000000')
                d_files.append('chips/' + chipname + '/img_create_iot/img_boot2.bin')
                d_addrs.append('00002000')
        elif chiptype == 'bl702':
            bflb_utils.printf('========= copy bootinfo_boot2.bin =========')
            bflb_utils.copyfile(chipnamedir + '/img_create_iot/bootinfo.bin', chipnamedir + '/img_create_iot/bootinfo_boot2.bin')
            d_files.append('chips/' + chipname + '/img_create_iot/bootinfo_boot2.bin')
            d_addrs.append('00000000')
        if pt_parcel is not None and len(pt_parcel) > 0 and (pt_parcel['pt_new'] is True):
            d_files.append('chips/' + chipname + '/partition/partition.bin')
            d_addrs.append(hex(pt_parcel['pt_addr0'])[2:])
            d_files.append('chips/' + chipname + '/partition/partition.bin')
            d_addrs.append(hex(pt_parcel['pt_addr1'])[2:])
        if bin_file is True:
            if 'fw_cpu0_addr' in pt_parcel:
                if bind_bootinfo is True:
                    whole_img = chipnamedir + '/img_create_iot/whole_img_cpu0.bin'
                    whole_img_len = 4096 + os.path.getsize(chipnamedir + '/img_create_iot/img_cpu0.bin')
                    whole_img_data = bl_create_flash_default_data(whole_img_len)
                    filedata = bl_get_file_data(['chips/' + chipname + '/img_create_iot/bootinfo_cpu0.bin'])[0]
                    whole_img_data[0:len(filedata)] = filedata
                    filedata = bl_get_file_data(['chips/' + chipname + '/img_create_iot/img_cpu0.bin'])[0]
                    whole_img_data[4096:4096 + len(filedata)] = filedata
                    fp = open(whole_img, 'wb+')
                    fp.write(whole_img_data)
                    fp.close()
                    d_files.append('chips/' + chipname + '/img_create_iot/whole_img_cpu0.bin')
                    d_addrs.append(hex(pt_parcel['fw_cpu0_addr'])[2:])
                else:
                    d_files.append('chips/' + chipname + '/img_create_iot/bootinfo_cpu0.bin')
                    d_addrs.append(hex(pt_parcel['fw_cpu0_addr'])[2:])
                    d_files.append('chips/' + chipname + '/img_create_iot/img_cpu0.bin')
                    d_addrs.append(hex(pt_parcel['fw_cpu0_addr'] + 4096)[2:])
            elif 'fw_group0_addr' in pt_parcel:
                if bind_bootinfo is True:
                    whole_img = chipnamedir + '/img_create_iot/whole_img_group0.bin'
                    whole_img_len = 8192 + os.path.getsize(chipnamedir + '/img_create_iot/img_group0.bin')
                    whole_img_data = bl_create_flash_default_data(whole_img_len)
                    filedata = bl_get_file_data(['chips/' + chipname + '/img_create_iot/bootinfo_group0.bin'])[0]
                    whole_img_data[0:len(filedata)] = filedata
                    filedata = bl_get_file_data(['chips/' + chipname + '/img_create_iot/img_group0.bin'])[0]
                    whole_img_data[8192:8192 + len(filedata)] = filedata
                    fp = open(whole_img, 'wb+')
                    fp.write(whole_img_data)
                    fp.close()
                    d_files.append('chips/' + chipname + '/img_create_iot/whole_img_group0.bin')
                    d_addrs.append(hex(pt_parcel['fw_group0_addr'])[2:])
                else:
                    d_files.append('chips/' + chipname + '/img_create_iot/bootinfo_group0.bin')
                    d_addrs.append(hex(pt_parcel['fw_group0_addr'])[2:])
                    d_files.append('chips/' + chipname + '/img_create_iot/img_group0.bin')
                    d_addrs.append(hex(pt_parcel['fw_group0_addr'] + 8192)[2:])
            elif 'fw_addr' in pt_parcel:
                offset = 4096
                if chiptype == 'bl808':
                    offset = 4096
                if bind_bootinfo is True:
                    whole_img = chipnamedir + '/img_create_iot/whole_img.bin'
                    whole_img_len = offset + os.path.getsize(chipnamedir + '/img_create_iot/img.bin')
                    whole_img_data = bl_create_flash_default_data(whole_img_len)
                    filedata = bl_get_file_data(['chips/' + chipname + '/img_create_iot/bootinfo.bin'])[0]
                    whole_img_data[0:len(filedata)] = filedata
                    filedata = bl_get_file_data(['chips/' + chipname + '/img_create_iot/img.bin'])[0]
                    whole_img_data[offset:offset + len(filedata)] = filedata
                    fp = open(whole_img, 'wb+')
                    fp.write(whole_img_data)
                    fp.close()
                    d_files.append('chips/' + chipname + '/img_create_iot/whole_img.bin')
                    d_addrs.append(hex(pt_parcel['fw_addr'])[2:])
                else:
                    d_files.append('chips/' + chipname + '/img_create_iot/bootinfo.bin')
                    d_addrs.append(hex(pt_parcel['fw_addr'])[2:])
                    d_files.append('chips/' + chipname + '/img_create_iot/img.bin')
                    d_addrs.append(hex(pt_parcel['fw_addr'] + offset)[2:])
            else:
                bflb_utils.printf('Error: FW/FW_CPU0/FW_GRP0 is not in partition table')
        if d0fw is True:
            if 'fw_d0_addr' in pt_parcel:
                offset = 4096
                if chiptype == 'bl808':
                    offset = 4096
                if bind_bootinfo is True:
                    whole_img = chipnamedir + '/img_create_iot/whole_img_d0fw.bin'
                    whole_img_len = offset + os.path.getsize(chipnamedir + '/img_create_iot/img_d0fw.bin')
                    whole_img_data = bl_create_flash_default_data(whole_img_len)
                    filedata = bl_get_file_data(['chips/' + chipname + '/img_create_iot/bootinfo_d0fw.bin'])[0]
                    whole_img_data[0:len(filedata)] = filedata
                    filedata = bl_get_file_data(['chips/' + chipname + '/img_create_iot/img_d0fw.bin'])[0]
                    whole_img_data[offset:offset + len(filedata)] = filedata
                    fp = open(whole_img, 'wb+')
                    fp.write(whole_img_data)
                    fp.close()
                    d_files.append('chips/' + chipname + '/img_create_iot/whole_img_d0fw.bin')
                    d_addrs.append(hex(pt_parcel['fw_d0_addr'])[2:])
                else:
                    d_files.append('chips/' + chipname + '/img_create_iot/bootinfo_d0fw.bin')
                    d_addrs.append(hex(pt_parcel['fw_d0_addr'])[2:])
                    d_files.append('chips/' + chipname + '/img_create_iot/img_d0fw.bin')
                    d_addrs.append(hex(pt_parcel['fw_d0_addr'] + offset)[2:])
            else:
                bflb_utils.printf('Error: D0FW is not in partition table')
        if yocboot is True:
            if 'fw_yocboot_addr' in pt_parcel:
                offset = 4096
                if chiptype == 'bl808':
                    offset = 4096
                if bind_bootinfo is True:
                    whole_img = chipnamedir + '/img_create_iot/whole_img_yocboot.bin'
                    whole_img_len = offset + os.path.getsize(chipnamedir + '/img_create_iot/img_yocboot.bin')
                    whole_img_data = bl_create_flash_default_data(whole_img_len)
                    filedata = bl_get_file_data(['chips/' + chipname + '/img_create_iot/bootinfo_yocboot.bin'])[0]
                    whole_img_data[0:len(filedata)] = filedata
                    filedata = bl_get_file_data(['chips/' + chipname + '/img_create_iot/img_yocboot.bin'])[0]
                    whole_img_data[offset:offset + len(filedata)] = filedata
                    fp = open(whole_img, 'wb+')
                    fp.write(whole_img_data)
                    fp.close()
                    d_files.append('chips/' + chipname + '/img_create_iot/whole_img_yocboot.bin')
                    d_addrs.append(hex(pt_parcel['fw_yocboot_addr'])[2:])
                else:
                    d_files.append('chips/' + chipname + '/img_create_iot/bootinfo_yocboot.bin')
                    d_addrs.append(hex(pt_parcel['fw_yocboot_addr'])[2:])
                    d_files.append('chips/' + chipname + '/img_create_iot/img_yocboot.bin')
                    d_addrs.append(hex(pt_parcel['fw_yocboot_addr'] + offset)[2:])
            else:
                bflb_utils.printf('Error: yocboot is not in partition table')
        if dtb is True:
            if 'dtb_addr' in pt_parcel:
                offset = 4096
                if chiptype == 'bl808':
                    offset = 4096
                if bind_bootinfo is True:
                    whole_img = chipnamedir + '/img_create_iot/whole_img_dtb.bin'
                    whole_img_len = offset + os.path.getsize(chipnamedir + '/img_create_iot/img_dtb.bin')
                    whole_img_data = bl_create_flash_default_data(whole_img_len)
                    filedata = bl_get_file_data(['chips/' + chipname + '/img_create_iot/bootinfo_dtb.bin'])[0]
                    whole_img_data[0:len(filedata)] = filedata
                    filedata = bl_get_file_data(['chips/' + chipname + '/img_create_iot/img_dtb.bin'])[0]
                    whole_img_data[offset:offset + len(filedata)] = filedata
                    fp = open(whole_img, 'wb+')
                    fp.write(whole_img_data)
                    fp.close()
                    d_files.append('chips/' + chipname + '/img_create_iot/whole_img_dtb.bin')
                    d_addrs.append(hex(pt_parcel['dtb_addr'])[2:])
                else:
                    d_files.append('chips/' + chipname + '/img_create_iot/bootinfo_dtb.bin')
                    d_addrs.append(hex(pt_parcel['dtb_addr'])[2:])
                    d_files.append('chips/' + chipname + '/img_create_iot/img_dtb.bin')
                    d_addrs.append(hex(pt_parcel['dtb_addr'] + offset)[2:])
            else:
                bflb_utils.printf('Error: dtb is not in partition table')
        if imtb is True:
            if 'imtb_addr' in pt_parcel:
                d_files.append('chips/' + chipname + '/img_create_iot/imtb.bin')
                d_addrs.append(hex(pt_parcel['imtb_addr'])[2:])
            else:
                bflb_utils.printf('Error: imtb is not in partition table')
        if kv is True:
            if 'kv_addr' in pt_parcel:
                d_files.append('chips/' + chipname + '/img_create_iot/kv.bin')
                d_addrs.append(hex(pt_parcel['kv_addr'])[2:])
            else:
                bflb_utils.printf('Error: kv is not in partition table')
        if ro_params is not None and len(ro_params) > 0:
            if 'conf_addr' in pt_parcel:
                bl_ro_device_tree.bl_ro_params_device_tree(ro_params, chipnamedir + '/device_tree/ro_params.dtb')
                d_files.append('chips/' + chipname + '/device_tree/ro_params.dtb')
                d_addrs.append(hex(pt_parcel['conf_addr'])[2:])
            else:
                bflb_utils.printf('Error: factory is not in partition table')
        if media is True:
            if 'media_addr' in pt_parcel:
                d_files.append('chips/' + chipname + '/img_create_iot/media.bin')
                d_addrs.append(hex(pt_parcel['media_addr'])[2:])
            else:
                bflb_utils.printf('Error: media is not in partition table')
        if mfg is True:
            if 'mfg_addr' in pt_parcel:
                offset = 4096
                if chiptype == 'bl808':
                    offset = 4096
                if bind_bootinfo is True:
                    whole_img = chipnamedir + '/img_create_iot/whole_img_mfg.bin'
                    whole_img_len = offset + os.path.getsize(chipnamedir + '/img_create_iot/img_mfg.bin')
                    whole_img_data = bl_create_flash_default_data(whole_img_len)
                    filedata = bl_get_file_data(['chips/' + chipname + '/img_create_iot/bootinfo_mfg.bin'])[0]
                    whole_img_data[0:len(filedata)] = filedata
                    filedata = bl_get_file_data(['chips/' + chipname + '/img_create_iot/img_mfg.bin'])[0]
                    whole_img_data[offset:offset + len(filedata)] = filedata
                    fp = open(whole_img, 'wb+')
                    fp.write(whole_img_data)
                    fp.close()
                    d_files.append('chips/' + chipname + '/img_create_iot/whole_img_mfg.bin')
                    d_addrs.append(hex(pt_parcel['mfg_addr'])[2:])
                else:
                    d_files.append('chips/' + chipname + '/img_create_iot/bootinfo_mfg.bin')
                    d_addrs.append(hex(pt_parcel['mfg_addr'])[2:])
                    d_files.append('chips/' + chipname + '/img_create_iot/img_mfg.bin')
                    d_addrs.append(hex(pt_parcel['mfg_addr'] + offset)[2:])
            else:
                bflb_utils.printf('Error: mfg is not in partition table')
        if len(d_files) > 0 and len(d_addrs) > 0:
            if check_pt_table_old(pt_parcel, d_files) != True:
                bflb_utils.set_error_code('0082')
                return bflb_utils.errorcode_msg()
            cfg = BFConfigParser()
            cfg.read(self.eflash_loader_cfg)
            self.bl_write_flash_img(d_addrs, d_files, flash_opt)
            files_str = ' '.join(d_files)
            addrs_str = ' '.join(d_addrs)
            cfg.set('FLASH_CFG', 'file', files_str)
            cfg.set('FLASH_CFG', 'address', addrs_str)
            cfg.write(self.eflash_loader_cfg, 'w')
            ret = img_create.compress_dir(chipname, 'img_create_iot', self.efuse_load_en)
            if ret is not True:
                return bflb_utils.errorcode_msg()
            return True
        else:
            bflb_utils.set_error_code('0060')
            return bflb_utils.errorcode_msg()

    def bl60x_mfg_uart_flasher(self, uart, baudrate='57600', cfg_ini=None):
        self.bl60x_mfg_flasher_cfg(uart, baudrate, cfg_ini)
        exe_genitor(['python', os.path.join(chip_path, 'libs/bflb_eflash_loader.py'), '--write', '--flash', '-c', self.eflash_loader_cfg])

    def flasher_download_cfg_ini_gen(self, chipname, chiptype, cpu_type, config):
        bin_d = False
        boot2_d = False
        ro_params_d = None
        pt_parcel = None
        media_bin_d = False
        mfg_bin_d = False
        d0_bin_d = False
        imtb_bin_d = False
        kv_bin_d = False
        yocboot_bin_d = False
        dtb_bin_d = False
        boot2_en = False
        dts_bytearray = None
        bin_d_list = []
        partition_path = os.path.join(chip_path, chipname, 'partition/partition.bin')
        error = 'Please check your partition table file'
        self.config = config
        if chiptype == 'bl702':
            if 'boot2_download' in config['check_box'] and config['check_box']['boot2_download'] is True:
                boot2_en = False
            else:
                boot2_en = True
        cfg = BFConfigParser()
        cfg.read(self.eflash_loader_cfg)
        if cfg.has_option('FLASH_CFG', 'flash_id'):
            flash_id = cfg.get('FLASH_CFG', 'flash_id')
            bflb_utils.printf('========= chip flash id: %s =========' % flash_id)
            if chiptype == 'bl602' or chiptype == 'bl702':
                if bflb_flash_select.update_flash_cfg(chipname, chiptype, flash_id, self.bh_cfg_file, False, 'BOOTHEADER_CFG') is False:
                    error = 'flash_id:' + flash_id + ' do not support'
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code('0069')
                    return bflb_utils.errorcode_msg()
            elif chiptype == 'bl60x':
                if bflb_flash_select.update_flash_cfg(chipname, chiptype, flash_id, self.bh_cfg_file, False, 'BOOTHEADER_CPU0_CFG') is False:
                    error = 'flash_id:' + flash_id + ' do not support'
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code('0069')
                    return bflb_utils.errorcode_msg()
            elif chiptype == 'bl808' or chiptype == 'bl616':
                if bflb_flash_select.update_flash_cfg(chipname, chiptype, flash_id, self.bh_cfg_file, False, 'BOOTHEADER_GROUP0_CFG') is False:
                    error = 'flash_id:' + flash_id + ' do not support'
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code('0069')
                    return bflb_utils.errorcode_msg()
        else:
            error = 'Do not find flash_id in eflash_loader_cfg.ini'
            bflb_utils.printf(error)
            bflb_utils.set_error_code('0070')
            return bflb_utils.errorcode_msg()
        if 'factory_download' in config['check_box'] and config['check_box']['factory_download'] is True:
            ro = config['input_path']['factory_bin_input']
            if not os.path.isfile(ro):
                bflb_utils.printf("Don't Find %s as bl_factory image" % ro)
                error = "Don't Find %s as bl_factory image" % ro
                bflb_utils.printf(error)
                bflb_utils.set_error_code('0079')
                return bflb_utils.errorcode_msg()
            if ro is not None and len(ro) > 0:
                ro_params_d = ro
                try:
                    dts_hex = bl_ro_device_tree.bl_dts2hex(ro_params_d)
                    dts_bytearray = bflb_utils.hexstr_to_bytearray(dts_hex)
                except Exception as e:
                    dts_bytearray = None
        if 'pt_table_bin_input' in config['input_path']:
            pt = config['input_path']['pt_table_bin_input']
            if pt is not None and len(pt) > 0:
                pt_helper = partition.PtCreater(pt)
                if config['check_box']['pt_table_download'] is True:
                    bflb_utils.printf('create partition.bin, pt_new is True')
                    pt_helper.create_pt_table(partition_path)
                (pt_parcel, name_list) = pt_helper.construct_table()
                bin_d_list = [False for i in range(len(name_list))]
                if chiptype == 'bl702':
                    cfg_t = BFConfigParser()
                    cfg_t.read(self.bh_cfg_file)
                    cfg_t.set('BOOTHEADER_CFG', 'boot2_pt_table_0', '0x%X' % pt_parcel['pt_addr0'])
                    cfg_t.set('BOOTHEADER_CFG', 'boot2_pt_table_1', '0x%X' % pt_parcel['pt_addr1'])
                    cfg_t.write(self.bh_cfg_file)
            else:
                bflb_utils.set_error_code('0076')
                return bflb_utils.errorcode_msg()
        if 'pt_bin_input' in config['input_path']:
            pt = config['input_path']['pt_bin_input']
            if pt is not None and len(pt) > 0:
                pt_helper = partition.PtCreater(pt)
                if config['check_box']['partition_download'] is True:
                    bflb_utils.printf('create partition.bin, pt_new is True')
                    pt_helper.create_pt_table(partition_path)
                (pt_parcel, name_list) = pt_helper.construct_table()
                bin_d_list = [False for i in range(len(name_list))]
                if chiptype == 'bl702':
                    cfg_t = BFConfigParser()
                    cfg_t.read(self.bh_cfg_file)
                    cfg_t.set('BOOTHEADER_CFG', 'boot2_pt_table_0', '0x%X' % pt_parcel['pt_addr0'])
                    cfg_t.set('BOOTHEADER_CFG', 'boot2_pt_table_1', '0x%X' % pt_parcel['pt_addr1'])
                    cfg_t.write(self.bh_cfg_file)
            else:
                bflb_utils.set_error_code('0076')
                return bflb_utils.errorcode_msg()
        if 'factory' in config['check_box'] and config['check_box']['factory'] is True:
            ro = config['input_path']['dts_input']
            if not os.path.isfile(ro):
                bflb_utils.printf("Don't Find %s as bl_factory image" % ro)
                error = "Don't Find %s as bl_factory image" % ro
                bflb_utils.printf(error)
                bflb_utils.set_error_code('0079')
                return bflb_utils.errorcode_msg()
            if ro is not None and len(ro) > 0:
                ro_params_d = ro
                try:
                    dts_hex = bl_ro_device_tree.bl_dts2hex(ro_params_d)
                    dts_bytearray = bflb_utils.hexstr_to_bytearray(dts_hex)
                except Exception as e:
                    dts_bytearray = None
        if config['check_box']['encrypt'] is True:
            aes_key = config['param']['aes_key'].replace(' ', '')
            aes_iv = config['param']['aes_iv'].replace(' ', '')
            if verify_hex_num(aes_key) is not True or len(aes_key) != 32:
                error = 'Error: Please check AES key data and len'
                bflb_utils.printf(error)
                bflb_utils.set_error_code('0077')
                return bflb_utils.errorcode_msg()
            if verify_hex_num(aes_iv) is not True or len(aes_iv) != 32:
                error = 'Error: Please check AES iv data and len'
                bflb_utils.printf(error)
                bflb_utils.set_error_code('0078')
                return bflb_utils.errorcode_msg()
            if aes_iv.endswith('00000000') is False:
                error = 'AES IV should endswith 4 bytes zero'
                bflb_utils.printf(error)
                bflb_utils.set_error_code('0073')
                return bflb_utils.errorcode_msg()
        if config['check_box']['sign'] is True:
            if not config['input_path']['publickey']:
                error = 'Please set public key'
                bflb_utils.printf(error)
                bflb_utils.set_error_code('0066')
                return bflb_utils.errorcode_msg()
            if not config['input_path']['privatekey']:
                error = 'Please set private key'
                bflb_utils.printf(error)
                bflb_utils.set_error_code('0067')
                return bflb_utils.errorcode_msg()
        cfg_t = BFConfigParser()
        cfg_t.read(self.bh_cfg_file)
        if 'BOOTHEADER_CPU0_CFG' in cfg_t.sections():
            bootheader_section_name = 'BOOTHEADER_CPU0_CFG'
        elif 'BOOTHEADER_GROUP0_CFG' in cfg_t.sections():
            bootheader_section_name = 'BOOTHEADER_GROUP0_CFG'
        else:
            bootheader_section_name = 'BOOTHEADER_CFG'
        crc_ignore = cfg_t.get(bootheader_section_name, 'crc_ignore')
        hash_ignore = cfg_t.get(bootheader_section_name, 'hash_ignore')
        cfg_t.set(bootheader_section_name, 'crc_ignore', 1)
        cfg_t.set(bootheader_section_name, 'hash_ignore', 1)
        cfg_t.write(self.bh_cfg_file)
        if 'boot2_download' in config['check_box'] and config['check_box']['boot2_download'] is True:
            if 'boot2_header' not in pt_parcel:
                if chiptype == 'bl808':
                    boot2 = '%s|UNUSED|UNUSED|' % config['input_path']['boot2_bin_input']
                else:
                    boot2 = config['input_path']['boot2_bin_input']
                if boot2 is not None and len(boot2) > 0:
                    self.bl60x_fw_boot_head_gen(True, config['param']['chip_xtal'], self.bh_cfg_file, config['check_box']['encrypt'], config['check_box']['sign'], chipname, chiptype, cpu_type, boot2_en)
                    f_org = os.path.join(chip_path, chipname, 'img_create_iot', 'img_create_cfg_boot2.conf')
                    f = os.path.join(chip_path, chipname, 'img_create_iot', 'img_create_cfg_boot2.ini')
                    if os.path.isfile(f) is False:
                        shutil.copyfile(f_org, f)
                    self.bl60x_image_gen(chipname, chiptype, cpu_type, 'boot2', boot2, config['param']['aes_key'], config['param']['aes_iv'], config['input_path']['publickey'], config['input_path']['privatekey'], f)
                    boot2_d = True
            elif 'boot2_header' in pt_parcel and (not pt_parcel['boot2_header']):
                if 'boot2_bin_input' in config['input_path']:
                    temp_bin = config['input_path']['boot2_bin_input']
                    if temp_bin is not None and len(temp_bin) > 0:
                        try:
                            shutil.copyfile(temp_bin, os.path.join(chip_path, chipname, 'img_create_iot', 'boot2.bin'))
                        except Exception as e:
                            bflb_utils.printf(e)
                    boot2_d = True
            elif pt_parcel['boot2_header'] == 1:
                if chiptype == 'bl808':
                    boot2 = '%s|UNUSED|UNUSED|' % config['input_path']['boot2_bin_input']
                else:
                    boot2 = config['input_path']['boot2_bin_input']
                if boot2 is not None and len(boot2) > 0:
                    temp_aes_key = None
                    temp_aes_iv = None
                    temp_publickey = None
                    temp_privatekey = None
                    temp_encrypt = 0
                    temp_sign = 0
                    if 'boot2_security' in pt_parcel:
                        if pt_parcel['boot2_security'] == 1:
                            temp_aes_key = config['param']['aes_key']
                            temp_aes_iv = config['param']['aes_iv']
                            temp_publickey = config['input_path']['publickey']
                            temp_privatekey = config['input_path']['privatekey']
                            if config['check_box']['encrypt']:
                                temp_encrypt = config['check_box']['encrypt']
                            if config['check_box']['sign']:
                                temp_sign = config['check_box']['sign']
                    self.bl60x_fw_boot_head_gen(True, config['param']['chip_xtal'], self.bh_cfg_file, temp_encrypt, temp_sign, chipname, chiptype, cpu_type, boot2_en)
                    f_org = os.path.join(chip_path, chipname, 'img_create_iot', 'img_create_cfg_boot2.conf')
                    f = os.path.join(chip_path, chipname, 'img_create_iot', 'img_create_cfg_boot2.ini')
                    if os.path.isfile(f) is False:
                        shutil.copyfile(f_org, f)
                    self.bl60x_image_gen(chipname, chiptype, cpu_type, 'boot2', boot2, temp_aes_key, temp_aes_iv, temp_publickey, temp_privatekey, f)
                    boot2_d = True
        elif chiptype == 'bl702':
            self.bl60x_fw_boot_head_gen(True, config['param']['chip_xtal'], self.bh_cfg_file, config['check_box']['encrypt'], config['check_box']['sign'], chipname, chiptype, cpu_type, boot2_en)
        cfg_t = BFConfigParser()
        cfg_t.read(self.bh_cfg_file)
        cfg_t.set(bootheader_section_name, 'crc_ignore', crc_ignore)
        cfg_t.set(bootheader_section_name, 'hash_ignore', hash_ignore)
        cfg_t.write(self.bh_cfg_file)
        if 'version' in pt_parcel and pt_parcel['version'] == 2:
            for i in range(len(name_list)):
                name = name_list[i].replace(' ', '_').lower()
                if name == 'boot2':
                    bin_d_list[i] = boot2_d
                    continue
                elif name == 'factory':
                    bin_d_list[i] = ro_params_d
                    continue
                if pt_parcel[name + '_header'] == 1:
                    if name + '_download' in config['check_box'] and name + '_bin_input' in config['input_path']:
                        media_sign = 0
                        if name == 'media':
                            if config['check_box']['media_download'] is True:
                                media_sign = 1
                            elif config['check_box']['romfs_download'] is True:
                                media_sign = 2
                            if config['check_box']['media_download'] is True:
                                media_bin = config['input_path']['media_bin_input']
                                if media_bin is not None and len(media_bin) > 0:
                                    try:
                                        shutil.copyfile(media_bin, os.path.join(chip_path, chipname, 'img_create_iot', 'media.bin'))
                                    except Exception as e:
                                        bflb_utils.printf(e)
                            if config['check_box']['romfs_download'] is True:
                                romfs_dir = config['input_path']['romfs_dir_input']
                                if romfs_dir is not None and len(romfs_dir) > 0:
                                    ret = generate_romfs_img(romfs_dir, os.path.join(chip_path, chipname, 'img_create_iot', 'media.bin'))
                                    if ret != 0:
                                        bflb_utils.printf('ERROR, ret %s.' % ret)
                                        error = 'ERROR, ret %s.' % ret
                                        bflb_utils.printf(error)
                                        bflb_utils.set_error_code('007A')
                                        return bflb_utils.errorcode_msg()
                        if media_sign == 1 or media_sign == 2 or config['check_box'][name + '_download'] is True:
                            if name + '_addr' in pt_parcel:
                                if chiptype == 'bl808':
                                    if media_sign == 2:
                                        media_path = os.path.join(chip_path, chipname, 'img_create_iot', 'media.bin')
                                        temp_obj = '%s|UNUSED|UNUSED|' % media_path
                                    else:
                                        temp_obj = '%s|UNUSED|UNUSED|' % config['input_path'][name + '_bin_input']
                                    cfg_t.read(self.bh_cfg_file)
                                    cfg_t.set(bootheader_section_name, 'group_image_offset', '0x%x' % (pt_parcel[name + '_addr'] + 4096))
                                    cfg_t.write(self.bh_cfg_file)
                                elif media_sign == 2:
                                    media_path = os.path.join(chip_path, chipname, 'img_create_iot', 'media.bin')
                                    temp_obj = media_path
                                else:
                                    temp_obj = config['input_path'][name + '_bin_input']
                                if temp_obj is not None and len(temp_obj) > 0:
                                    temp = temp_obj.split('|')[0]
                                    try:
                                        if parse_rfpa(temp) == b'BLRFPARA' and dts_bytearray:
                                            length = len(dts_bytearray)
                                            with open(temp, 'rb') as fp:
                                                bin_byte = fp.read()
                                                bin_bytearray = bytearray(bin_byte)
                                                bin_bytearray[1032:1032 + length] = dts_bytearray
                                            (filedir, ext) = os.path.splitext(temp)
                                            temp = filedir + '_rfpa' + ext
                                            with open(temp, 'wb') as fp:
                                                fp.write(bin_bytearray)
                                            temp_obj = temp
                                            if chiptype == 'bl808':
                                                temp_obj = '%s|UNUSED|UNUSED|' % temp_obj
                                    except Exception as e:
                                        bflb_utils.printf(e)
                                    temp_aes_key = None
                                    temp_aes_iv = None
                                    temp_publickey = None
                                    temp_privatekey = None
                                    temp_encrypt = 0
                                    temp_sign = 0
                                    if name + '_security' in pt_parcel:
                                        if pt_parcel[name + '_security'] == 1:
                                            temp_aes_key = config['param']['aes_key']
                                            temp_aes_iv = config['param']['aes_iv']
                                            temp_publickey = config['input_path']['publickey']
                                            temp_privatekey = config['input_path']['privatekey']
                                            if config['check_box']['encrypt']:
                                                temp_encrypt = config['check_box']['encrypt']
                                            if config['check_box']['sign']:
                                                temp_sign = config['check_box']['sign']
                                    if name == 'fw':
                                        self.bl60x_fw_boot_head_gen(False, config['param']['chip_xtal'], self.bh_cfg_file, temp_encrypt, temp_sign, chipname, chiptype, cpu_type, boot2_en)
                                        self.bl60x_image_gen(chipname, chiptype, cpu_type, name, temp_obj, temp_aes_key, temp_aes_iv, temp_publickey, temp_privatekey)
                                        if False == self.bl60x_mfg_ota_bin_gen(chipname, chiptype, pt_parcel, cpu_type, config['param']['version'], config['param']['ota']):
                                            bflb_utils.set_error_code('0082')
                                            return bflb_utils.errorcode_msg()
                                    else:
                                        self.bl60x_fw_boot_head_gen(False, config['param']['chip_xtal'], self.bh_cfg_file, temp_encrypt, temp_sign, chipname, chiptype, cpu_type, boot2_en)
                                        self.bl60x_image_gen(chipname, chiptype, cpu_type, name, temp_obj, temp_aes_key, temp_aes_iv, temp_publickey, temp_privatekey)
                                    'elif name == "mfg":\n                                        self.bl60x_mfg_boot_head_gen(hex(pt_parcel[name+\'_addr\']), config[\'param\']["chip_xtal"],\n                                            self.bh_cfg_file, chipname, chiptype, cpu_type, temp_encrypt, temp_sign)\n                                        self.bl60x_image_gen(chipname, chiptype, cpu_type, name, temp_obj, \n                                                        temp_aes_key, temp_aes_iv, temp_publickey, temp_privatekey)'
                                    bin_d_list[i] = True
                            else:
                                bflb_utils.printf('Error: %s is not in partition table' % name)
                else:
                    if name == 'media':
                        if 'media_download' in config['check_box'] and config['check_box']['media_download'] is True:
                            media_bin = config['input_path']['media_bin_input']
                            if media_bin is not None and len(media_bin) > 0:
                                try:
                                    shutil.copyfile(media_bin, os.path.join(chip_path, chipname, 'img_create_iot', 'media.bin'))
                                except Exception as e:
                                    bflb_utils.printf(e)
                            bin_d_list[i] = True
                        if 'romfs_download' in config['check_box'] and config['check_box']['romfs_download'] is True:
                            romfs_dir = config['input_path']['romfs_dir_input']
                            if romfs_dir is not None and len(romfs_dir) > 0:
                                ret = generate_romfs_img(romfs_dir, os.path.join(chip_path, chipname, 'img_create_iot', 'media.bin'))
                                if ret != 0:
                                    bflb_utils.printf('ERROR, ret %s.' % ret)
                                    error = 'ERROR, ret %s.' % ret
                                    bflb_utils.printf(error)
                                    bflb_utils.set_error_code('007A')
                                    return bflb_utils.errorcode_msg()
                                bin_d_list[i] = True
                    if name + '_download' in config['check_box'] and name + '_bin_input' in config['input_path']:
                        if config['check_box'][name + '_download'] is True:
                            temp_bin = config['input_path'][name + '_bin_input']
                            if temp_bin is not None and len(temp_bin) > 0:
                                try:
                                    shutil.copyfile(temp_bin, os.path.join(chip_path, chipname, 'img_create_iot', name + '.bin'))
                                except Exception as e:
                                    bflb_utils.printf(e)
                            bin_d_list[i] = True
            return self.bl60x_mfg_flasher_eflash_loader_cfg(chipname, chiptype, boot2_d, pt_parcel, bin_d_list, name_list)
        if 'bin_download' in config['check_box'] and config['check_box']['bin_download'] is True:
            if 'fw_addr' in pt_parcel:
                if chiptype == 'bl808':
                    print(config['input_path']['cfg2_bin_input'])
                    bin = '%s|UNUSED|UNUSED|' % config['input_path']['cfg2_bin_input']
                    cfg_t.read(self.bh_cfg_file)
                    cfg_t.set(bootheader_section_name, 'group_image_offset', '0x%x' % (pt_parcel['fw_addr'] + 4096))
                    cfg_t.write(self.bh_cfg_file)
                else:
                    bin = config['input_path']['cfg2_bin_input']
                if bin is not None and len(bin) > 0:
                    temp = bin.split('|')[0]
                    if parse_rfpa(temp) == b'BLRFPARA' and dts_bytearray:
                        length = len(dts_bytearray)
                        with open(temp, 'rb') as fp:
                            bin_byte = fp.read()
                            bin_bytearray = bytearray(bin_byte)
                            bin_bytearray[1032:1032 + length] = dts_bytearray
                        (filedir, ext) = os.path.splitext(temp)
                        temp = filedir + '_rfpa' + ext
                        with open(temp, 'wb') as fp:
                            fp.write(bin_bytearray)
                        bin = temp
                        if chiptype == 'bl808':
                            bin = '%s|UNUSED|UNUSED|' % bin
                    self.bl60x_fw_boot_head_gen(False, config['param']['chip_xtal'], self.bh_cfg_file, config['check_box']['encrypt'], config['check_box']['sign'], chipname, chiptype, cpu_type, boot2_en)
                    self.bl60x_image_gen(chipname, chiptype, cpu_type, 'fw', bin, config['param']['aes_key'], config['param']['aes_iv'], config['input_path']['publickey'], config['input_path']['privatekey'])
                    if False == self.bl60x_mfg_ota_bin_gen(chipname, chiptype, pt_parcel, cpu_type, config['param']['version'], config['param']['ota']):
                        bflb_utils.set_error_code('0082')
                        return bflb_utils.errorcode_msg()
                    bin_d = True
            else:
                bflb_utils.printf('Error: FW is not in partition table')
        if 'fw_download' in config['check_box'] and config['check_box']['fw_download'] is True:
            if 'fw_addr' in pt_parcel:
                if chiptype == 'bl808':
                    print(config['input_path']['fw_bin_input'])
                    bin = '%s|UNUSED|UNUSED|' % config['input_path']['fw_bin_input']
                    cfg_t.read(self.bh_cfg_file)
                    cfg_t.set(bootheader_section_name, 'group_image_offset', '0x%x' % (pt_parcel['fw_addr'] + 4096))
                    cfg_t.write(self.bh_cfg_file)
                else:
                    bin = config['input_path']['fw_bin_input']
                if bin is not None and len(bin) > 0:
                    temp = bin.split('|')[0]
                    if parse_rfpa(temp) == b'BLRFPARA' and dts_bytearray:
                        length = len(dts_bytearray)
                        with open(temp, 'rb') as fp:
                            bin_byte = fp.read()
                            bin_bytearray = bytearray(bin_byte)
                            bin_bytearray[1032:1032 + length] = dts_bytearray
                        (filedir, ext) = os.path.splitext(temp)
                        temp = filedir + '_rfpa' + ext
                        with open(temp, 'wb') as fp:
                            fp.write(bin_bytearray)
                        bin = temp
                        if chiptype == 'bl808':
                            bin = '%s|UNUSED|UNUSED|' % bin
                    self.bl60x_fw_boot_head_gen(False, config['param']['chip_xtal'], self.bh_cfg_file, config['check_box']['encrypt'], config['check_box']['sign'], chipname, chiptype, cpu_type, boot2_en)
                    self.bl60x_image_gen(chipname, chiptype, cpu_type, 'fw', bin, config['param']['aes_key'], config['param']['aes_iv'], config['input_path']['publickey'], config['input_path']['privatekey'])
                    if False == self.bl60x_mfg_ota_bin_gen(chipname, chiptype, pt_parcel, cpu_type, config['param']['version'], config['param']['ota']):
                        bflb_utils.set_error_code('0082')
                        return bflb_utils.errorcode_msg()
                    bin_d = True
            else:
                bflb_utils.printf('Error: FW is not in partition table')
        if 'd0_download' in config['check_box'] and 'd0_bin_input' in config['input_path']:
            if config['check_box']['d0_download'] is True:
                if 'fw_d0_addr' in pt_parcel:
                    if chiptype == 'bl808':
                        d0_bin = '%s|UNUSED|UNUSED|' % config['input_path']['d0_bin_input']
                        cfg_t.read(self.bh_cfg_file)
                        cfg_t.set(bootheader_section_name, 'group_image_offset', '0x%x' % (pt_parcel['fw_d0_addr'] + 4096))
                        cfg_t.write(self.bh_cfg_file)
                    else:
                        d0_bin = config['input_path']['d0_bin_input']
                    if d0_bin is not None and len(d0_bin) > 0:
                        temp = d0_bin.split('|')[0]
                        if parse_rfpa(temp) == b'BLRFPARA' and dts_bytearray:
                            length = len(dts_bytearray)
                            with open(temp, 'rb') as fp:
                                bin_byte = fp.read()
                                bin_bytearray = bytearray(bin_byte)
                                bin_bytearray[1032:1032 + length] = dts_bytearray
                            (filedir, ext) = os.path.splitext(temp)
                            temp = filedir + '_rfpa' + ext
                            with open(temp, 'wb') as fp:
                                fp.write(bin_bytearray)
                            d0_bin = temp
                            if chiptype == 'bl808':
                                d0_bin = '%s|UNUSED|UNUSED|' % d0_bin
                        self.bl60x_fw_boot_head_gen(False, config['param']['chip_xtal'], self.bh_cfg_file, config['check_box']['encrypt'], config['check_box']['sign'], chipname, chiptype, cpu_type, boot2_en)
                        self.bl60x_image_gen(chipname, chiptype, cpu_type, 'd0fw', d0_bin, config['param']['aes_key'], config['param']['aes_iv'], config['input_path']['publickey'], config['input_path']['privatekey'])
                        d0_bin_d = True
                else:
                    bflb_utils.printf('Error: D0FW is not in partition table')
        if 'd0fw_download' in config['check_box'] and 'd0fw_bin_input' in config['input_path']:
            if config['check_box']['d0fw_download'] is True:
                if 'fw_d0_addr' in pt_parcel:
                    if chiptype == 'bl808':
                        d0_bin = '%s|UNUSED|UNUSED|' % config['input_path']['d0fw_bin_input']
                        cfg_t.read(self.bh_cfg_file)
                        cfg_t.set(bootheader_section_name, 'group_image_offset', '0x%x' % (pt_parcel['fw_d0_addr'] + 4096))
                        cfg_t.write(self.bh_cfg_file)
                    else:
                        d0_bin = config['input_path']['d0_bin_input']
                    if d0_bin is not None and len(d0_bin) > 0:
                        temp = d0_bin.split('|')[0]
                        if parse_rfpa(temp) == b'BLRFPARA' and dts_bytearray:
                            length = len(dts_bytearray)
                            with open(temp, 'rb') as fp:
                                bin_byte = fp.read()
                                bin_bytearray = bytearray(bin_byte)
                                bin_bytearray[1032:1032 + length] = dts_bytearray
                            (filedir, ext) = os.path.splitext(temp)
                            temp = filedir + '_rfpa' + ext
                            with open(temp, 'wb') as fp:
                                fp.write(bin_bytearray)
                            d0_bin = temp
                            if chiptype == 'bl808':
                                d0_bin = '%s|UNUSED|UNUSED|' % d0_bin
                        self.bl60x_fw_boot_head_gen(False, config['param']['chip_xtal'], self.bh_cfg_file, config['check_box']['encrypt'], config['check_box']['sign'], chipname, chiptype, cpu_type, boot2_en)
                        self.bl60x_image_gen(chipname, chiptype, cpu_type, 'd0fw', d0_bin, config['param']['aes_key'], config['param']['aes_iv'], config['input_path']['publickey'], config['input_path']['privatekey'])
                        d0_bin_d = True
                else:
                    bflb_utils.printf('Error: D0FW is not in partition table')
        if 'yocboot_download' in config['check_box'] and 'yocboot_bin_input' in config['input_path']:
            if config['check_box']['yocboot_download'] is True:
                if 'fw_yocboot_addr' in pt_parcel:
                    if chiptype == 'bl808':
                        yocboot_bin = '%s|UNUSED|UNUSED|' % config['input_path']['yocboot_bin_input']
                        cfg_t.read(self.bh_cfg_file)
                        cfg_t.set(bootheader_section_name, 'group_image_offset', '0x%x' % (pt_parcel['fw_yocboot_addr'] + 4096))
                        cfg_t.write(self.bh_cfg_file)
                    else:
                        yocboot_bin = config['input_path']['yocboot_bin_input']
                    if yocboot_bin is not None and len(yocboot_bin) > 0:
                        temp = yocboot_bin.split('|')[0]
                        if parse_rfpa(temp) == b'BLRFPARA' and dts_bytearray:
                            length = len(dts_bytearray)
                            with open(temp, 'rb') as fp:
                                bin_byte = fp.read()
                                bin_bytearray = bytearray(bin_byte)
                                bin_bytearray[1032:1032 + length] = dts_bytearray
                            (filedir, ext) = os.path.splitext(temp)
                            temp = filedir + '_rfpa' + ext
                            with open(temp, 'wb') as fp:
                                fp.write(bin_bytearray)
                            yocboot_bin = temp
                            if chiptype == 'bl808':
                                yocboot_bin = '%s|UNUSED|UNUSED|' % yocboot_bin
                        self.bl60x_fw_boot_head_gen(False, config['param']['chip_xtal'], self.bh_cfg_file, config['check_box']['encrypt'], config['check_box']['sign'], chipname, chiptype, cpu_type, boot2_en)
                        self.bl60x_image_gen(chipname, chiptype, cpu_type, 'yocboot', yocboot_bin, config['param']['aes_key'], config['param']['aes_iv'], config['input_path']['publickey'], config['input_path']['privatekey'])
                        yocboot_bin_d = True
                else:
                    bflb_utils.printf('Error: yocboot is not in partition table')
        if 'dtb_download' in config['check_box'] and 'dtb_bin_input' in config['input_path']:
            if config['check_box']['dtb_download'] is True:
                if 'dtb_addr' in pt_parcel:
                    if chiptype == 'bl808':
                        dtb_bin = '%s|UNUSED|UNUSED|' % config['input_path']['dtb_bin_input']
                        cfg_t.read(self.bh_cfg_file)
                        cfg_t.set(bootheader_section_name, 'group_image_offset', '0x%x' % (pt_parcel['dtb_addr'] + 4096))
                        cfg_t.write(self.bh_cfg_file)
                    else:
                        dtb_bin = config['input_path']['dtb_bin_input']
                    if dtb_bin is not None and len(dtb_bin) > 0:
                        temp = dtb_bin.split('|')[0]
                        if parse_rfpa(temp) == b'BLRFPARA' and dts_bytearray:
                            length = len(dts_bytearray)
                            with open(temp, 'rb') as fp:
                                bin_byte = fp.read()
                                bin_bytearray = bytearray(bin_byte)
                                bin_bytearray[1032:1032 + length] = dts_bytearray
                            (filedir, ext) = os.path.splitext(temp)
                            temp = filedir + '_rfpa' + ext
                            with open(temp, 'wb') as fp:
                                fp.write(bin_bytearray)
                            dtb_bin = temp
                            if chiptype == 'bl808':
                                dtb_bin = '%s|UNUSED|UNUSED|' % dtb_bin
                        self.bl60x_fw_boot_head_gen(False, config['param']['chip_xtal'], self.bh_cfg_file, config['check_box']['encrypt'], config['check_box']['sign'], chipname, chiptype, cpu_type, boot2_en)
                        self.bl60x_image_gen(chipname, chiptype, cpu_type, 'dtb', dtb_bin, config['param']['aes_key'], config['param']['aes_iv'], config['input_path']['publickey'], config['input_path']['privatekey'])
                        dtb_bin_d = True
                else:
                    bflb_utils.printf('Error: dtb is not in partition table')
        if 'imtb_download' in config['check_box'] and 'imtb_bin_input' in config['input_path']:
            if config['check_box']['imtb_download'] is True:
                imtb_bin = config['input_path']['imtb_bin_input']
                if imtb_bin is not None and len(imtb_bin) > 0:
                    try:
                        shutil.copyfile(imtb_bin, os.path.join(chip_path, chipname, 'img_create_iot', 'imtb.bin'))
                    except Exception as e:
                        bflb_utils.printf(e)
                imtb_bin_d = True
        if 'kv_download' in config['check_box'] and 'kv_bin_input' in config['input_path']:
            if config['check_box']['kv_download'] is True:
                kv_bin = config['input_path']['kv_bin_input']
                if kv_bin is not None and len(kv_bin) > 0:
                    try:
                        shutil.copyfile(kv_bin, os.path.join(chip_path, chipname, 'img_create_iot', 'kv.bin'))
                    except Exception as e:
                        bflb_utils.printf(e)
                kv_bin_d = True
        if 'media_download' in config['check_box'] and config['check_box']['media_download'] is True:
            media_bin = config['input_path']['media_bin_input']
            if media_bin is not None and len(media_bin) > 0:
                try:
                    shutil.copyfile(media_bin, os.path.join(chip_path, chipname, 'img_create_iot', 'media.bin'))
                except Exception as e:
                    bflb_utils.printf(e)
            media_bin_d = True
        if 'romfs_download' in config['check_box'] and config['check_box']['romfs_download'] is True:
            romfs_dir = config['input_path']['romfs_dir_input']
            if romfs_dir is not None and len(romfs_dir) > 0:
                ret = generate_romfs_img(romfs_dir, os.path.join(chip_path, chipname, 'img_create_iot', 'media.bin'))
                if ret != 0:
                    bflb_utils.printf('ERROR, ret %s.' % ret)
                    error = 'ERROR, ret %s.' % ret
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code('007A')
                    return bflb_utils.errorcode_msg()
                media_bin_d = True
        if 'mfg_download' in config['check_box'] and config['check_box']['mfg_download'] is True:
            if 'mfg_addr' in pt_parcel:
                if chiptype == 'bl808':
                    mfg = '%s|UNUSED|UNUSED|' % config['input_path']['mfg_bin_input']
                    cfg_t.read(self.bh_cfg_file)
                    cfg_t.set(bootheader_section_name, 'group_image_offset', '0x%x' % (pt_parcel['mfg_addr'] + 4096))
                    cfg_t.write(self.bh_cfg_file)
                else:
                    mfg = config['input_path']['mfg_bin_input']
                if mfg is not None and len(mfg) > 0:
                    temp = mfg.split('|')[0]
                    if parse_rfpa(temp) == b'BLRFPARA' and dts_bytearray:
                        length = len(dts_bytearray)
                        with open(temp, 'rb') as fp:
                            bin_byte = fp.read()
                            bin_bytearray = bytearray(bin_byte)
                            bin_bytearray[1032:1032 + length] = dts_bytearray
                        (filedir, ext) = os.path.splitext(temp)
                        temp = filedir + '_rfpa' + ext
                        with open(temp, 'wb') as fp:
                            fp.write(bin_bytearray)
                        mfg = temp
                        if chiptype == 'bl808':
                            mfg = '%s|UNUSED|UNUSED|' % mfg
                    self.bl60x_mfg_boot_head_gen(hex(pt_parcel['mfg_addr']), config['param']['chip_xtal'], self.bh_cfg_file, chipname, chiptype, cpu_type, config['check_box']['encrypt'], config['check_box']['sign'])
                    f_org = os.path.join(chip_path, chipname, 'img_create_iot', 'img_create_cfg_mfg.conf')
                    f = os.path.join(chip_path, chipname, 'img_create_iot', 'img_create_cfg_mfg.ini')
                    if os.path.isfile(f) is False:
                        shutil.copyfile(f_org, f)
                    self.bl60x_image_gen(chipname, chiptype, cpu_type, 'mfg', mfg, config['param']['aes_key'], config['param']['aes_iv'], config['input_path']['publickey'], config['input_path']['privatekey'], f)
                    mfg_bin_d = True
            else:
                bflb_utils.printf('Error: mfg is not in partition table')
        return self.bl60x_mfg_flasher_eflash_loader_cfg_old(chipname, chiptype, bin_d, boot2_d, ro_params_d, pt_parcel, media_bin_d, mfg_bin_d, d0_bin_d, imtb_bin_d, kv_bin_d, yocboot_bin_d, dtb_bin_d)

    def flasher_download_cfg_ini_gen_old(self, chipname, chiptype, cpu_type, config):
        bin_d = False
        boot2_d = False
        ro_params_d = None
        pt_parcel = None
        media_bin_d = False
        mfg_bin_d = False
        d0_bin_d = False
        imtb_bin_d = False
        kv_bin_d = False
        yocboot_bin_d = False
        boot2_en = False
        dts_bytearray = None
        partition_path = os.path.join(chip_path, chipname, 'partition/partition.bin')
        error = 'Please check your partition table file'
        self.config = config
        if chiptype == 'bl702':
            if config['check_box']['boot2_download'] is True:
                boot2_en = False
            else:
                boot2_en = True
        cfg = BFConfigParser()
        cfg.read(self.eflash_loader_cfg)
        if cfg.has_option('FLASH_CFG', 'flash_id'):
            flash_id = cfg.get('FLASH_CFG', 'flash_id')
            bflb_utils.printf('========= chip flash id: %s =========' % flash_id)
            if chiptype == 'bl602' or chiptype == 'bl702':
                if bflb_flash_select.update_flash_cfg(chipname, chiptype, flash_id, self.bh_cfg_file, False, 'BOOTHEADER_CFG') is False:
                    error = 'flash_id:' + flash_id + ' do not support'
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code('0069')
                    return bflb_utils.errorcode_msg()
            elif chiptype == 'bl60x':
                if bflb_flash_select.update_flash_cfg(chipname, chiptype, flash_id, self.bh_cfg_file, False, 'BOOTHEADER_CPU0_CFG') is False:
                    error = 'flash_id:' + flash_id + ' do not support'
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code('0069')
                    return bflb_utils.errorcode_msg()
            elif chiptype == 'bl808' or chiptype == 'bl616':
                if bflb_flash_select.update_flash_cfg(chipname, chiptype, flash_id, self.bh_cfg_file, False, 'BOOTHEADER_GROUP0_CFG') is False:
                    error = 'flash_id:' + flash_id + ' do not support'
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code('0069')
                    return bflb_utils.errorcode_msg()
        else:
            error = 'Do not find flash_id in eflash_loader_cfg.ini'
            bflb_utils.printf(error)
            bflb_utils.set_error_code('0070')
            return bflb_utils.errorcode_msg()
        if config['check_box']['ro_params_download'] is True:
            ro = config['input_path']['dts_input']
            if not os.path.isfile(ro):
                bflb_utils.printf("Don't Find %s as bl_factory image" % ro)
                error = "Don't Find %s as bl_factory image" % ro
                bflb_utils.printf(error)
                bflb_utils.set_error_code('0079')
                return bflb_utils.errorcode_msg()
            if ro is not None and len(ro) > 0:
                ro_params_d = ro
                try:
                    dts_hex = bl_ro_device_tree.bl_dts2hex(ro_params_d)
                    dts_bytearray = bflb_utils.hexstr_to_bytearray(dts_hex)
                except Exception as e:
                    dts_bytearray = None
        pt = config['input_path']['pt_bin_input']
        if pt is not None and len(pt) > 0:
            pt_helper = partition.PtCreater(pt)
            if config['check_box']['partition_download'] is True:
                bflb_utils.printf('create partition.bin, pt_new is True')
                pt_helper.create_pt_table(partition_path)
            (pt_parcel, name_list) = pt_helper.construct_table()
            if chiptype == 'bl702':
                cfg_t = BFConfigParser()
                cfg_t.read(self.bh_cfg_file)
                cfg_t.set('BOOTHEADER_CFG', 'boot2_pt_table_0', '0x%X' % pt_parcel['pt_addr0'])
                cfg_t.set('BOOTHEADER_CFG', 'boot2_pt_table_1', '0x%X' % pt_parcel['pt_addr1'])
                cfg_t.write(self.bh_cfg_file)
        else:
            bflb_utils.set_error_code('0076')
            return bflb_utils.errorcode_msg()
        if config['check_box']['encrypt'] is True:
            aes_key = config['param']['aes_key'].replace(' ', '')
            aes_iv = config['param']['aes_iv'].replace(' ', '')
            if verify_hex_num(aes_key) is not True or len(aes_key) != 32:
                error = 'Error: Please check AES key data and len'
                bflb_utils.printf(error)
                bflb_utils.set_error_code('0077')
                return bflb_utils.errorcode_msg()
            if verify_hex_num(aes_iv) is not True or len(aes_iv) != 32:
                error = 'Error: Please check AES iv data and len'
                bflb_utils.printf(error)
                bflb_utils.set_error_code('0078')
                return bflb_utils.errorcode_msg()
            if aes_iv.endswith('00000000') is False:
                error = 'AES IV should endswith 4 bytes zero'
                bflb_utils.printf(error)
                bflb_utils.set_error_code('0073')
                return bflb_utils.errorcode_msg()
        if config['check_box']['sign'] is True:
            if not config['input_path']['publickey']:
                error = 'Please set public key'
                bflb_utils.printf(error)
                bflb_utils.set_error_code('0066')
                return bflb_utils.errorcode_msg()
            if not config['input_path']['privatekey']:
                error = 'Please set private key'
                bflb_utils.printf(error)
                bflb_utils.set_error_code('0067')
                return bflb_utils.errorcode_msg()
        cfg_t = BFConfigParser()
        cfg_t.read(self.bh_cfg_file)
        if 'BOOTHEADER_CPU0_CFG' in cfg_t.sections():
            bootheader_section_name = 'BOOTHEADER_CPU0_CFG'
        elif 'BOOTHEADER_GROUP0_CFG' in cfg_t.sections():
            bootheader_section_name = 'BOOTHEADER_GROUP0_CFG'
        else:
            bootheader_section_name = 'BOOTHEADER_CFG'
        crc_ignore = cfg_t.get(bootheader_section_name, 'crc_ignore')
        hash_ignore = cfg_t.get(bootheader_section_name, 'hash_ignore')
        cfg_t.set(bootheader_section_name, 'crc_ignore', 1)
        cfg_t.set(bootheader_section_name, 'hash_ignore', 1)
        cfg_t.write(self.bh_cfg_file)
        if config['check_box']['boot2_download'] is True:
            if chiptype == 'bl808':
                boot2 = '%s|UNUSED|UNUSED|' % config['input_path']['boot2_bin_input']
            else:
                boot2 = config['input_path']['boot2_bin_input']
            if boot2 is not None and len(boot2) > 0:
                self.bl60x_fw_boot_head_gen(True, config['param']['chip_xtal'], self.bh_cfg_file, config['check_box']['encrypt'], config['check_box']['sign'], chipname, chiptype, cpu_type, boot2_en)
                f_org = os.path.join(chip_path, chipname, 'img_create_iot', 'img_create_cfg_boot2.conf')
                f = os.path.join(chip_path, chipname, 'img_create_iot', 'img_create_cfg_boot2.ini')
                if os.path.isfile(f) is False:
                    shutil.copyfile(f_org, f)
                self.bl60x_image_gen(chipname, chiptype, cpu_type, 'boot2', boot2, config['param']['aes_key'], config['param']['aes_iv'], config['input_path']['publickey'], config['input_path']['privatekey'], f)
                boot2_d = True
        elif chiptype == 'bl702':
            self.bl60x_fw_boot_head_gen(True, config['param']['chip_xtal'], self.bh_cfg_file, config['check_box']['encrypt'], config['check_box']['sign'], chipname, chiptype, cpu_type, boot2_en)
        cfg_t = BFConfigParser()
        cfg_t.read(self.bh_cfg_file)
        cfg_t.set(bootheader_section_name, 'crc_ignore', crc_ignore)
        cfg_t.set(bootheader_section_name, 'hash_ignore', hash_ignore)
        cfg_t.write(self.bh_cfg_file)
        if config['check_box']['bin_download'] is True:
            if 'fw_addr' in pt_parcel:
                if chiptype == 'bl808':
                    print(config['input_path']['cfg2_bin_input'])
                    bin = '%s|UNUSED|UNUSED|' % config['input_path']['cfg2_bin_input']
                    cfg_t.read(self.bh_cfg_file)
                    cfg_t.set(bootheader_section_name, 'group_image_offset', '0x%x' % (pt_parcel['fw_addr'] + 4096))
                    cfg_t.write(self.bh_cfg_file)
                else:
                    bin = config['input_path']['cfg2_bin_input']
                if bin is not None and len(bin) > 0:
                    temp = bin.split('|')[0]
                    if parse_rfpa(temp) == b'BLRFPARA' and dts_bytearray:
                        length = len(dts_bytearray)
                        with open(temp, 'rb') as fp:
                            bin_byte = fp.read()
                            bin_bytearray = bytearray(bin_byte)
                            bin_bytearray[1032:1032 + length] = dts_bytearray
                        (filedir, ext) = os.path.splitext(temp)
                        temp = filedir + '_rfpa' + ext
                        with open(temp, 'wb') as fp:
                            fp.write(bin_bytearray)
                        bin = temp
                        if chiptype == 'bl808':
                            bin = '%s|UNUSED|UNUSED|' % bin
                    self.bl60x_fw_boot_head_gen(False, config['param']['chip_xtal'], self.bh_cfg_file, config['check_box']['encrypt'], config['check_box']['sign'], chipname, chiptype, cpu_type, boot2_en)
                    self.bl60x_image_gen(chipname, chiptype, cpu_type, 'fw', bin, config['param']['aes_key'], config['param']['aes_iv'], config['input_path']['publickey'], config['input_path']['privatekey'])
                    if False == self.bl60x_mfg_ota_bin_gen(chipname, chiptype, pt_parcel, cpu_type, config['param']['version'], config['param']['ota']):
                        bflb_utils.set_error_code('0082')
                        return bflb_utils.errorcode_msg()
                    bin_d = True
            else:
                bflb_utils.printf('Error: FW is not in partition table')
        if 'd0_download' in config['check_box'] and 'd0_bin_input' in config['input_path']:
            if config['check_box']['d0_download'] is True:
                if 'fw_d0_addr' in pt_parcel:
                    if chiptype == 'bl808':
                        d0_bin = '%s|UNUSED|UNUSED|' % config['input_path']['d0_bin_input']
                        cfg_t.read(self.bh_cfg_file)
                        cfg_t.set(bootheader_section_name, 'group_image_offset', '0x%x' % (pt_parcel['fw_d0_addr'] + 4096))
                        cfg_t.write(self.bh_cfg_file)
                    else:
                        d0_bin = config['input_path']['d0_bin_input']
                    if d0_bin is not None and len(d0_bin) > 0:
                        temp = d0_bin.split('|')[0]
                        if parse_rfpa(temp) == b'BLRFPARA' and dts_bytearray:
                            length = len(dts_bytearray)
                            with open(temp, 'rb') as fp:
                                bin_byte = fp.read()
                                bin_bytearray = bytearray(bin_byte)
                                bin_bytearray[1032:1032 + length] = dts_bytearray
                            (filedir, ext) = os.path.splitext(temp)
                            temp = filedir + '_rfpa' + ext
                            with open(temp, 'wb') as fp:
                                fp.write(bin_bytearray)
                            d0_bin = temp
                            if chiptype == 'bl808':
                                d0_bin = '%s|UNUSED|UNUSED|' % d0_bin
                        self.bl60x_fw_boot_head_gen(False, config['param']['chip_xtal'], self.bh_cfg_file, config['check_box']['encrypt'], config['check_box']['sign'], chipname, chiptype, cpu_type, boot2_en)
                        self.bl60x_image_gen(chipname, chiptype, cpu_type, 'd0fw', d0_bin, config['param']['aes_key'], config['param']['aes_iv'], config['input_path']['publickey'], config['input_path']['privatekey'])
                        d0_bin_d = True
                else:
                    bflb_utils.printf('Error: D0FW is not in partition table')
        if 'yocboot_download' in config['check_box'] and 'yocboot_bin_input' in config['input_path']:
            if config['check_box']['yocboot_download'] is True:
                if 'fw_yocboot_addr' in pt_parcel:
                    if chiptype == 'bl808':
                        yocboot_bin = '%s|UNUSED|UNUSED|' % config['input_path']['yocboot_bin_input']
                        cfg_t.read(self.bh_cfg_file)
                        cfg_t.set(bootheader_section_name, 'group_image_offset', '0x%x' % (pt_parcel['fw_yocboot_addr'] + 4096))
                        cfg_t.write(self.bh_cfg_file)
                    else:
                        yocboot_bin = config['input_path']['yocboot_bin_input']
                    if yocboot_bin is not None and len(yocboot_bin) > 0:
                        temp = yocboot_bin.split('|')[0]
                        if parse_rfpa(temp) == b'BLRFPARA' and dts_bytearray:
                            length = len(dts_bytearray)
                            with open(temp, 'rb') as fp:
                                bin_byte = fp.read()
                                bin_bytearray = bytearray(bin_byte)
                                bin_bytearray[1032:1032 + length] = dts_bytearray
                            (filedir, ext) = os.path.splitext(temp)
                            temp = filedir + '_rfpa' + ext
                            with open(temp, 'wb') as fp:
                                fp.write(bin_bytearray)
                            yocboot_bin = temp
                            if chiptype == 'bl808':
                                yocboot_bin = '%s|UNUSED|UNUSED|' % yocboot_bin
                        self.bl60x_fw_boot_head_gen(False, config['param']['chip_xtal'], self.bh_cfg_file, config['check_box']['encrypt'], config['check_box']['sign'], chipname, chiptype, cpu_type, boot2_en)
                        self.bl60x_image_gen(chipname, chiptype, cpu_type, 'yocboot', yocboot_bin, config['param']['aes_key'], config['param']['aes_iv'], config['input_path']['publickey'], config['input_path']['privatekey'])
                        yocboot_bin_d = True
                else:
                    bflb_utils.printf('Error: yocboot is not in partition table')
        if 'dtb_download' in config['check_box'] and 'dtb_bin_input' in config['input_path']:
            if config['check_box']['dtb_download'] is True:
                if 'dtb_addr' in pt_parcel:
                    if chiptype == 'bl808':
                        dtb_bin = '%s|UNUSED|UNUSED|' % config['input_path']['dtb_bin_input']
                        cfg_t.read(self.bh_cfg_file)
                        cfg_t.set(bootheader_section_name, 'group_image_offset', '0x%x' % (pt_parcel['dtb_addr'] + 4096))
                        cfg_t.write(self.bh_cfg_file)
                    else:
                        dtb_bin = config['input_path']['dtb_bin_input']
                    if dtb_bin is not None and len(dtb_bin) > 0:
                        temp = dtb_bin.split('|')[0]
                        if parse_rfpa(temp) == b'BLRFPARA' and dts_bytearray:
                            length = len(dts_bytearray)
                            with open(temp, 'rb') as fp:
                                bin_byte = fp.read()
                                bin_bytearray = bytearray(bin_byte)
                                bin_bytearray[1032:1032 + length] = dts_bytearray
                            (filedir, ext) = os.path.splitext(temp)
                            temp = filedir + '_rfpa' + ext
                            with open(temp, 'wb') as fp:
                                fp.write(bin_bytearray)
                            dtb_bin = temp
                            if chiptype == 'bl808':
                                dtb_bin = '%s|UNUSED|UNUSED|' % dtb_bin
                        self.bl60x_fw_boot_head_gen(False, config['param']['chip_xtal'], self.bh_cfg_file, config['check_box']['encrypt'], config['check_box']['sign'], chipname, chiptype, cpu_type, boot2_en)
                        self.bl60x_image_gen(chipname, chiptype, cpu_type, 'dtb', dtb_bin, config['param']['aes_key'], config['param']['aes_iv'], config['input_path']['publickey'], config['input_path']['privatekey'])
                        dtb_bin_d = True
                else:
                    bflb_utils.printf('Error: dtb is not in partition table')
        if 'imtb_download' in config['check_box'] and 'imtb_bin_input' in config['input_path']:
            if config['check_box']['imtb_download'] is True:
                imtb_bin = config['input_path']['imtb_bin_input']
                if imtb_bin is not None and len(imtb_bin) > 0:
                    try:
                        shutil.copyfile(imtb_bin, os.path.join(chip_path, chipname, 'img_create_iot', 'imtb.bin'))
                    except Exception as e:
                        bflb_utils.printf(e)
                imtb_bin_d = True
        if 'kv_download' in config['check_box'] and 'kv_bin_input' in config['input_path']:
            if config['check_box']['kv_download'] is True:
                kv_bin = config['input_path']['kv_bin_input']
                if kv_bin is not None and len(kv_bin) > 0:
                    try:
                        shutil.copyfile(kv_bin, os.path.join(chip_path, chipname, 'img_create_iot', 'kv.bin'))
                    except Exception as e:
                        bflb_utils.printf(e)
                kv_bin_d = True
        if config['check_box']['media_download'] is True:
            media_bin = config['input_path']['media_bin_input']
            if media_bin is not None and len(media_bin) > 0:
                try:
                    shutil.copyfile(media_bin, os.path.join(chip_path, chipname, 'img_create_iot', 'media.bin'))
                except Exception as e:
                    bflb_utils.printf(e)
            media_bin_d = True
        if config['check_box']['romfs_download'] is True:
            romfs_dir = config['input_path']['romfs_dir_input']
            if romfs_dir is not None and len(romfs_dir) > 0:
                ret = generate_romfs_img(romfs_dir, os.path.join(chip_path, chipname, 'img_create_iot', 'media.bin'))
                if ret != 0:
                    bflb_utils.printf('ERROR, ret %s.' % ret)
                    error = 'ERROR, ret %s.' % ret
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code('007A')
                    return bflb_utils.errorcode_msg()
                media_bin_d = True
        if config['check_box']['mfg_download'] is True:
            if 'mfg_addr' in pt_parcel:
                if chiptype == 'bl808':
                    mfg = '%s|UNUSED|UNUSED|' % config['input_path']['mfg_bin_input']
                    cfg_t.read(self.bh_cfg_file)
                    cfg_t.set(bootheader_section_name, 'group_image_offset', '0x%x' % (pt_parcel['mfg_addr'] + 4096))
                    cfg_t.write(self.bh_cfg_file)
                else:
                    mfg = config['input_path']['mfg_bin_input']
                if mfg is not None and len(mfg) > 0:
                    temp = mfg.split('|')[0]
                    if parse_rfpa(temp) == b'BLRFPARA' and dts_bytearray:
                        length = len(dts_bytearray)
                        with open(temp, 'rb') as fp:
                            bin_byte = fp.read()
                            bin_bytearray = bytearray(bin_byte)
                            bin_bytearray[1032:1032 + length] = dts_bytearray
                        (filedir, ext) = os.path.splitext(temp)
                        temp = filedir + '_rfpa' + ext
                        with open(temp, 'wb') as fp:
                            fp.write(bin_bytearray)
                        mfg = temp
                        if chiptype == 'bl808':
                            mfg = '%s|UNUSED|UNUSED|' % mfg
                    self.bl60x_mfg_boot_head_gen(hex(pt_parcel['mfg_addr']), config['param']['chip_xtal'], self.bh_cfg_file, chipname, chiptype, cpu_type)
                    f_org = os.path.join(chip_path, chipname, 'img_create_iot', 'img_create_cfg_mfg.conf')
                    f = os.path.join(chip_path, chipname, 'img_create_iot', 'img_create_cfg_mfg.ini')
                    if os.path.isfile(f) is False:
                        shutil.copyfile(f_org, f)
                    self.bl60x_image_gen(chipname, chiptype, cpu_type, 'mfg', mfg, config['param']['aes_key'], config['param']['aes_iv'], config['input_path']['publickey'], config['input_path']['privatekey'], f)
                    mfg_bin_d = True
            else:
                bflb_utils.printf('Error: mfg is not in partition table')
        return self.bl60x_mfg_flasher_eflash_loader_cfg(chipname, chiptype, bin_d, boot2_d, ro_params_d, pt_parcel, media_bin_d, mfg_bin_d, d0_bin_d, imtb_bin_d, kv_bin_d, yocboot_bin_d, dtb_bin_d)

    def flasher_download_thread(self, chipname, chiptype, act, config, callback=None):
        self.config = config
        error = None
        cpu_type = None
        ota_path = os.path.join(chip_path, chipname, 'ota')
        imgcreate_path = os.path.join(chip_path, chipname, 'img_create_iot')
        if not os.path.exists(ota_path):
            os.makedirs(ota_path)
        if not os.path.exists(imgcreate_path):
            os.makedirs(imgcreate_path)
        if chipname in gol.cpu_type.keys():
            cpu_type = gol.cpu_type[chipname][0]
        if act != 'build' and act != 'download':
            return 'no such action!'
        try:
            if config['param']['interface_type'] == 'uart':
                uart = config['param']['comport_uart']
                uart_brd = config['param']['speed_uart']
                if not uart_brd.isdigit():
                    error = '{"ErrorCode":"FFFF","ErrorMsg":"BAUDRATE MUST BE DIGIT"}'
                    bflb_utils.printf(error)
                    return error
                bflb_utils.printf('========= Interface is Uart =========')
                self.bl60x_mfg_flasher_cfg(uart, uart_brd)
            elif config['param']['interface_type'] == 'jlink':
                jlink_brd = config['param']['speed_jlink']
                if not jlink_brd.isdigit():
                    error = '{"ErrorCode":"FFFF","ErrorMsg":"BAUDRATE MUST BE DIGIT"}'
                    bflb_utils.printf(error)
                    return error
                bflb_utils.printf('========= Interface is JLink =========')
                self.bl60x_mfg_flasher_jlink_cfg(rate=jlink_brd)
            elif config['param']['interface_type'] == 'cklink':
                bflb_utils.printf('========= Interface is CKLink =========')
                self.bl60x_mfg_flasher_cklink_cfg()
            else:
                openocd_brd = config['param']['speed_jlink']
                bflb_utils.printf('========= Interface is Openocd =========')
                self.bl60x_mfg_flasher_openocd_cfg(rate=openocd_brd)
            cfg = BFConfigParser()
            cfg.read(self.eflash_loader_cfg)
            if 'dl_verify' in config['param'].keys():
                if config['param']['verify'] == 'True':
                    cfg.set('LOAD_CFG', 'verify', '1')
                else:
                    cfg.set('LOAD_CFG', 'verify', '0')
            cfg.set('LOAD_CFG', 'device', config['param']['comport_uart'])
            cfg.write(self.eflash_loader_cfg, 'w')
            bl60x_xtal = config['param']['chip_xtal']
            bflb_utils.printf('eflash loader bin is ' + get_eflash_loader(bl60x_xtal))
            eflash_loader_bin = os.path.join(chip_path, chipname, 'eflash_loader/' + get_eflash_loader(bl60x_xtal))
            if config['check_box']['single_download'] is True and act == 'download':
                cfg = BFConfigParser()
                cfg.read(self.eflash_loader_cfg)
                files_str = config['input_path']['img_bin_input']
                files_single = os.path.join(imgcreate_path, 'img_single.bin')
                shutil.copyfile(files_str, files_single)
                files_single = 'chips/' + chipname + '/img_create_iot/img_single.bin'
                addrs_str = config['param']['addr'].replace('0x', '')
                cfg.set('FLASH_CFG', 'file', files_single)
                cfg.set('FLASH_CFG', 'address', addrs_str)
                cfg.write(self.eflash_loader_cfg, 'w')
                self.eflash_loader_t = eflash_loader.BflbEflashLoader(chipname, chiptype)
                if not config['param']['comport_uart'] and config['param']['interface_type'] == 'uart':
                    error = '{"ErrorCode":"FFFF","ErrorMsg":"BFLB INTERFACE HAS NO COM PORT"}'
                    bflb_utils.printf(error)
                    return error
                if 'ckb_erase_all' in config['check_box']:
                    if config['check_box']['ckb_erase_all'] == 'True':
                        self.bl60x_mfg_flasher_erase_all(True)
                    else:
                        self.bl60x_mfg_flasher_erase_all(False)
                if config['param']['interface_type'] == 'uart':
                    options = ['--write', '--flash', '-p', uart]
                    if cfg.has_option('LOAD_CFG', 'boot2_isp_mode'):
                        boot2_isp_mode = cfg.get('LOAD_CFG', 'boot2_isp_mode')
                        if int(boot2_isp_mode) == 1:
                            options.extend(['--isp'])
                    args = parser_eflash.parse_args(options)
                    error = self.eflash_loader_t.efuse_flash_loader(args, self.eflash_loader_cfg, eflash_loader_bin, callback, None, None)
                    self.eflash_loader_t.object_status_clear()
                else:
                    options = ['--write', '--flash']
                    args = parser_eflash.parse_args(options)
                    error = self.eflash_loader_t.efuse_flash_loader(args, self.eflash_loader_cfg, eflash_loader_bin, callback, None, None)
                    self.eflash_loader_t.object_status_clear()
            elif self.flasher_download_cfg_ini_gen(chipname, chiptype, cpu_type, config) is True:
                if act == 'download':
                    self.eflash_loader_t = eflash_loader.BflbEflashLoader(chipname, chiptype)
                    self.eflash_loader_t.set_config_file(self.bh_cfg_file, '')
                    if not config['param']['comport_uart'] and config['param']['interface_type'] == 'uart':
                        error = '{"ErrorCode":"FFFF","ErrorMsg":"BFLB INTERFACE HAS NO COM PORT"}'
                        bflb_utils.printf(error)
                        return error
                    if 'ckb_erase_all' in config['check_box']:
                        if config['check_box']['ckb_erase_all'] == 'True':
                            self.bl60x_mfg_flasher_erase_all(True)
                        else:
                            self.bl60x_mfg_flasher_erase_all(False)
                    options = ['--write', '--flash']
                    if config['check_box']['encrypt'] is True or config['check_box']['sign'] is True:
                        options.extend(['--efuse'])
                        if config['check_box']['encrypt'] is True or config['check_box']['sign'] is True:
                            cfg_file = os.path.join(chip_path, chipname, 'img_create_iot', 'img_create_cfg.ini')
                            options.extend(['--createcfg=' + cfg_file])
                    if config['param']['interface_type'] == 'uart':
                        options.extend(['-p', uart])
                    if cfg.has_option('LOAD_CFG', 'boot2_isp_mode'):
                        boot2_isp_mode = cfg.get('LOAD_CFG', 'boot2_isp_mode')
                        if int(boot2_isp_mode) == 1:
                            options.extend(['--isp'])
                    args = parser_eflash.parse_args(options)
                    error = self.eflash_loader_t.efuse_flash_loader(args, self.eflash_loader_cfg, eflash_loader_bin, callback, self.create_simple_callback, None)
                    self.eflash_loader_t.object_status_clear()
            else:
                error = self.flasher_download_cfg_ini_gen(chipname, chiptype, cpu_type, config)
                bflb_utils.printf('Please check your partition table file')
        except Exception as e:
            traceback.print_exc(limit=10, file=sys.stdout)
            error = str(e)
        finally:
            return error

    def create_simple_callback(self):
        cpu_type = None
        if self.chipname in gol.cpu_type.keys():
            cpu_type = gol.cpu_type[self.chipname][0]
        values = self.config
        error = self.flasher_download_cfg_ini_gen(self.chipname, self.chiptype, cpu_type, values)
        if error is not True:
            bflb_utils.printf(error)
        return error

    def log_read_thread(self):
        try:
            (ret, data) = self.eflash_loader_t.log_read_process()
            self.eflash_loader_t.close_port()
            return (ret, data)
        except Exception as e:
            traceback.print_exc(limit=10, file=sys.stdout)
            ret = str(e)
            return (False, ret)

def flasher_download_cmd(args):
    config = toml.load(args.config)
    chipname = args.chipname
    chiptype = gol.dict_chip_cmd.get(chipname, 'unkown chip type')
    if chiptype not in ['bl60x', 'bl602', 'bl702', 'bl808', 'bl616', 'wb03']:
        bflb_utils.printf('Chip type is not in bl60x/bl602/bl702/bl808/bl616/wb03')
        return
    act = 'download'
    obj_iot = BflbIotTool(chipname, chiptype)
    obj_iot.flasher_download_thread(chipname, chiptype, act, config)

def iot_download_cmd(args):
    if args.firmware:
        firmware = args.firmware.replace('~', expanduser('~'))
    else:
        firmware = None
    if not firmware or not os.path.exists(firmware):
        bflb_utils.printf('firmware is not existed')
        return
    chipname = args.chipname.lower()
    chiptype = gol.dict_chip_cmd.get(chipname, 'unkown chip type')
    config = dict()
    config['param'] = dict()
    config['check_box'] = dict()
    config['input_path'] = dict()
    config['param']['interface_type'] = args.interface.lower()
    config['param']['comport_uart'] = args.port
    config['param']['speed_uart'] = str(args.baudrate)
    config['param']['speed_jlink'] = str(args.baudrate)
    config['param']['chip_xtal'] = args.xtal
    config['param']['aes_key'] = ''
    config['param']['aes_iv'] = ''
    config['check_box']['partition_download'] = True
    config['check_box']['bin_download'] = True
    config['check_box']['fw_download'] = True
    config['check_box']['boot2_download'] = True
    config['check_box']['media_download'] = False
    config['check_box']['romfs_download'] = False
    config['check_box']['mfg_download'] = False
    if chiptype == 'bl60x' or chiptype == 'bl602' or chiptype == 'bl702':
        config['check_box']['ckb_erase_all'] = str(args.erase)
    else:
        config['check_box']['ckb_erase_all'] = 'False'
    config['check_box']['encrypt'] = False
    config['check_box']['sign'] = False
    config['input_path']['cfg2_bin_input'] = firmware
    config['input_path']['fw_bin_input'] = firmware
    config['input_path']['boot2_bin_input'] = ''
    config['input_path']['media_bin_input'] = ''
    config['input_path']['romfs_dir_input'] = ''
    config['input_path']['mfg_bin_input'] = ''
    config['input_path']['publickey'] = ''
    config['input_path']['privatekey'] = ''
    config['check_box']['single_download'] = args.single
    config['input_path']['img_bin_input'] = firmware
    config['param']['addr'] = '0x' + args.addr.replace('0x', '')
    if chiptype == 'bl60x':
        if not args.boot2:
            config['input_path']['boot2_bin_input'] = os.path.join(chip_path, chipname, 'builtin_imgs', 'blsp_boot2.bin')
        else:
            config['input_path']['boot2_bin_input'] = args.boot2.replace('~', expanduser('~'))
            if not os.path.exists(config['input_path']['boot2_bin_input']):
                bflb_utils.printf('boot2 is not existed')
                return
        if not args.xtal:
            config['param']['chip_xtal'] = '38.4M'
        else:
            config['param']['chip_xtal'] = args.xtal
    elif chiptype == 'bl702':
        config['check_box']['boot2_download'] = False
        config['input_path']['boot2_bin_input'] = ''
        if not args.xtal:
            config['param']['chip_xtal'] = '32M'
        else:
            config['param']['chip_xtal'] = args.xtal
    elif chiptype == 'bl602' or chiptype == 'bl808' or chiptype == 'bl616' or (chiptype == 'wb03'):
        if not args.boot2:
            boot2_dir = find_boot2(os.path.join(chip_path, chipname, 'builtin_imgs'), 'boot2_isp_release.bin')
            if boot2_dir:
                config['input_path']['boot2_bin_input'] = boot2_dir
        else:
            config['input_path']['boot2_bin_input'] = args.boot2.replace('~', expanduser('~'))
            if not os.path.exists(config['input_path']['boot2_bin_input']):
                bflb_utils.printf('boot2 is not existed')
                return
        if not args.xtal:
            if chiptype == 'bl602':
                config['param']['chip_xtal'] = '40M'
            else:
                config['param']['chip_xtal'] = 'Auto'
        else:
            config['param']['chip_xtal'] = args.xtal
    else:
        bflb_utils.printf('Chip type is not correct')
        return
    if not args.pt:
        if chiptype == 'bl808':
            config['input_path']['pt_bin_input'] = os.path.join(chip_path, chipname, 'partition/partition_cfg_8M.toml')
        else:
            config['input_path']['pt_bin_input'] = os.path.join(chip_path, chipname, 'partition/partition_cfg_2M.toml')
    else:
        config['input_path']['pt_bin_input'] = args.pt.replace('~', expanduser('~'))
        if not os.path.exists(config['input_path']['pt_bin_input']):
            bflb_utils.printf('partition table is not existed')
            return
    if not args.version:
        config['param']['version'] = ''
    else:
        config['param']['version'] = args.version
    if not args.ota:
        config['param']['ota'] = os.path.join(chip_path, chipname, 'ota')
    else:
        config['param']['ota'] = args.ota
    if args.dts:
        config['check_box']['factory_download'] = True
        config['input_path']['factory_bin_input'] = args.dts.replace('~', expanduser('~'))
        config['check_box']['factory'] = True
        config['input_path']['dts_input'] = args.dts.replace('~', expanduser('~'))
        if not os.path.exists(config['input_path']['dts_input']):
            bflb_utils.printf('device tree is not existed')
            return
    if args.mfg:
        config['check_box']['mfg_download'] = True
        config['input_path']['mfg_bin_input'] = args.mfg.replace('~', expanduser('~'))
        if not os.path.exists(config['input_path']['mfg_bin_input']):
            bflb_utils.printf('mfg is not existed')
            return
    if args.media:
        config['check_box']['media_download'] = True
        config['input_path']['media_bin_input'] = args.media.replace('~', expanduser('~'))
        if not os.path.exists(config['input_path']['media_bin_input']):
            bflb_utils.printf('mfg is not existed')
            return
    if args.romfs:
        config['check_box']['romfs_download'] = True
        config['input_path']['romfs_dir_input'] = args.media.replace('~', expanduser('~'))
        if not os.path.exists(config['input_path']['romfs_dir_input']):
            bflb_utils.printf('romfs dir is not existed')
            return
    if config['param']['interface_type'].lower() == 'jlink' and args.baudrate > 12000:
        config['param']['speed_jlink'] = '12000'
    if args.build:
        act = 'build'
    else:
        act = 'download'
    obj_iot = BflbIotTool(chipname, chiptype)
    obj_iot.flasher_download_thread(chipname, chiptype, act, config)
    if act == 'build':
        f_org = os.path.join(chip_path, args.chipname, 'img_create_iot', 'whole_flash_data.bin')
        f = 'firmware.bin'
        try:
            shutil.copyfile(f_org, f)
        except Exception as error:
            pass

def run():
    port = None
    ports = []
    for item in get_serial_ports():
        ports.append(item['port'])
    if ports:
        try:
            port = sorted(ports, key=lambda x: int(re.match('COM(\\d+)', x).group(1)))[0]
        except Exception:
            port = sorted(ports)[0]
    parser = argparse.ArgumentParser(description='iot-tool')
    parser.add_argument('--chipname', required=True, help='chip name')
    parser.add_argument('--interface', dest='interface', default='uart', help='interface to use')
    parser.add_argument('--port', dest='port', default=port, help='serial port to use')
    parser.add_argument('--baudrate', dest='baudrate', default=115200, type=int, help='the speed at which to communicate')
    parser.add_argument('--xtal', dest='xtal', help='xtal type')
    parser.add_argument('--dts', dest='dts', help='device tree')
    parser.add_argument('--pt', dest='pt', help='partition table')
    parser.add_argument('--boot2', dest='boot2', help='boot2 bin')
    parser.add_argument('--firmware', dest='firmware', required=True, help='image to write')
    parser.add_argument('--mfg', dest='mfg', help='mfg bin')
    parser.add_argument('--media', dest='media', help='media bin')
    parser.add_argument('--romfs', dest='romfs', help='romfs dir')
    parser.add_argument('--build', dest='build', action='store_true', help='build image')
    parser.add_argument('--erase', dest='erase', action='store_true', help='chip erase')
    parser.add_argument('--single', dest='single', action='store_true', help='single download')
    parser.add_argument('--addr', dest='addr', default='0', help='address to write')
    parser.add_argument('--config', dest='config', help='config file')
    parser.add_argument('--ota', dest='ota', help='ota dir')
    parser.add_argument('--version', dest='version', help='version')
    args = parser.parse_args()
    bflb_utils.printf('==================================================')
    bflb_utils.printf('Chip name is %s' % args.chipname)
    gol.chip_name = args.chipname
    if conf_sign:
        reload(cgc)
    if args.port:
        bflb_utils.printf('Serial port is ' + args.port)
    elif port:
        bflb_utils.printf('Serial port is ' + port)
    else:
        bflb_utils.printf('Serial port is not found')
    bflb_utils.printf('Baudrate is ' + str(args.baudrate))
    bflb_utils.printf('Firmware is ' + str(args.firmware))
    bflb_utils.printf('Partition Table is ' + str(args.pt))
    bflb_utils.printf('Device Tree is ' + str(args.dts))
    bflb_utils.printf('Boot2 is ' + str(args.boot2))
    bflb_utils.printf('MFG is ' + str(args.mfg))
    bflb_utils.printf('Media is ' + str(args.media))
    bflb_utils.printf('Romfs Dir is ' + str(args.romfs))
    bflb_utils.printf('==================================================')
    if args.config:
        parser.set_defaults(func=flasher_download_cmd)
    else:
        parser.set_defaults(func=iot_download_cmd)
    args = parser.parse_args()
    args.func(args)
if __name__ == '__main__':
    print(sys.argv)
    run()