from pydicom.sequence import Sequence
from pydicom.dataset import Dataset

block_ds1 = Dataset()
block_ds1.BlockType = "APERTURE"
block_ds1.BlockName = "Block1"

block_ds2 = Dataset()
block_ds2.BlockType = "APERTURE"
block_ds2.BlockName = "Block2"

beam = Dataset()

plan_ds = Dataset()

plan_ds.BeamSequence = Sequence([beam])
plan_ds.BeamSequence[0].BlockSequence = Sequence([block_ds1, block_ds2])
plan_ds.BeamSequence[0].NumberOfBlocks = 2

beam0 = plan_ds.BeamSequence[0]

block_ds3 = Dataset()

print(plan_ds)

beam0.BlockSequence.append(block_ds3)
del plan_ds.BeamSequence[0].BlockSequence[1]
