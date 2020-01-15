from pynetdicom import AE
from pynetdicom.sop_class import DisplaySystemSOPClass
from pynetdicom.status import code_to_category

ae = AE()

ae.add_requested_context(DisplaySystemSOPClass)

assoc = ae.associate('127.0.0.1', 11112)

if assoc.is_established:
    status, attr_list = assoc.send_n_get(
        [(0x0008,0x0070)],
        DisplaySystemSOPClass,
        '1.2.840.10008.5.1.1.40.1'
    )

    if status:
        print('N-GET request status: 0x{0:04x}'.format(status.Status))
    print('established!')
    print(status)
    print(attr_list)
else:
    print('Association rejected, aborted or never connected')
