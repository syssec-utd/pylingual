from tconnectsync.domain.therapy_event import BolusTherapyEvent, CGMTherapyEvent, BGTherapyEvent, BasalTherapyEvent
from tconnectsync.parser.tconnect import TConnectEntry
import logging
logger = logging.getLogger(__name__)

def split_therapy_events(ciqTherapyEvents):
    bolusEvents = []
    cgmEvents = []
    bgEvents = []
    basalEvents = []
    for e in ciqTherapyEvents['event']:
        event = TConnectEntry.parse_therapy_event(e)
        if isinstance(event, BolusTherapyEvent):
            bolusEvents.append(event)
        elif isinstance(event, CGMTherapyEvent):
            cgmEvents.append(event)
        elif isinstance(event, BGTherapyEvent):
            bgEvents.append(event)
        elif isinstance(event, BasalTherapyEvent):
            basalEvents.append(event)
    logger.debug('split_therapy_events: %d bolus, %d CGM, %d BG, %d basal' % (len(bolusEvents), len(cgmEvents), len(bgEvents), len(basalEvents)))
    return (bolusEvents, cgmEvents)