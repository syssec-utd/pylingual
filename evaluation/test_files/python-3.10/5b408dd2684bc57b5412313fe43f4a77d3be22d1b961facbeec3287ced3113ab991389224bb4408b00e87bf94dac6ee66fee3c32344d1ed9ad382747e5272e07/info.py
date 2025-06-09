import datetime
import sys
import os
import json
import argparse
import logging
from chainlib.chain import ChainSpec
from hexathon import add_0x, strip_0x, even
import sha3
from funga.eth.signer import EIP155Signer
from chainlib.settings import ChainSettings
from chainlib.eth.address import AddressChecksum
from chainlib.eth.chain import network_id
from chainlib.eth.block import block_latest, block_by_number, syncing, Block
from chainlib.eth.tx import count
from chainlib.eth.connection import EthHTTPConnection
from chainlib.eth.gas import OverrideGasOracle, balance, price
import chainlib.eth.cli
from chainlib.eth.cli.arg import Arg, ArgFlag, process_args
from chainlib.eth.cli.config import Config, process_config
from chainlib.eth.cli.log import process_log
from chainlib.eth.settings import process_settings
BLOCK_SAMPLES = 10
logg = logging.getLogger()
script_dir = os.path.dirname(os.path.realpath(__file__))
config_dir = os.path.join(script_dir, '..', 'data', 'config')
results_translation = {'network_id': 'Network Id', 'block': 'Block', 'syncing': 'Syncing', 'gas_limit': 'Gas Limit', 'gas_price': 'Gas Price', 'block_time': 'Block time'}

def process_config_local(config, arg, args, flags):
    config.add(args.local, '_LOCAL', False)
    config.add(args.long, '_LONG', False)
    config.add(None, '_ENTRY', False)
    if len(args.entry) > 0:
        config.add(args.entry[0], '_ENTRY', True)
        if config.get('_ENTRY') not in results_translation.keys():
            raise ValueError('Unknown entry {}'.format(config.get('_ENTRY')))
    return config
arg_flags = ArgFlag()
arg = Arg(arg_flags)
flags = arg_flags.STD_READ | arg_flags.ENV
argparser = chainlib.eth.cli.ArgumentParser()
argparser = process_args(argparser, arg, flags)
argparser.add_argument('--long', action='store_true', help='Calculate averages through sampling of blocks and txs')
argparser.add_argument('--local', action='store_true', help='Include local info')
argparser.add_argument('entry', nargs='?', help='Output single item')
args = argparser.parse_args()
logg = process_log(args, logg)
config = Config()
config = process_config(config, arg, args, flags)
config = process_config_local(config, arg, args, flags)
logg.debug('config loaded:\n{}'.format(config))
settings = ChainSettings()
settings = process_settings(settings, config)
logg.debug('settings loaded:\n{}'.format(settings))

def set_result(results, k, v, w=sys.stdout):
    kt = results_translation[k]
    if str(config.get('_ENTRY')) == k:
        w.write('{}'.format(v))
        return True
    logg.info('{}: {}\n'.format(kt, v))
    results[k] = v
    return False

def main():
    human = not config.true('_RAW')
    results = {}
    o = network_id(id_generator=settings.get('RPC_ID_GENERATOR'))
    r = settings.get('CONN').do(o)
    if set_result(results, 'network_id', r):
        return
    o = block_latest(id_generator=settings.get('RPC_ID_GENERATOR'))
    r = settings.get('CONN').do(o)
    try:
        n = int(r, 16)
    except ValueError:
        n = int(r)
    first_block_number = n
    if human:
        n = format(n, ',')
    if set_result(results, 'block', n):
        return
    o = block_by_number(first_block_number, False, id_generator=settings.get('RPC_ID_GENERATOR'))
    r = settings.get('CONN').do(o)
    last_block = Block(r)
    last_timestamp = last_block.timestamp
    if config.true('_LONG'):
        aggr_time = 0.0
        aggr_gas = 0
        for i in range(BLOCK_SAMPLES):
            o = block_by_number(first_block_number - i, False, id_generator=settings.get('RPC_ID_GENERATOR'))
            r = settings.get('CONN').do(o)
            block = Block(r)
            aggr_time += last_block.timestamp - block.timestamp
            gas_limit = int(r['gasLimit'], 16)
            aggr_gas += gas_limit
            last_block = block
            last_timestamp = block.timestamp
        n = int(aggr_gas / BLOCK_SAMPLES)
        if human:
            n = format(n, ',')
        if set_result(results, 'gas_limit', n):
            return
        if set_result(results, 'block_time', aggr_time / BLOCK_SAMPLES):
            return
    o = price(id_generator=settings.get('RPC_ID_GENERATOR'))
    r = settings.get('CONN').do(o)
    n = int(r, 16)
    if human:
        n = format(n, ',')
    if set_result(results, 'gas_price', n):
        return
    if config.get('_LOCAL'):
        o = syncing()
        r = settings.get('CONN').do(o)
        if set_result(results, 'syncing', r):
            return
    if config.get('_ENTRY') != None:
        raise RuntimeError('entry {} ({}) not processed, please review the flag settings'.format(config.get('_ENTRY'), results_translation[config.get('_ENTRY')]))
    for k in results.keys():
        kt = results_translation[k]
        sys.stdout.write('{}: {}\n'.format(kt, results[k]))
if __name__ == '__main__':
    main()