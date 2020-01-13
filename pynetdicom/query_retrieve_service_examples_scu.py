from pydicom.dataset import Dataset

from pynetdicom import AE
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind

ae = AE()

ae.add_requested_context(PatientRootQueryRetrieveInformationModelFind)

ds = Dataset()
ds.PatientName = 'Lestrade^G'
ds.QueryRetrieveLevel = 'PATIENT'

assoc = ae.associate('127.0.0.1', 11112)

if assoc.is_established:
    responses = assoc.send_c_find(ds, PatientRootQueryRetrieveInformationModelFind)

    for (status, identifier) in responses:
        if status:
            print('C-FIND query status: 0x{0:04x}'.format(status.Status))

            if status.Status in (0xFF00, 0xFF01):
                print(identifier)
        else:
            print('Connection timed out, was aborted or received invalid response')

else:
    print('Association rejected, aborted or never connected')
