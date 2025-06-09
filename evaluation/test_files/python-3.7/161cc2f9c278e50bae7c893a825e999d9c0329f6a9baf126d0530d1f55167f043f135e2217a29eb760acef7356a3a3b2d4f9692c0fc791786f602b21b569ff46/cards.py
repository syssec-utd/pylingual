from json.encoder import py_encode_basestring_ascii
import requests
import json
from creditagricole_particuliers import operations
from creditagricole_particuliers import accounts

class Card:

    def __init__(self, session, card):
        """account class"""
        self.session = session
        self.card = card
        self.idCompte = card['idCompte']
        self.typeCarte = card['typeCarte']
        self.idCarte = card['idCarte']
        self.titulaire = card['titulaire']

    def __str__(self):
        """str"""
        return f'Carte[compte={self.idCompte}, type={self.typeCarte}, titulaire={self.titulaire}]'

    def get_operations(self):
        """get deferred operations"""
        account = accounts.Accounts(session=self.session).search(num=self.idCompte)
        return operations.DeferredOperations(session=self.session, compteIdx=account.compteIdx, grandeFamilleCode=account.grandeFamilleCode, carteIdx=self.card['index'])

    def as_json(self):
        """return as json"""
        return json.dumps(self.card)

class Cards:

    def __init__(self, session):
        """cards class"""
        self.session = session
        self.cards_list = []
        self.get_cards_per_account()

    def __iter__(self):
        """iter"""
        self.n = 0
        return self

    def __next__(self):
        """next"""
        if self.n < len(self.cards_list):
            op = self.cards_list[self.n]
            self.n += 1
            return op
        else:
            raise StopIteration

    def as_json(self):
        """as json"""
        _accs = []
        for acc in self.cards_list:
            _accs.append(acc.card)
        return json.dumps(_accs)

    def search(self, num_last_digits):
        """search card """
        for cb in self.cards_list:
            if cb.idCarte.endswith(num_last_digits):
                return cb
        raise Exception('[error] card not found')

    def get_cards_per_account(self):
        """get cards per account"""
        url = '%s' % self.session.url
        url += '/%s/particulier/operations/' % self.session.regional_bank_url
        url += 'moyens-paiement/gestion-carte-v2/mes-cartes/jcr:content.listeCartesParCompte.json'
        r = requests.get(url=url, verify=self.session.ssl_verify, cookies=self.session.cookies)
        if r.status_code != 200:
            raise Exception('[error] get cards: %s - %s' % (r.status_code, r.text))
        r = json.loads(r.text)
        if 'comptes' not in r:
            raise Exception('[error] compte not found in response ')
        for account in r['comptes']:
            for card in account['listeCartes']:
                card['idCompte'] = account['idCompte']
                self.cards_list.append(Card(self.session, card))