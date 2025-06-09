def _add_category(self, categories):
    """ categories variable must be a list """
    categories_obj = self.vcard.add('categories')
    categories_obj.value = helpers.convert_to_vcard('category', categories, ObjectType.list_with_strings)