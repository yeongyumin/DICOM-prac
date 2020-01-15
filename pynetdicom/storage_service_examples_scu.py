from pydicom import dcmread
from pydicom.data import get_testdata_files

from pynetdicom import AE
from pynetdicom.sop_class import CTImageStorage

ae = AE()

ae.add_requested_context(CTImageStorage)

file_name = get_testdata_files('CT_small')[0]

ds = dcmread(file_name)

assoc = ae.associate('127.0.0.1', 11112)

if assoc.is_established:
    status = assoc.send_c_store(ds)

    if status:
        print('C-STORE request status: 0x{0:04x}'.format(status.Status))
    else:
        print('Connection timed out, was aborted or received invalid response')

    assoc.release()
else:
    print('Association rejected, aborted or never connected')
