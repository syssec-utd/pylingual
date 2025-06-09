def build_core_type(s_cdt):
    """
    Build an xsd simpleType out of a S_CDT.
    """
    s_dt = nav_one(s_cdt).S_DT[17]()
    if s_dt.name == 'void':
        type_name = None
    elif s_dt.name == 'boolean':
        type_name = 'xs:boolean'
    elif s_dt.name == 'integer':
        type_name = 'xs:integer'
    elif s_dt.name == 'real':
        type_name = 'xs:decimal'
    elif s_dt.name == 'string':
        type_name = 'xs:string'
    elif s_dt.name == 'unique_id':
        type_name = 'xs:integer'
    else:
        type_name = None
    if type_name:
        mapped_type = ET.Element('xs:simpleType', name=s_dt.name)
        ET.SubElement(mapped_type, 'xs:restriction', base=type_name)
        return mapped_type