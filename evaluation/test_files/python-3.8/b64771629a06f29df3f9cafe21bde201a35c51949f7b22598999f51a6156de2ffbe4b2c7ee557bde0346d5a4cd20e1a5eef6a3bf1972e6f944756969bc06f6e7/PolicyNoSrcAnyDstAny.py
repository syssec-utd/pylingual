from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories

class PolicyNoSrcAnyDstAny(BaseResourceCheck):

    def __init__(self):
        name = "Ensure security rules do not have 'source_addresses' and 'destination_addresses' both containing values of 'any' "
        id = 'CKV_PAN_7'
        supported_resources = ['panos_security_policy', 'panos_security_rule_group']
        categories = [CheckCategories.NETWORKING]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        if 'rule' in conf:
            self.evaluated_keys = ['rule']
            rules = conf.get('rule')
            for secrule in rules:
                if 'source_addresses' in secrule:
                    source_addresses = secrule.get('source_addresses')
                    for src_address in source_addresses[0]:
                        if src_address == 'any':
                            if 'destination_addresses' in secrule:
                                destination_addresses = secrule.get('destination_addresses')
                                for dst_address in destination_addresses[0]:
                                    if dst_address == 'any':
                                        return CheckResult.FAILED
                            else:
                                return CheckResult.FAILED
                else:
                    return CheckResult.FAILED
            return CheckResult.PASSED
        return CheckResult.UNKNOWN
check = PolicyNoSrcAnyDstAny()