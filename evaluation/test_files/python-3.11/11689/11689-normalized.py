def parse_gene_panel(path, institute='cust000', panel_id='test', panel_type='clinical', date=datetime.now(), version=1.0, display_name=None, genes=None):
    """Parse the panel info and return a gene panel

        Args:
            path(str): Path to panel file
            institute(str): Name of institute that owns the panel
            panel_id(str): Panel id
            date(datetime.datetime): Date of creation
            version(float)
            full_name(str): Option to have a long name

        Returns:
            gene_panel(dict)
    """
    LOG.info('Parsing gene panel %s', panel_id)
    gene_panel = {}
    gene_panel['path'] = path
    gene_panel['type'] = panel_type
    gene_panel['date'] = date
    gene_panel['panel_id'] = panel_id
    gene_panel['institute'] = institute
    version = version or 1.0
    gene_panel['version'] = float(version)
    gene_panel['display_name'] = display_name or panel_id
    if not path:
        panel_handle = genes
    else:
        panel_handle = get_file_handle(gene_panel['path'])
    gene_panel['genes'] = parse_genes(gene_lines=panel_handle)
    return gene_panel