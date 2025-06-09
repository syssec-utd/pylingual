import re
from riscv_isac.log import logger
import riscv_isac.plugins as plugins
import riscv_isac.plugins.specification as spec
from riscv_isac.InstructionObject import instructionObject

class spike(spec.ParserSpec):

    @plugins.parserHookImpl
    def setup(self, trace, arch):
        self.trace = trace
        self.arch = arch
    instr_pattern_spike = re.compile('[0-9]\\s(?P<addr>[0-9abcdefx]+)\\s\\((?P<instr>[0-9abcdefx]+)\\)')
    instr_pattern_spike_xd = re.compile('[0-9]\\s(?P<addr>[0-9abcdefx]+)\\s\\((?P<instr>[0-9abcdefx]+)\\)' + '\\s(?P<regt>[xf])(?P<reg>[\\s|\\d]\\d)\\s(?P<val>[0-9abcdefx]+)')

    def extractInstruction(self, line):
        instr_pattern = self.instr_pattern_spike
        re_search = instr_pattern.search(line)
        if re_search is not None:
            return (int(re_search.group('instr'), 16), None)
        else:
            return (None, None)

    def extractAddress(self, line):
        instr_pattern = self.instr_pattern_spike
        re_search = instr_pattern.search(line)
        if re_search is not None:
            return int(re_search.group('addr'), 16)
        else:
            return 0

    def extractRegisterCommitVal(self, line):
        instr_pattern = self.instr_pattern_spike_xd
        re_search = instr_pattern.search(line)
        if re_search is not None:
            return (re_search.group('regt'), re_search.group('reg'), re_search.group('val'))
        else:
            return None

    @plugins.parserHookImpl
    def __iter__(self):
        with open(self.trace) as fp:
            for line in fp:
                logger.debug('parsing ' + str(line))
                instr, mnemonic = self.extractInstruction(line)
                addr = self.extractAddress(line)
                reg_commit = self.extractRegisterCommitVal(line)
                csr_commit = None
                instrObj = instructionObject(instr, 'None', addr, reg_commit=reg_commit, csr_commit=csr_commit, mnemonic=mnemonic)
                yield instrObj