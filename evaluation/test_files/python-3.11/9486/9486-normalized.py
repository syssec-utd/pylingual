def do_fuzzyindex(self, word):
    """Compute fuzzy extensions of word that exist in index.
    FUZZYINDEX lilas"""
    word = list(preprocess_query(word))[0]
    token = Token(word)
    neighbors = make_fuzzy(token)
    neighbors = [(n, DB.zcard(dbkeys.token_key(n))) for n in neighbors]
    neighbors.sort(key=lambda n: n[1], reverse=True)
    for token, freq in neighbors:
        if freq == 0:
            break
        print(white(token), blue(freq))