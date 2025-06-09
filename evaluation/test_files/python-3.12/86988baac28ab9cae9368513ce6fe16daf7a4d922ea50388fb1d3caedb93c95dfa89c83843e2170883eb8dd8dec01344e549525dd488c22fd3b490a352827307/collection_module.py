from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = '\n---\nmodule: collection_module\nshort_description: Test collection module\ndescription:\n  - This is a test module in a local collection.\nauthor: "Felix Fontein (@felixfontein)"\noptions: {}\n'
EXAMPLES = ' # '
RETURN = ' # '
from ansible.module_utils.basic import AnsibleModule

def main():
    AnsibleModule(argument_spec={}).exit_json()
if __name__ == '__main__':
    main()