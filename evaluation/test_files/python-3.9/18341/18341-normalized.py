def _get_class_definition(self):
    """Builds the class definition of the parser."""
    fmt = 'class Parser({parser_base}):\n             {indent}"""This class contains methods for reading source code and generating a parse tree."""\n             {indent}entry_point = "{entry_point}"\n\n             {rule_definitions}\n             '
    fmt = self._clean_fmt(fmt)
    return fmt.format(parser_base=self._get_parser_base(), indent=self.indent, entry_point=self._get_entry_point(), rule_definitions='\n'.join(self._get_rule_definitions()))