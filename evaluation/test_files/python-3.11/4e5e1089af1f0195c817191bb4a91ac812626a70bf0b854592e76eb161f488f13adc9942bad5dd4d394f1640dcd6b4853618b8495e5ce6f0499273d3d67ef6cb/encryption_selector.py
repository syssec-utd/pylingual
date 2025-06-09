from licenseware.utils.logger import log
RULE_KEYS = ['values']
REQUIRED_DICT_KEYS = ['target', 'values', 'uploader_id']

class EncryptionSelector:
    """
    Get all encryption rules for an uploader.

    Encryption rules are a list[dict] shaped:

    {
        "target": any("filecontent", "filename", "columns"),
        "values": any("regex", "columns"),
        "description": "concise description for the rule",
        "uploader_id": "needs to match the uploader id from reg service"
    }
    Usage:

    ```py

    from licenseware.utils import EncryptionSelector

    encryption_rules = [
        {
            "target": "filecontent",
            "values": [r"Machine Name=(.*)", r"Device Name=(.*)"],
            "description": "encrypt device name",
            "uploader_id": "cpuq"
        },
    ]

    cpuq_encryption = EncryptionSelector(uploader_id="cpuq", encryption_rules=encryption_rules)
    filecontent_rules = cpuq_encryption.filecontent_rules
    filepaths_rules = cpuq_encryption.filepaths_rules
    columns_rules = cpuq_encryption.columns_rules
    ```
    """

    def __init__(self, uploader_id, encryption_rules):
        self.uploader_id = uploader_id
        self.encryption_rules = self._get_uploader_rules(encryption_rules)
        self.filecontent_rules = self.get_rule('filecontent')
        self.filepaths_rules = self.get_rule('filename')
        self.columns_rules = self.get_rule('columns')

    def _get_uploader_rules(self, encryption_rules):
        uploader_rules = []
        for d in encryption_rules:
            if not isinstance(d['uploader_id'], list):
                d['uploader_id'] = [d['uploader_id']]
            if self.uploader_id in d['uploader_id']:
                uploader_rules += [d]
        return uploader_rules

    def get_rule(self, rule_target):
        rules = []
        for rule in self.encryption_rules:
            if not all((key in rule for key in REQUIRED_DICT_KEYS)):
                log.error(f'Missing required dict keys for parsing rule: {rule}, skipping')
                continue
            if rule['target'] == rule_target:
                self.append_new_rule(new_rule=rule, rules=rules)
        return rules

    def append_new_rule(self, new_rule, rules):
        for key in RULE_KEYS:
            try:
                rules += new_rule[key] if isinstance(new_rule[key], list) else [new_rule[key]]
            except KeyError:
                pass
        return rules