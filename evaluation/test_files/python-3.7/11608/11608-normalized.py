def build_variant(variant, institute_id, gene_to_panels=None, hgncid_to_gene=None, sample_info=None):
    """Build a variant object based on parsed information

        Args:
            variant(dict)
            institute_id(str)
            gene_to_panels(dict): A dictionary with
                {<hgnc_id>: {
                    'panel_names': [<panel_name>, ..],
                    'disease_associated_transcripts': [<transcript_id>, ..]
                    }
                    .
                    .
                }

            hgncid_to_gene(dict): A dictionary with
                {<hgnc_id>: <hgnc_gene info>
                    .
                    .
                }
            sample_info(dict): A dictionary with info about samples.
                               Strictly for cancer to tell which is tumor


        Returns:
            variant_obj(dict)

        variant = dict(
            # document_id is a md5 string created by institute_genelist_caseid_variantid:
            _id = str, # required, same as document_id
            document_id = str, # required
            # variant_id is a md5 string created by chrom_pos_ref_alt (simple_id)
            variant_id = str, # required
            # display name is variant_id (no md5)
            display_name = str, # required

            # chrom_pos_ref_alt
            simple_id = str,
            # The variant can be either research or clinical.
            # For research variants we display all the available information while
            # the clinical variants have limited annotation fields.
            variant_type = str, # required, choices=('research', 'clinical'))

            category = str, # choices=('sv', 'snv', 'str')
            sub_category = str, # choices=('snv', 'indel', 'del', 'ins', 'dup', 'inv', 'cnv', 'bnd')
            mate_id = str, # For SVs this identifies the other end

            case_id = str, # case_id is a string like owner_caseid
            chromosome = str, # required
            position = int, # required
            end = int, # required
            length = int, # required
            reference = str, # required
            alternative = str, # required

            rank_score = float, # required
            variant_rank = int, # required
            rank_score_results = list, # List if dictionaries
            variant_rank = int, # required

            institute = str, # institute_id, required

            sanger_ordered = bool,
            validation = str, # Sanger validation, choices=('True positive', 'False positive')

            quality = float,
            filters = list, # list of strings
            samples = list, # list of dictionaries that are <gt_calls>
            genetic_models = list, # list of strings choices=GENETIC_MODELS
            compounds = list, # sorted list of <compound> ordering='combined_score'

            genes = list, # list with <gene>
            dbsnp_id = str,

            # Gene ids:
            hgnc_ids = list, # list of hgnc ids (int)
            hgnc_symbols = list, # list of hgnc symbols (str)
            panels = list, # list of panel names that the variant ovelapps

            # Frequencies:
            thousand_genomes_frequency = float,
            thousand_genomes_frequency_left = float,
            thousand_genomes_frequency_right = float,
            exac_frequency = float,
            max_thousand_genomes_frequency = float,
            max_exac_frequency = float,
            local_frequency = float,
            local_obs_old = int,
            local_obs_hom_old = int,
            local_obs_total_old = int, # default=638

            # Predicted deleteriousness:
            cadd_score = float,
            clnsig = list, # list of <clinsig>
            spidex = float,

            missing_data = bool, # default False
            
            # STR specific information
            str_repid = str, repeat id generally corresponds to gene symbol
            str_ru = str, used e g in PanelApp naming of STRs
            str_ref = int, reference copy number
            str_len = int, number of repeats found in case
            str_status = str, this indicates the severity of the expansion level

            # Callers
            gatk = str, # choices=VARIANT_CALL, default='Not Used'
            samtools = str, # choices=VARIANT_CALL, default='Not Used'
            freebayes = str, # choices=VARIANT_CALL, default='Not Used'

            # Conservation:
            phast_conservation = list, # list of str, choices=CONSERVATION
            gerp_conservation = list, # list of str, choices=CONSERVATION
            phylop_conservation = list, # list of str, choices=CONSERVATION
            # Database options:
            gene_lists = list,
            manual_rank = int, # choices=[0, 1, 2, 3, 4, 5]
            dismiss_variant = list,

            acmg_evaluation = str, # choices=ACMG_TERMS
        )

    """
    gene_to_panels = gene_to_panels or {}
    hgncid_to_gene = hgncid_to_gene or {}
    sample_info = sample_info or {}
    variant_obj = dict(_id=variant['ids']['document_id'], document_id=variant['ids']['document_id'], variant_id=variant['ids']['variant_id'], display_name=variant['ids']['display_name'], variant_type=variant['variant_type'], case_id=variant['case_id'], chromosome=variant['chromosome'], reference=variant['reference'], alternative=variant['alternative'], institute=institute_id)
    variant_obj['missing_data'] = False
    variant_obj['position'] = int(variant['position'])
    variant_obj['rank_score'] = float(variant['rank_score'])
    end = variant.get('end')
    if end:
        variant_obj['end'] = int(end)
    length = variant.get('length')
    if length:
        variant_obj['length'] = int(length)
    variant_obj['simple_id'] = variant['ids'].get('simple_id')
    variant_obj['quality'] = float(variant['quality']) if variant['quality'] else None
    variant_obj['filters'] = variant['filters']
    variant_obj['dbsnp_id'] = variant.get('dbsnp_id')
    variant_obj['cosmic_ids'] = variant.get('cosmic_ids')
    variant_obj['category'] = variant['category']
    variant_obj['sub_category'] = variant.get('sub_category')
    if 'mate_id' in variant:
        variant_obj['mate_id'] = variant['mate_id']
    if 'cytoband_start' in variant:
        variant_obj['cytoband_start'] = variant['cytoband_start']
    if 'cytoband_end' in variant:
        variant_obj['cytoband_end'] = variant['cytoband_end']
    if 'end_chrom' in variant:
        variant_obj['end_chrom'] = variant['end_chrom']
    if 'str_ru' in variant:
        variant_obj['str_ru'] = variant['str_ru']
    if 'str_repid' in variant:
        variant_obj['str_repid'] = variant['str_repid']
    if 'str_ref' in variant:
        variant_obj['str_ref'] = variant['str_ref']
    if 'str_len' in variant:
        variant_obj['str_len'] = variant['str_len']
    if 'str_status' in variant:
        variant_obj['str_status'] = variant['str_status']
    gt_types = []
    for sample in variant.get('samples', []):
        gt_call = build_genotype(sample)
        gt_types.append(gt_call)
        if sample_info:
            sample_id = sample['individual_id']
            if sample_info[sample_id] == 'case':
                key = 'tumor'
            else:
                key = 'normal'
            variant_obj[key] = {'alt_depth': sample['alt_depth'], 'ref_depth': sample['ref_depth'], 'read_depth': sample['read_depth'], 'alt_freq': sample['alt_frequency'], 'ind_id': sample_id}
    variant_obj['samples'] = gt_types
    if 'genetic_models' in variant:
        variant_obj['genetic_models'] = variant['genetic_models']
    compounds = []
    for compound in variant.get('compounds', []):
        compound_obj = build_compound(compound)
        compounds.append(compound_obj)
    if compounds:
        variant_obj['compounds'] = compounds
    genes = []
    for (index, gene) in enumerate(variant.get('genes', [])):
        if gene.get('hgnc_id'):
            gene_obj = build_gene(gene, hgncid_to_gene)
            genes.append(gene_obj)
            if index > 30:
                variant_obj['missing_data'] = True
                break
    if genes:
        variant_obj['genes'] = genes
    if 'hgnc_ids' in variant:
        variant_obj['hgnc_ids'] = [hgnc_id for hgnc_id in variant['hgnc_ids'] if hgnc_id]
    hgnc_symbols = []
    for hgnc_id in variant_obj['hgnc_ids']:
        gene_obj = hgncid_to_gene.get(hgnc_id)
        if gene_obj:
            hgnc_symbols.append(gene_obj['hgnc_symbol'])
    if hgnc_symbols:
        variant_obj['hgnc_symbols'] = hgnc_symbols
    panel_names = set()
    for hgnc_id in variant_obj['hgnc_ids']:
        gene_panels = gene_to_panels.get(hgnc_id, set())
        panel_names = panel_names.union(gene_panels)
    if panel_names:
        variant_obj['panels'] = list(panel_names)
    clnsig_objects = []
    for entry in variant.get('clnsig', []):
        clnsig_obj = build_clnsig(entry)
        clnsig_objects.append(clnsig_obj)
    if clnsig_objects:
        variant_obj['clnsig'] = clnsig_objects
    call_info = variant.get('callers', {})
    for caller in call_info:
        if call_info[caller]:
            variant_obj[caller] = call_info[caller]
    conservation_info = variant.get('conservation', {})
    if conservation_info.get('phast'):
        variant_obj['phast_conservation'] = conservation_info['phast']
    if conservation_info.get('gerp'):
        variant_obj['gerp_conservation'] = conservation_info['gerp']
    if conservation_info.get('phylop'):
        variant_obj['phylop_conservation'] = conservation_info['phylop']
    if variant.get('azlength'):
        variant_obj['azlength'] = variant['azlength']
    if variant.get('azqual'):
        variant_obj['azqual'] = variant['azqual']
    frequencies = variant.get('frequencies', {})
    if frequencies.get('thousand_g'):
        variant_obj['thousand_genomes_frequency'] = float(frequencies['thousand_g'])
    if frequencies.get('thousand_g_max'):
        variant_obj['max_thousand_genomes_frequency'] = float(frequencies['thousand_g_max'])
    if frequencies.get('exac'):
        variant_obj['exac_frequency'] = float(frequencies['exac'])
    if frequencies.get('exac_max'):
        variant_obj['max_exac_frequency'] = float(frequencies['exac_max'])
    if frequencies.get('gnomad'):
        variant_obj['gnomad_frequency'] = float(frequencies['gnomad'])
    if frequencies.get('gnomad_max'):
        variant_obj['max_gnomad_frequency'] = float(frequencies['gnomad_max'])
    if frequencies.get('thousand_g_left'):
        variant_obj['thousand_genomes_frequency_left'] = float(frequencies['thousand_g_left'])
    if frequencies.get('thousand_g_right'):
        variant_obj['thousand_genomes_frequency_right'] = float(frequencies['thousand_g_right'])
    if variant.get('local_obs_old'):
        variant_obj['local_obs_old'] = variant['local_obs_old']
    if variant.get('local_obs_hom_old'):
        variant_obj['local_obs_hom_old'] = variant['local_obs_hom_old']
    if frequencies.get('clingen_cgh_benign'):
        variant_obj['clingen_cgh_benign'] = frequencies['clingen_cgh_benign']
    if frequencies.get('clingen_cgh_pathogenic'):
        variant_obj['clingen_cgh_pathogenic'] = frequencies['clingen_cgh_pathogenic']
    if frequencies.get('clingen_ngi'):
        variant_obj['clingen_ngi'] = frequencies['clingen_ngi']
    if frequencies.get('swegen'):
        variant_obj['swegen'] = frequencies['swegen']
    if frequencies.get('decipher'):
        variant_obj['decipher'] = frequencies['decipher']
    elif frequencies.get('decipherAF'):
        variant_obj['decipher'] = frequencies['decipherAF']
    if variant.get('cadd_score'):
        variant_obj['cadd_score'] = variant['cadd_score']
    if variant.get('spidex'):
        variant_obj['spidex'] = variant['spidex']
    rank_results = []
    for category in variant.get('rank_result', []):
        rank_result = {'category': category, 'score': variant['rank_result'][category]}
        rank_results.append(rank_result)
    if rank_results:
        variant_obj['rank_score_results'] = rank_results
    if variant.get('mvl_tag'):
        variant_obj['mvl_tag'] = True
    return variant_obj