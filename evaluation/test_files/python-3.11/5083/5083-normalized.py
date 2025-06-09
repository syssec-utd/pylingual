def store(self, uri, payload, headers, data):
    """Store a raw item in this archive.

        The method will store `data` content in this archive. The unique
        identifier for that item will be generated using the rest of the
        parameters.

        :param uri: request URI
        :param payload: request payload
        :param headers: request headers
        :param data: data to store in this archive

        :raises ArchiveError: when an error occurs storing the given data
        """
    hashcode = self.make_hashcode(uri, payload, headers)
    payload_dump = pickle.dumps(payload, 0)
    headers_dump = pickle.dumps(headers, 0)
    data_dump = pickle.dumps(data, 0)
    logger.debug('Archiving %s with %s %s %s in %s', hashcode, uri, payload, headers, self.archive_path)
    try:
        cursor = self._db.cursor()
        insert_stmt = 'INSERT INTO ' + self.ARCHIVE_TABLE + ' (id, hashcode, uri, payload, headers, data) VALUES(?,?,?,?,?,?)'
        cursor.execute(insert_stmt, (None, hashcode, uri, payload_dump, headers_dump, data_dump))
        self._db.commit()
        cursor.close()
    except sqlite3.IntegrityError as e:
        msg = 'data storage error; cause: duplicated entry %s' % hashcode
        raise ArchiveError(cause=msg)
    except sqlite3.DatabaseError as e:
        msg = 'data storage error; cause: %s' % str(e)
        raise ArchiveError(cause=msg)
    logger.debug('%s data archived in %s', hashcode, self.archive_path)