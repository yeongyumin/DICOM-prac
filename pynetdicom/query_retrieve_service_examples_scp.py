import os

from pydicom import dcmread
from pydicom.dataset import Dataset

from pynetdicom import AE, evt
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind

instances = []

def handle_find(event):
    # event의 identifier가 dataset
    ds = event.identifier

    fdir = '/Users/yeongyumin/Desktop/public/DICOM-prac/lib/python3.7/site-packages/pydicom/data/test_files'

    # instance가 존재하지 않으면 memory에 캐싱
    if len(instances) == 0:
        print("worked")
        for fpath in os.listdir(fdir):
            full_filename = os.path.join(fdir, fpath)

            ext = os.path.splitext(full_filename)[-1]
            # dcm파일 중에 읽을 수 있는 애들만 instances로 mount
            if ext == '.dcm':
                try:
                    instances.append(dcmread(full_filename))
                except:
                    print('exception: ' + full_filename)

    # QueryRetrieveLevel이 지정되어 있지 않으면(쿼리에 어디까지 정보를 제공할 것인지 결정) Failed 반환
    if 'QueryRetrieveLevel' not in ds:
        # Failure
        print('Failed T-T')
        # yield??
        yield 0xC000, None
        return

    if ds.QueryRetrieveLevel == 'PATIENT':
        if 'PatientName' in ds:
            matching = [
                # 애초에 DICOM Dataset에 PatientName이라는 필드가 없을 수도 있음
                inst for inst in instances if 'PatientName' in inst and inst.PatientName == ds.PatientName
            ]

    for instance in matching:
        if event.is_cancelled:
            yield (0xFE00, None)
            return

        identifier = Dataset()
        identifier.PatientName = instance.PatientName
        identifier.QueryRetrieveLevel = ds.QueryRetrieveLevel

        yield (0xFF00, identifier)

handlers = [(evt.EVT_C_FIND, handle_find)]

ae = AE()

# 서포트 가능한 컨텍스트만 등록
ae.add_supported_context(PatientRootQueryRetrieveInformationModelFind)

# request가 왔을 때 핸들링할 핸들러 지정
ae.start_server(('', 11112), evt_handlers=handlers)
