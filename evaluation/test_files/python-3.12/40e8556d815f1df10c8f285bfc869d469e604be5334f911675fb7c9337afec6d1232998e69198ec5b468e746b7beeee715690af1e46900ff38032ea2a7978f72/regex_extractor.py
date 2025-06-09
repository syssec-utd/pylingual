import regex as re
from kolibri.core.entity import Entity

class RegexExtractor:

    def __init__(self, exclusion_list=[], regexes=[], case_sensitive=True):
        self.entity_res = regexes
        flag = re.MULTILINE
        if case_sensitive:
            flag = flag | re.IGNORECASE
        self.entity_res = [re.compile(reg, flag) for reg in self.entity_res]
        self.exclusion_list = exclusion_list

    def get_matches(self, doc):
        """
        Input: doc - string containing description text
        Returns: list of strings, each one is a valid phone number
        """
        res = []
        for pattern in self.entity_res:
            found_entity = None
            matches = pattern.finditer(doc)
            for match in matches:
                for k in match.re.groupindex:
                    found_exc = False
                    found_entity = match.group(k)
                    if found_entity is None:
                        continue
                    start_pos, end_pos = match.span(k)
                    if found_entity in self.exclusion_list:
                        found_exc = True
                    if not found_exc:
                        res.append(Entity(k, found_entity, start_pos, end_pos))
            if found_entity:
                return res
        return res

def main():
    extractor = RegexExtractor(regexes=['(?P<position>P\\d{6})'])
    line = 'Please transfer following positions: P512537 P765471 P765475 P765474 P765473 P765472 P541802 P756850 Under supervisory organization of Maria Lukaszewicz [e532888]'
    res = extractor.get_matches(line)
    for r in res:
        print(r.tojson())
if __name__ == '__main__':
    sample = 'Dedupe positive numbers 6900547151 but when i check the "View details" in the iDOC portal no details not found'
    doc = {'text': sample}
    main()