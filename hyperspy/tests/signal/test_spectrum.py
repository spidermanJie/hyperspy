# Copyright 2007-2012 The Hyperspy developers
#
# This file is part of Hyperspy.
#
# Hyperspy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hyperspy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hyperspy. If not, see <http://www.gnu.org/licenses/>.


import os

import numpy as np

from nose.tools import assert_true, assert_equal, assert_not_equal
from hyperspy.signals.spectrum import Spectrum

class TestAlignTools:
    def setUp(self):
        s = Spectrum({'data' : np.zeros((10,100))})
        self.scale = 0.1
        self.offset = -2
        eaxis = s.axes_manager.signal_axes[0]
        eaxis.scale = self.scale
        eaxis.offset = self.offset
        self.izlp = eaxis.value2index(0)
        self.bg = 2
        self.ishifts = np.array([0,  4,  2, -2,  5, -2, -5, -9, -9, -8])
        self.new_offset = self.offset - self.ishifts.min() * self.scale
        s.data[np.arange(10), self.ishifts + self.izlp] = 10
        s.data += self.bg
        self.spectrum = s
        
    def test_estimate_shift(self):
        s = self.spectrum
        eshifts = -1 * s.estimate_shift_in_units_1D().squeeze()
        assert_true(np.allclose(eshifts, self.ishifts * self.scale))
        
    def test_align_with_array_1D(self):
        s = self.spectrum
        s.align_with_array_1D(-1 * self.ishifts[:, np.newaxis] * self.scale)
        i_zlp = s.axes_manager.signal_axes[0].value2index(0)
        assert_true(np.allclose(s.data[:, i_zlp], 12))
        # Check that at the edges of the spectrum the value == to the
        # background value. If it wasn't it'll mean that the cropping
        # code is buggy
        assert_true((s.data[:,-1] == 2).all())
        assert_true((s.data[:,0] == 2).all())
        # Check that the calibration is correct
        assert_equal(s.axes_manager.axes[1].offset, self.new_offset)
        assert_equal(s.axes_manager.axes[1].scale, self.scale)
        
    def test_align(self):
        s = self.spectrum
        s.align_1D()
        i_zlp = s.axes_manager.signal_axes[0].value2index(0)
        assert_true(np.allclose(s.data[:, i_zlp], 12))
        # Check that at the edges of the spectrum the value == to the
        # background value. If it wasn't it'll mean that the cropping
        # code is buggy
        assert_true((s.data[:,-1] == 2).all())
        assert_true((s.data[:,0] == 2).all())
        # Check that the calibration is correct
        assert_equal(s.axes_manager.axes[1].offset, self.new_offset)
        assert_equal(s.axes_manager.axes[1].scale, self.scale)
