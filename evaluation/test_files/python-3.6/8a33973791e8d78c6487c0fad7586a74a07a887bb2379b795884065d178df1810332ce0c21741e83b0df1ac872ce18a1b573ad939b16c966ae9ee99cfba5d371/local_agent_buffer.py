from concurrent.futures import ProcessPoolExecutor
from typing import Optional
import psutil
from smarts.core.agent_buffer import AgentBuffer
from smarts.core.buffer_agent import BufferAgent
from smarts.core.local_agent import LocalAgent

class LocalAgentBuffer(AgentBuffer):
    """A buffer that manages social agents."""

    def __init__(self):
        pass

    def destroy(self):
        pass

    def acquire_agent(self, retries: int=3, timeout: Optional[float]=None) -> BufferAgent:
        localAgent = LocalAgent()
        return localAgent