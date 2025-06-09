from .teamtv_object import TeamTVObject

class Person(TeamTVObject):

    @property
    def person_id(self):
        return self._person_id

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def gender(self):
        return self._gender

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def tags(self):
        return self._tags

    def __hash__(self):
        return hash(self.person_id)

    def __eq__(self, other):
        return isinstance(other, Person) and other.person_id == self.person_id

    def _use_attributes(self, attributes: dict):
        self._person_id = attributes['personId']
        self._first_name = attributes['firstName']
        self._last_name = attributes['lastName']
        self._gender = attributes['gender']
        self._tags = attributes.get('tags', {})

    def __repr__(self):
        return f"<Person name='{self.name}' person_id={self.person_id}>"