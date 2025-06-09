def _rewrite_and_copy(src_file, dst_file, project_name):
    """Replace vars and copy."""
    fh, abs_path = mkstemp()
    with io.open(abs_path, 'w', encoding='utf-8') as new_file:
        with io.open(src_file, 'r', encoding='utf-8') as old_file:
            for line in old_file:
                new_line = line.replace('#{project}', project_name).replace('#{project|title}', project_name.title())
                new_file.write(new_line)
    shutil.copy(abs_path, dst_file)
    os.close(fh)