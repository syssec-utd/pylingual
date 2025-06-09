def transform_multidim_to_1d_decl(decl):
    """
    Transform ast of multidimensional declaration to a single dimension declaration.

    In-place operation!

    Returns name and dimensions of array (to be used with transform_multidim_to_1d_ref())
    """
    dims = []
    type_ = decl.type
    while type(type_) is c_ast.ArrayDecl:
        dims.append(type_.dim)
        type_ = type_.type
    if dims:
        decl.type.dim = reduce(lambda l, r: c_ast.BinaryOp('*', l, r), dims)
        decl.type.type = type_
    return (decl.name, dims)