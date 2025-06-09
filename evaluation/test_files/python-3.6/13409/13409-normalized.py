def get_import(self, sym: sym.Symbol) -> Optional[types.ModuleType]:
    """Return the module if a moduled named by sym has been imported into
        this Namespace, None otherwise.

        First try to resolve a module directly with the given name. If no module
        can be resolved, attempt to resolve the module using import aliases."""
    mod = self.imports.entry(sym, None)
    if mod is None:
        alias = self.import_aliases.get(sym, None)
        if alias is None:
            return None
        return self.imports.entry(alias, None)
    return mod