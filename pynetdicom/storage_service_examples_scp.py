from pydicom.dataset import Dataset

from pynetdicom import (
    AE, evt,
    StoragePresentationContexts,
    PYNETDICOM_IMPLEMENTATION_UID,
    PYNETDICOM_IMPLEMENTATION_VERSION
)

def handle_store(event):
    ds = event.dataset

    ds.file_meta = event.file_meta

    ds.save_as(ds.SOPInstanceUID, write_like_original=False)

    return 0x0000

handlers = [(evt.EVT_C_STORE, handle_store)]

ae = AE()

ae.supported_contexts = StoragePresentationContexts

ae.start_server(('', 11112), evt_handlers=handlers)
