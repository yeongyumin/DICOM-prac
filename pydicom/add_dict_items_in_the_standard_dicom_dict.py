from __future__ import print_function

from pydicom.datadict import DicomDictionary, keyword_dict
from pydicom.dataset import Dataset

print(__doc__)

new_dict_items = {
    0x10011001: ('UL', '1', "Test One", '', 'TestOne'),
    0x10011002: ('OB', '1', "Test Two", '', 'TestTwo'),
    0x10011003: ('UI', '1', "Test Three", '', 'TestThree')
}

DicomDictionary.update(new_dict_items)

print(new_dict_items)

new_names_dict = dict([(val[4], tag) for tag, val in new_dict_items.items()])

keyword_dict.update(new_names_dict)

ds = Dataset()

ds.TestOne = 42
ds.TestTwo = '12345'
ds.TestThree = '1.2.3.4.5'
ds.TestFour = 134

print(ds)
