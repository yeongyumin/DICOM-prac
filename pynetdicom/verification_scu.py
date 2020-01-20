from pydicom import dcmread
from pydicom.data import get_testdata_files

from pynetdicom import AE
from pynetdicom.sop_class import VerificationSOPClass, CTImageStorage

file_name = get_testdata_files('CT_small')[0]

ds = dcmread(file_name)

ae = AE()

ae.add_requested_context(VerificationSOPClass)
ae.add_requested_context(CTImageStorage)

assoc = ae.associate('localhost', 11112)

if assoc.is_established:
    status = assoc.send_c_echo()

    print(status)

    if status:
        print('C-ECHO request status: 0x{0:04x}'.format(status.Status))
    else:
        print('Connection timed out, was aborted or received invalid response')

else:
    print('Association rejected, aborted or never connected')
