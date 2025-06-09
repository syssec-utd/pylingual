from enum import auto, Flag, IntEnum
import datetime
from .datatype import Datatype

class EventSeverity(IntEnum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

    @staticmethod
    def all():
        return ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

    def __str__(self):
        return EventSeverity.all()[self.value]

    @staticmethod
    def from_string(name):
        return EventSeverity(EventSeverity.all().index(name))

class EventTrigger(Flag):
    """Specifies under which conditions the associated event is triggered.
    Flags can be logically combined. Not all combinations of cause are meaningful.
    """
    NOT = auto()
    EQUALS = auto()
    SMALLER = auto()
    LARGER = auto()

    def __str__(self):
        trigger = self.simplify(self)
        if trigger.value == 0:
            return 'Always triggered'
        res = ''
        if EventTrigger.NOT in self:
            res += '!'
        if EventTrigger.SMALLER in self:
            res += '<'
        if EventTrigger.LARGER in self:
            res += '>'
        if EventTrigger.EQUALS in self:
            res += '='
        return res

    @staticmethod
    def is_valid(trigger):
        return trigger not in [EventTrigger.NOT, EventTrigger.SMALLER | EventTrigger.LARGER]

    @staticmethod
    def simplify(trigger):
        if trigger == EventTrigger.SMALLER | EventTrigger.NOT:
            return EventTrigger.EQUALS | EventTrigger.LARGER
        if trigger == EventTrigger.LARGER | EventTrigger.NOT:
            return EventTrigger.EQUALS | EventTrigger.SMALLER
        if trigger == EventTrigger.SMALLER | EventTrigger.NOT | EventTrigger.EQUALS:
            return EventTrigger.LARGER
        if trigger == EventTrigger.LARGER | EventTrigger.NOT | EventTrigger.EQUALS:
            return EventTrigger.SMALLER
        if trigger == EventTrigger.LARGER | EventTrigger.SMALLER | EventTrigger.NOT:
            return EventTrigger.EQUALS
        if trigger == EventTrigger.LARGER | EventTrigger.SMALLER | EventTrigger.EQUALS or trigger == EventTrigger.LARGER | EventTrigger.SMALLER | EventTrigger.NOT | EventTrigger.EQUALS:
            return EventTrigger(0)
        return trigger

class Event(object):

    def __init__(self, severity, trigger, datatype: str, target, message=''):
        """Constructor

        :param severity: Severity of the event, according to Enum @EventSeverity.
        :param trigger: Flag for specifying the trigger for that event, as described in Enum @EventTrigger.
        :param datatype: Datatype of the corresponding measurement or parameter, as given by Enum @Datatype.
        :param target: Value associated with the trigger, either interpreted as threshold or target value, depending on the type of trigger.
        :param message: Optional message, containing a user-understandable description of the event, also send with the event.
        """
        datatype = Datatype.from_string(datatype)
        if not EventTrigger.is_valid(trigger):
            raise ValueError('Combination of trigger values is not reasonable!')
        if datatype in [Datatype.ENUM, Datatype.STRING, Datatype.BOOLEAN]:
            if trigger not in [EventTrigger.EQUALS, EventTrigger.EQUALS | EventTrigger.NOT]:
                raise AttributeError('Datatype and Trigger are not compatible.')
        if not isinstance(message, str):
            raise TypeError('Message must be of string type!')
        self._severity = severity
        self._datatype = datatype
        self._trigger = trigger
        self._target = target
        self._message = message
        self._timestamp = None
        self._value = None

    def is_triggered(self, value):
        trigger = EventTrigger.simplify(self._trigger)
        if trigger == EventTrigger.EQUALS:
            return value == self._target
        elif trigger == EventTrigger.LARGER:
            return value > self._target
        elif trigger == EventTrigger.SMALLER:
            return value < self._target
        elif trigger == EventTrigger.EQUALS | EventTrigger.LARGER:
            return value >= self._target
        elif trigger == EventTrigger.EQUALS | EventTrigger.SMALLER:
            return value <= self._target
        elif trigger == EventTrigger.EQUALS | EventTrigger.NOT:
            return value != self._target
        return True

    def __eq__(self, other):
        return other.severity == self._severity and self._datatype == other.datatype and (self._trigger == other.trigger) and (self._target == other.target)

    def trigger(self, value):
        self._value = value
        self._timestamp = datetime.datetime.now()

    def serialize(self):
        return {'severity': str(self._severity), 'trigger': str(self._trigger.value), 'target': self._target, 'message': self._message, 'timestamp': self._timestamp.isoformat() + 'Z', 'value': self._value}