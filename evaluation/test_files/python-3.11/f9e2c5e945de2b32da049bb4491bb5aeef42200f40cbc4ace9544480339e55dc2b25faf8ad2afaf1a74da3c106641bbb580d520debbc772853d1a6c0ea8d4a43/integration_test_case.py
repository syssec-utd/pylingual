import urllib.request, urllib.error, urllib.parse
from flask import Flask, g
from .test_case import TestCase
from flask_login import login_user, current_user, current_app
import requests

class IntegrationTestCase(TestCase):

    def create_user(self, email, password, username='identifier', fn='First', ln='Last', roles='Admin'):
        from whyis import commands
        from uuid import uuid4
        pw = 'password'
        creator = commands.CreateUser()
        creator.run(email, password, fn, ln, username, roles)
        return (email, password)

    def login(self, email, password):
        return self.client.post('/login', data={'email': email, 'password': password, 'remember': 'y'}, follow_redirects=True)

    def run_agent(self, agent, nanopublication=None):
        app = self.app
        agent.dry_run = True
        agent.app = app
        results = []
        if nanopublication is not None:
            results.extend(agent.process_graph(nanopublication))
        elif agent.query_predicate == app.NS.whyis.globalChangeQuery:
            results.extend(agent.process_graph(app.db))
        else:
            print('Running as update agent')
            for resource in agent.getInstances(app.db):
                print(resource.identifier)
                for np_uri, in app.db.query('select ?np where {\n    graph ?assertion { ?e ?p ?o.}\n    ?np a np:Nanopublication;\n        np:hasAssertion ?assertion.\n}', initBindings={'e': resource.identifier}, initNs=app.NS.prefixes):
                    print(np_uri)
                    np = app.nanopub_manager.get(np_uri)
                    results.extend(agent.process_graph(np))
        return results