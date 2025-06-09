def po_to_csv_merge(languages, locale_root, po_files_path, local_trans_csv, local_meta_csv, gdocs_trans_csv, gdocs_meta_csv):
    """
    Converts po file to csv GDocs spreadsheet readable format.
    Merges them if some msgid aren't in the spreadsheet.
    :param languages: list of language codes
    :param locale_root: path to locale root folder containing directories
                        with languages
    :param po_files_path: path from lang directory to po file
    :param local_trans_csv: path where local csv with translations
                            will be created
    :param local_meta_csv: path where local csv with metadata will be created
    :param gdocs_trans_csv: path to gdoc csv with translations
    """
    msgids = []
    trans_reader = UnicodeReader(gdocs_trans_csv)
    meta_reader = UnicodeReader(gdocs_meta_csv)
    try:
        trans_title = trans_reader.next()
        meta_title = meta_reader.next()
    except StopIteration:
        trans_title = ['file', 'comment', 'msgid']
        trans_title += map(lambda s: s + ':msgstr', languages)
        meta_title = ['metadata']
    (trans_writer, meta_writer) = _get_new_csv_writers(trans_title, meta_title, local_trans_csv, local_meta_csv)
    for (trans_row, meta_row) in izip_longest(trans_reader, meta_reader):
        msgids.append(trans_row[2])
        trans_writer.writerow(trans_row)
        meta_writer.writerow(meta_row if meta_row else [METADATA_EMPTY])
    trans_reader.close()
    meta_reader.close()
    po_files = _get_all_po_filenames(locale_root, languages[0], po_files_path)
    new_trans = False
    for po_filename in po_files:
        new_msgstrs = {}
        for lang in languages[1:]:
            po_file_path = os.path.join(locale_root, lang, po_files_path, po_filename)
            if not os.path.exists(po_file_path):
                open(po_file_path, 'a').close()
            new_msgstrs[lang] = _get_new_msgstrs(po_file_path, msgids)
        if len(new_msgstrs[languages[1]].keys()) > 0:
            new_trans = True
            po_file_path = os.path.join(locale_root, languages[0], po_files_path, po_filename)
            _write_new_messages(po_file_path, trans_writer, meta_writer, msgids, new_msgstrs, languages)
    trans_writer.close()
    meta_writer.close()
    return new_trans