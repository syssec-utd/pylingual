def _get_json_content_from_folder(folder):
    """yield objects from json files in the folder and subfolders."""
    for (dirpath, dirnames, filenames) in os.walk(folder):
        for filename in filenames:
            if filename.lower().endswith('.json'):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'rb') as file:
                    yield json.loads(file.read().decode('UTF-8'))