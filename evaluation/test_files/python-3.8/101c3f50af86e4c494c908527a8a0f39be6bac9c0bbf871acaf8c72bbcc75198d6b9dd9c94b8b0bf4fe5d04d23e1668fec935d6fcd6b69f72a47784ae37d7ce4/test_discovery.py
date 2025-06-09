import time
from .base import TestDHTBase
from ..mocking.ipv8 import MockIPv8
from ...dht import DHTError
from ...dht.discovery import DHTDiscoveryCommunity
from ...dht.routing import Node, RoutingTable
from ...util import succeed

class TestDHTDiscoveryCommunity(TestDHTBase):

    def setUp(self):
        super().setUp()
        self.initialize(DHTDiscoveryCommunity, 2)
        self.pinged = None
        self.puncture_to = None
        for node in self.nodes:
            node.overlay.cancel_pending_task('store_peer')
            node.overlay.token_maintenance()

    def create_node(self, *args, **kwargs):
        return MockIPv8(u'curve25519', DHTDiscoveryCommunity)

    async def test_store_peer(self):
        await self.introduce_nodes()
        await self.overlay(0).store_peer()
        self.assertIn(self.mid(0), self.overlay(1).store)
        self.assertIn(self.mid(0), self.overlay(0).store_for_me)

    async def test_store_peer_fail(self):
        await self.introduce_nodes()
        self.overlay(0).routing_tables[self.address(0).__class__] = RoutingTable(self.my_node_id(0))
        self.assertFalse(await self.overlay(0).store_peer())

    async def test_connect_peer(self):
        node = MockIPv8(u'curve25519', DHTDiscoveryCommunity)
        self.add_node_to_experiment(node)
        await self.introduce_nodes()
        self.overlay(1).store[self.mid(0)].append(self.my_peer(0))
        self.overlay(0).store_for_me[self.mid(0)].append(self.my_peer(1))
        org_func = self.overlay(1).create_puncture_request

        def create_puncture_request(*args):
            self.puncture_to = args[1]
            return org_func(*args)
        self.overlay(1).create_puncture_request = create_puncture_request
        await self.deliver_messages()
        nodes = await self.overlay(2).connect_peer(self.mid(0))
        self.assertEqual(self.puncture_to, self.address(2))
        self.assertIn(self.key_bin(0), [n.public_key.key_to_bin() for n in nodes])

    async def test_connect_peer_fail(self):
        await self.introduce_nodes()
        self.overlay(0).routing_tables[self.address(0).__class__] = RoutingTable(self.my_node_id(0))
        with self.assertRaises(DHTError):
            await self.overlay(0).connect_peer(self.mid(1))

    async def test_ping_pong(self):
        now = time.time() - 1
        node0 = Node(self.private_key(0), self.address(0))
        node0.last_response = now
        node0.last_queries.append(now)
        node1 = Node(self.private_key(1), self.address(1))
        node1.last_response = now
        node1.last_queries.append(now)
        key = node1.mid
        self.overlay(0).store[key].append(node1)
        self.overlay(1).store_for_me[key].append(node0)
        await self.overlay(1).ping(node0)
        self.assertNotEqual(node0.last_response, now)
        self.assertNotEqual(node1.last_query, now)

    def test_ping_all(self):
        self.overlay(0).ping = lambda n: setattr(self, 'pinged', n) or succeed(None)
        node1 = Node(self.private_key(1), self.address(1))
        node1.last_ping_sent = time.time()
        node1.last_queries.append(time.time())
        self.overlay(0).store[node1.mid].append(node1)
        self.overlay(0).ping_all()
        self.assertIn(node1, self.overlay(0).store[node1.mid])
        node1.last_queries[-1] -= 100
        self.overlay(0).ping_all()
        self.assertNotIn(node1, self.overlay(0).store[node1.mid])
        self.assertEqual(self.pinged, None)
        self.overlay(0).store_for_me[node1.mid].append(node1)
        self.overlay(0).ping_all()
        self.assertIn(node1.mid, self.overlay(0).store_for_me)
        node1.last_ping_sent -= 30
        self.overlay(0).ping_all()
        self.assertEqual(self.pinged, node1)
        self.assertIn(node1, self.overlay(0).store_for_me[node1.mid])
        self.pinged = None
        node1.failed = 3
        self.overlay(0).ping_all()
        self.assertEqual(self.pinged, None)
        self.assertNotIn(node1, self.overlay(0).store_for_me[node1.mid])