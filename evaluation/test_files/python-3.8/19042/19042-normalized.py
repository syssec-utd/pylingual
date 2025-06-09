def tokens(self, sentence_dom):
    """
        Tokenize all the words and preserve NER labels from ENAMEX tags
        """
    self.sent_pos = 0
    mention_id = 0
    while len(sentence_dom.childNodes) > 0:
        node = sentence_dom.childNodes.pop(0)
        if node.nodeType == node.TEXT_NODE:
            for line in node.data.splitlines(True):
                self._input_string = line
                for (start, end) in self.word_tokenizer.span_tokenize(line):
                    tok = self._make_token(start, end)
                    if tok:
                        yield tok
                if line.endswith('\n'):
                    self.line_idx += 1
                self.byte_idx += len(line.encode('utf-8'))
        else:
            assert node.nodeName == 'ENAMEX', node.nodeName
            chain_id = node.attributes.get('ID').value
            entity_type = node.attributes.get('TYPE').value
            for node in node.childNodes:
                assert node.nodeType == node.TEXT_NODE, node.nodeType
                for line in node.data.splitlines(True):
                    self._input_string = line
                    for (start, end) in self.word_tokenizer.span_tokenize(line):
                        tok = self._make_token(start, end)
                        if tok:
                            if entity_type in _PRONOUNS:
                                tok.mention_type = MentionType.PRO
                                tok.entity_type = _ENTITY_TYPES[entity_type]
                                attr = Attribute(attribute_type=AttributeType.PER_GENDER, value=str(_PRONOUNS[entity_type]))
                                self.attributes.append(attr)
                            else:
                                tok.mention_type = MentionType.NAME
                                tok.entity_type = _ENTITY_TYPES[entity_type]
                            tok.equiv_id = int(chain_id)
                            tok.mention_id = mention_id
                            yield tok
                    if line.endswith('\n'):
                        self.line_idx += 1
                    self.byte_idx += len(line.encode('utf-8'))
            mention_id += 1