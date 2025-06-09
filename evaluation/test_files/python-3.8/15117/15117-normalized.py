def project_data(self, project):
    """Return a list of Data objects for given project.

        :param project: ObjectId or slug of Genesis project
        :type project: string
        :rtype: list of Data objects

        """
    projobjects = self.cache['project_objects']
    objects = self.cache['objects']
    project_id = str(project)
    if not re.match('^[0-9a-fA-F]{24}$', project_id):
        projects = self.api.case.get(url_slug=project_id)['objects']
        if len(projects) != 1:
            raise ValueError(msg='Attribute project not a slug or ObjectId: {}'.format(project_id))
        project_id = str(projects[0]['id'])
    if project_id not in projobjects:
        projobjects[project_id] = []
        data = self.api.data.get(case_ids__contains=project_id)['objects']
        for d in data:
            _id = d['id']
            if _id in objects:
                objects[_id].update(d)
            else:
                objects[_id] = GenData(d, self)
            projobjects[project_id].append(objects[_id])
        for d in projobjects[project_id]:
            while True:
                ref_annotation = {}
                remove_annotation = []
                for (path, ann) in d.annotation.items():
                    if ann['type'].startswith('data:'):
                        if ann['value'] in self.cache['objects']:
                            annotation = self.cache['objects'][ann['value']].annotation
                            ref_annotation.update({path + '.' + k: v for (k, v) in annotation.items()})
                        remove_annotation.append(path)
                if ref_annotation:
                    d.annotation.update(ref_annotation)
                    for path in remove_annotation:
                        del d.annotation[path]
                else:
                    break
    return projobjects[project_id]