def search_all(self):
    """a "show all" search that doesn't require a query"""
    results = []
    for entry in self.dbx.files_list_folder('').entries:
        for item in self.dbx.files_list_folder(entry.path_lower).entries:
            name = item.name.replace('.simg', '')
            results.append(['%s/%s' % (entry.name, name)])
    if len(results) == 0:
        bot.info('No container collections found.')
        sys.exit(1)
    bot.info('Collections')
    bot.table(results)
    return results