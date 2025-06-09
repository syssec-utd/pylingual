"""CogniteRobotics web interface gRPC client."""
import logging
from typing import Union
from cognite_robotics.config.config import CogniteRoboticsClientConfig, LocalClientConfig
from cognite_robotics.grpc.helpers.channel import get_insecure_channel, get_secure_channel
from cognite_robotics.protos.services.web_interface_pb2_grpc import WebInterfaceStub
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class CogniteRoboticsWebInterfaceClient:
    """gRPC Client for cloud <-> Web UI communication."""

    def __init__(self, client_config: Union[CogniteRoboticsClientConfig, LocalClientConfig]) -> None:
        """Initialize a gRPC client for cloud <-> Web UI communication."""
        self.client_config = client_config
        self.initialized_channel = False

    async def _refresh_channel(self) -> None:
        if isinstance(self.client_config, CogniteRoboticsClientConfig):
            logger.info('Setting up a secure channel.')
            channel = await get_secure_channel(self.client_config.project, self.client_config.oidc_token_callable, self.client_config.target)
        else:
            logger.info(f'Setting up an insecure channel at {self.client_config.ip}:{self.client_config.port}.')
            channel = await get_insecure_channel(self.client_config.ip, self.client_config.port)
        self.web_interface_client = WebInterfaceStub(channel)