def sync_labels(self, repo):
    """Creates a local map of github labels/milestones to asana tags."""
    logging.info('syncing new github.com labels to tags')
    ltm = self.app.data.get('label-tag-map', {})
    for label in repo.get_labels():
        tag_id = ltm.get(label.name, None)
        if tag_id is None:
            tag = self.app.asana.tags.create(name=label.name, workspace=self.asana_ws_id, notes='gh: %s' % label.url)
            logging.info('\t%s => tag %d', label.name, tag['id'])
            ltm[label.name] = tag['id']
    for ms in repo.get_milestones(state='all'):
        tag_id = ltm.get(_ms_label(ms.id), None)
        if tag_id is None:
            tag = self.app.asana.tags.create(name=ms.title, workspace=self.asana_ws_id, notes='gh: %s' % ms.url)
            logging.info('\t%s => tag %d', ms.title, tag['id'])
            ltm[_ms_label(ms.id)] = tag['id']
    self.app.data['label-tag-map'] = ltm
    return ltm