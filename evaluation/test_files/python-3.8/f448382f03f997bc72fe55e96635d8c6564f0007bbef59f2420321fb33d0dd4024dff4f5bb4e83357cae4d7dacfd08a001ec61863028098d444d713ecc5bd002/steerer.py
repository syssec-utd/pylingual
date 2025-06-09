import logging
from enum import Enum
import numpy as np
import rosys
from rosys.event import Event
from rosys.helpers import ramp
from .drivable import Drivable

class State(Enum):
    IDLE = 1
    STEERING = 2
    STOPPING = 3

class Steerer:
    """The steerer module translates x-y information (e.g. from a joystick) to linear/angular velocities sent to the robot.

    The wheels module can be any drivable hardware representation.
    Changing the steering state emits events that can be used to react to manual user interaction.

    The conversion from x-y joystick coordinates to linear and angular velocities is implemented as follows:
    The coordinates are translated into an angle (forward: 0 degrees, backward: 180 degrees).
    If the angle is below 110 degrees, y is used as linear velocity and x is used as angular velocity:
    Pulling the joystick to the front-right corner leads to a clockwise rotation while driving forwards.
    Above 110 degrees the angular velocity is flipped:
    Pulling the joystick to the rear-right corner leads to a counter-clockwise rotation while driving backwards.
    From 100 degrees to 110 degrees both velocities are throttled with a linear ramp from factor 1.0 down to 0.0.
    From 110 degrees to 120 degrees the throttle factor is linearly ramped from 0.0 back to 1.0.
    """

    def __init__(self, wheels: Drivable, speed_scaling: float=1.0) -> None:
        self.STEERING_STARTED = Event()
        'steering has started'
        self.STEERING_STOPPED = Event()
        'steering has stopped'
        self.log = logging.getLogger('rosys.steerer')
        self.wheels = wheels
        self.speed_scaling = speed_scaling
        self.state = State.IDLE
        self.linear_speed = 0
        self.angular_speed = 0
        rosys.on_repeat(self.step, 0.05)

    def start(self) -> None:
        self.log.info('start steering')
        self.state = State.STEERING
        self.STEERING_STARTED.emit()

    def update(self, x: float, y: float) -> None:
        if self.state == State.STEERING:
            degrees = np.abs(np.rad2deg(np.arctan2(x, y)))
            throttle = ramp(abs(degrees - 110), 0, 10, 0, 1, clip=True)
            flip = degrees > 110
            self.linear_speed = y * self.speed_scaling * throttle
            self.angular_speed = -x * self.speed_scaling * throttle * (-1 if flip else 1)

    def stop(self) -> None:
        if self.state != State.STEERING:
            return
        self.log.info('stop steering')
        self.orientation = None
        self.state = State.STOPPING
        self.STEERING_STOPPED.emit()

    async def step(self) -> None:
        if self.state == State.STEERING:
            await self.wheels.drive(self.linear_speed, self.angular_speed)
        elif self.state == State.STOPPING:
            await self.wheels.stop()
            self.state = State.IDLE

    def set_speed_scaling(self, speed_scaling: float) -> None:
        self.speed_scaling = speed_scaling

    def __str__(self) -> str:
        return f'{type(self).__name__} ({self.state})'