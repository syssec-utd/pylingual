import subprocess
import os
import shutil
import sys
import inspect
import json
from concurrent import futures
from cakework import cakework_pb2
from cakework import cakework_pb2_grpc
from .activity_server import ActivityServer
import importlib
import logging
logging.basicConfig(level=logging.INFO)

class App:

    def __init__(self, app, user_id='shared', local=False):
        self.app = app.lower().replace('_', '-')
        self.user_id = user_id.lower().replace('_', '-')
        self.local = local
        logging.info('Created app for user id: ' + user_id + ', app name: ' + app)

    def add_task(self, activity):
        logging.info('Adding task')
        activity_server = ActivityServer(activity, self.local)
        activity_server.start()

def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    cakework_pb2_grpc.add_CakeworkServicer_to_server(Cakework(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    logging.info('Server started, listening on ' + port)
    server.wait_for_termination()