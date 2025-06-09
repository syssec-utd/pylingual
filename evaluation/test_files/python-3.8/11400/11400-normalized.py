def archive_info(database: Database, archive_case: dict) -> dict:
    """Get information about a case from archive."""
    data = {'collaborators': archive_case['collaborators'], 'synopsis': archive_case.get('synopsis'), 'assignees': [], 'suspects': [], 'causatives': [], 'phenotype_terms': [], 'phenotype_groups': []}
    if archive_case.get('assignee'):
        archive_user = database.user.find_one({'_id': archive_case['assignee']})
        data['assignee'].append(archive_user['email'])
    for key in ['suspects', 'causatives']:
        for variant_id in archive_case.get(key, []):
            archive_variant = database.variant.find_one({'_id': variant_id})
            data[key].append({'chromosome': archive_variant['chromosome'], 'position': archive_variant['position'], 'reference': archive_variant['reference'], 'alternative': archive_variant['alternative'], 'variant_type': archive_variant['variant_type']})
    for key in ['phenotype_terms', 'phenotype_groups']:
        for archive_term in archive_case.get(key, []):
            data[key].append({'phenotype_id': archive_term['phenotype_id'], 'feature': archive_term['feature']})
    return data