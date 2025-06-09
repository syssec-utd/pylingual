def from_multiple(cls, sections, parent_name=None, child_name=None, is_list=True):
    """
        :type parent_name: str
        :type sections: list of Section
        """
    if len(sections) == 1:
        return sections[0]
    if parent_name:
        master_section = filter(lambda section: section.name == parent_name, sections)[0]
        rest = filter(lambda section: section.name != parent_name, sections)
    else:
        master_section = sections[0]
        parent_name = master_section.name
        rest = sections[1:]
    child = {'multi': [section.get_cfg_dict(with_meta=False) for section in rest]} if is_list else {child_name: cls._select_one(master_section, rest).get_cfg_dict(with_meta=False)}
    master_section.merged_options.update(child)
    return master_section