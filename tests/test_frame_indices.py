#!/usr/bin/env python

from __future__ import print_function
import unittest
import numpy as np
import pytraj as pt
from pytraj.utils import eq, aa_eq
from pytraj.compat import string_types
from pytraj.hbond_analysis import DatasetHBond


class TestFrameIndices(unittest.TestCase):
    def setUp(self):
        self.traj = pt.iterload("./data/tz2.nc", "./data/tz2.parm7")
    def test_frame_indices_from_yield(self):
        '''extensive and seperated testsing
        '''
        traj = self.traj

        def gen_int():
            for i in range(0, 10, 2):
                yield i

        for idx, frame in enumerate(pt.iterframe(traj, frame_indices=gen_int())):
            pass

        assert idx == len(range(0, 10, 2)) - 1
        aa_eq(frame.xyz, traj[8].xyz)

    def test_frame_indices_for_function(self):
        traj = self.traj

        pdict = pt.__dict__
        funclist = list(set(pdict[key] for key in dir(pt) if hasattr(pdict[key], '_is_super_dispatched')))

        frame_indices = [0, 5, 2]

        # remove 'calc_jcoupling' since does not have kfile on travis
        # remove energy_decomposition since does not have sander
        # remove center, why?
        # remove search_neighbors, why? (got messup with Frame memory owner) 
        excluded_fn = ['calc_jcoupling', 'calc_volmap', 'calc_density',
                'energy_decomposition', 'center', 'search_neighbors',
                'calc_atomiccorr','do_autoimage', 'closest']

        # default mask, default ref
        for func in funclist:
            if func.__name__ not in excluded_fn:
                if func is pt.calc_multivector:
                    data_0 = func(traj, resrange='1-6', names='C N', frame_indices=frame_indices)
                    data_1 = func(traj[frame_indices], resrange='1-6', names='C N')
                else:
                    data_0 = func(traj, frame_indices=frame_indices)
                    data_1 = func(traj[frame_indices])

                if isinstance(data_0, np.ndarray):
                    aa_eq(data_0, data_1)
                elif isinstance(data_0, pt.DatasetList):
                    for arr0, arr1 in zip(data_0, data_1):
                        # do each element in case we can not convert DatasetList to
                        # ndarray
                        if not isinstance(arr0[0], string_types):
                            aa_eq(arr0.values, arr1.values)
                elif isinstance(data_0, DatasetHBond):
                    aa_eq(data_0.data.values, data_1.data.values)
                elif isinstance(data_0, (list, tuple)):
                    # dssp
                    aa_eq(data_0[-1].values, data_1[-1].values)
                else:
                    raise RuntimeError('must return ndarray or DatasetList or DatasetHBond')

        # test excluded fns
        # calc_atomiccorr
        # FIXME: why failed?
        #aa_eq(pt.atomiccorr(traj[frame_indices], '@CA'),
        #      pt.atomiccorr(traj, '@CA', frame_indices=frame_indices))
                    

if __name__ == "__main__":
    unittest.main()
