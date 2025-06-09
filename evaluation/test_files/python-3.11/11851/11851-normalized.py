def to_python_package(classes, target_folder, parent_package=None, indent=DEFAULT_INDENT):
    """
    This function can be used to build a python package representation of pyschema classes.
    One module is created per namespace in a package matching the namespace hierarchy.

    Args:
        classes: A collection of classes to build the package from
        target_folder: Root folder of the package
        parent_package: Prepended on all import statements in order to support absolute imports.
            parent_package is not used when building the package file structure
        indent: Indent level. Defaults to 4 spaces
    """
    PackageBuilder(target_folder, parent_package, indent).from_classes_with_refs(classes)