# -*- coding: utf-8 -*-
# Copyright 2007-2011 The Hyperspy developers
#
# This file is part of  Hyperspy.
#
#  Hyperspy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
#  Hyperspy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with  Hyperspy.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np

from hyperspy.component import Component

class RC(Component):
    """
    """

    def __init__(self, V=1, V0= 0, tau=1.):
        Component.__init__(self, ('Vmax', 'V0', 'tau'))
        self.Vmax.value, self.V0.value, self.tau.value = Vmax, V0, tau

    def function( self, x ) :
        """
        """
        Vmax = self.Vmax.value
        V0 = self.V0.value
        tau = self.tau.value
        return V0 + Vmax*(1-np.exp(-x/tau))
    



