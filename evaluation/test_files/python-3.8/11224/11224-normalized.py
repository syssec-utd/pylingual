def parse_coordinates(variant, category):
    """Find out the coordinates for a variant

    Args:
        variant(cyvcf2.Variant)

    Returns:
        coordinates(dict): A dictionary on the form:
        {
            'position':<int>,
            'end':<int>,
            'end_chrom':<str>,
            'length':<int>,
            'sub_category':<str>,
            'mate_id':<str>,
            'cytoband_start':<str>,
            'cytoband_end':<str>,
        }
    """
    ref = variant.REF
    if variant.ALT:
        alt = variant.ALT[0]
    if category == 'str' and (not variant.ALT):
        alt = '.'
    chrom_match = CHR_PATTERN.match(variant.CHROM)
    chrom = chrom_match.group(2)
    svtype = variant.INFO.get('SVTYPE')
    if svtype:
        svtype = svtype.lower()
    mate_id = variant.INFO.get('MATEID')
    svlen = variant.INFO.get('SVLEN')
    svend = variant.INFO.get('END')
    snvend = int(variant.end)
    position = int(variant.POS)
    ref_len = len(ref)
    alt_len = len(alt)
    sub_category = get_sub_category(alt_len, ref_len, category, svtype)
    end = get_end(position, alt, category, snvend, svend)
    length = get_length(alt_len, ref_len, category, position, end, svtype, svlen)
    end_chrom = chrom
    if sub_category == 'bnd':
        if ':' in alt:
            match = BND_ALT_PATTERN.match(alt)
            if match:
                other_chrom = match.group(1)
                match = CHR_PATTERN.match(other_chrom)
                end_chrom = match.group(2)
    cytoband_start = get_cytoband_coordinates(chrom, position)
    cytoband_end = get_cytoband_coordinates(end_chrom, end)
    coordinates = {'position': position, 'end': end, 'length': length, 'sub_category': sub_category, 'mate_id': mate_id, 'cytoband_start': cytoband_start, 'cytoband_end': cytoband_end, 'end_chrom': end_chrom}
    return coordinates