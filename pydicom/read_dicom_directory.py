from os.path import dirname, join
from pprint import pprint

import pydicom
from pydicom.data import get_testdata_files
from pydicom.filereader import read_dicomdir

filepath = get_testdata_files('DICOMDIR')[0]
print('Path to the DICOM directory: {}'.format(filepath))

dicom_dir = read_dicomdir(filepath)
base_dir = dirname(filepath)

for patient_record in dicom_dir.patient_records:
    # print(patient_record)
    if (hasattr(patient_record, 'PatientID') and hasattr(patient_record, 'PatientName')):
        print("Patient: {}: {}".format(patient_record.PatientID, patient_record.PatientName))

    studies = patient_record.children

    for study in studies:
        print(" " * 4 + "Study {}: {}: {}".format(study.StudyID, study.StudyDate, study.StudyDescription))

        all_series = study.children

        for series in all_series:
            image_count = len(series.children)
            plural = ('', 's')[image_count > 1]

            if 'SeriesDescription' not in series:
                series.SeriesDescription = "N/A"
            print(" " * 8 + "Series {}: {}: {} ({} image{})".format(
                series.SeriesNumber, series.Modality, series.SeriesDescription, image_count, plural
            ))

            print(" " * 12 + "Reading images...")
            image_records = series.children
            image_filenames = [join(base_dir, *image_rec.ReferencedFileID) for image_rec in image_records]

            datasets = [pydicom.dcmread(image_filename) for image_filename in image_filenames]

            patient_names = set(ds.PatientName for ds in datasets)
            patient_IDs = set(ds.PatientID for ds in datasets)

            print("\n" + " " * 12 + "Image filenames:")
            print(" " * 12, end=' ')
            pprint(image_filenames, indent=12)

            print(" " * 12 + "Patient Names in images...: {}".format(patient_names))
            print(" " * 12 + "Patient IDs in images...: {}".format(patient_IDs))
