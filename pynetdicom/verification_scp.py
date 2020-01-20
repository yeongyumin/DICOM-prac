from pynetdicom import AE, evt
from pynetdicom.sop_class import VerificationSOPClass

def handle_echo(event):
    print(event.assoc)
    print(event.event)
    print(event.timestamp)
    print(event.identifier)
    return 0x0000

handlers = [
    (evt.EVT_C_ECHO, handle_echo)
]

ae = AE()
ae.add_supported_context(VerificationSOPClass)
ae.start_server(('', 11112), block=True, evt_handlers=handlers)
