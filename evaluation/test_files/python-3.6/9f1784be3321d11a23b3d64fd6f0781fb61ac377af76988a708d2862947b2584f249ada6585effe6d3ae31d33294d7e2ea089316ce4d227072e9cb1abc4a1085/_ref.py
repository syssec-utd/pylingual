import pathlib
import wmb
PACKAGE_DIR = pathlib.Path(wmb.__path__[0])
ENCODE_BLACKLIST_PATH = PACKAGE_DIR / 'files/mm10-blacklist.v2.bed.gz'
GENCODE_MM10_vm22 = PACKAGE_DIR / 'files/gencode.vM22.annotation.gene.flat.tsv.gz'
GENCODE_MM10_vm23 = PACKAGE_DIR / 'files/modified_gencode.vM23.primary_assembly.annotation.gene.flat.tsv.gz'