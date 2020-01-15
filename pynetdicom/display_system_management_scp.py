from pynetdicom import AE, evt
from pynetdicom.sop_class import DisplaySystemSOPClass

from pydicom.dataset import Dataset

def handle_get(event):
    attr = event.request.AttributeIdentifierList

    ds = Dataset()
    ds.PatientName = 'hohoho'

    ds.SOPClassUID = '1.2.840.10008.5.1.1.40'
    ds.SOPInstanceUID = '1.2.840.10008.5.1.1.40.1'

    return 0x0000, ds

ae = AE()

handlers = [(evt.EVT_N_GET, handle_get)]

ae.add_supported_context(DisplaySystemSOPClass)

ae.start_server(('', 11112), evt_handlers=handlers)
