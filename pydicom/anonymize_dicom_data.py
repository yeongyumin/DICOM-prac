from __future__ import print_function

import tempfile

import pydicom
from pydicom.data import get_testdata_files

filename = get_testdata_files('MR_small.dcm')[0]
dataset = pydicom.dcmread(filename)

data_elements = ['PatientID', 'PatientBirthDate']

# for de in data_elements:
#     print(dataset.data_element(de))

def person_names_callback(dataset, data_element):
    if data_element.VR == "PN":
        data_element.value = "anonymous"

def curves_callback(dataset, data_element):
    if (data_element.tag.group & 0xFF00) == 0x5000:
        del dataset[data_element.tag]

dataset.PatientID = "id"
dataset.walk(person_names_callback)
dataset.walk(curves_callback)

dataset.remove_private_tags()
