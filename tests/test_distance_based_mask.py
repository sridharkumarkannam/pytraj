#!/usr/bin/env python
from __future__ import print_function
import unittest
import numpy as np
import pytraj as pt
from pytraj.testing import aa_eq
from pytraj import io as mdio
from itertools import product


class TestDistanceBasedMask(unittest.TestCase):
    def test_smaller(self):
        traj = mdio.iterload("./data/tz2.nc", "./data/tz2.parm7")
        top = traj.top

        ref = traj[0]
        # test for 1st frame
        top.set_reference_frame(ref)
        ref.top = top

        # all atoms within 5 Angtrom from :3@CA
        indices = top.select(":3@CA <@5.0")

        saved_indices = np.loadtxt(
            "./data/mask.tz2.dat",
            skiprows=1,
            usecols=(1, ))

        # subtract by '1' since cpptraj uses "1" as starting index for output
        saved_indices = saved_indices - 1
        aa_eq(indices, saved_indices)

        # re-calculate the distance
        ca_indices = pt.select_atoms(traj.top, ':3@CA')
        all_pairs = list(product(ca_indices, indices))
        distances = pt.tools.flatten(pt.distance(ref, all_pairs))
        for dist in distances:
            assert dist < 5.0, 'all distances must be smaller than 5.0 Angstrom'

        # test larger
        # why do we need to set reference frame again?
        top.set_reference_frame(ref)
        indices_larger = top.select(":3@CA >@5.0")
        all_pairs_larger = list(product(ca_indices, indices_larger))
        distances = pt.tools.flatten(pt.distance(ref, all_pairs_larger))
        for dist in distances:
            assert dist > 5.0, 'all distances must be smaller than 5.0 Angstrom'


if __name__ == "__main__":
    unittest.main()
