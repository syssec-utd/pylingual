def get_cloud_default_index_settings():
    """
    Diverges from default in:
        - number_of_shards
    """
    return {'index_defaults': {'treat_urls_and_pointers_as_images': False, 'model': 'hf/all_datasets_v4_MiniLM-L6', 'normalize_embeddings': True, 'text_preprocessing': {'split_length': 2, 'split_overlap': 0, 'split_method': 'sentence'}, 'image_preprocessing': {'patch_method': None}}, 'number_of_shards': 2, 'number_of_replicas': 1}