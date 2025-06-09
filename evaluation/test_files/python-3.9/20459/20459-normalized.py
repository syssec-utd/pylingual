def list_profiles_in(path):
    """list profiles in a given root directory"""
    files = os.listdir(path)
    profiles = []
    for f in files:
        full_path = os.path.join(path, f)
        if os.path.isdir(full_path) and f.startswith('profile_'):
            profiles.append(f.split('_', 1)[-1])
    return profiles