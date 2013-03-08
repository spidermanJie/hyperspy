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

import copy
import os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.backend_bases import NavigationToolbar2

import hyperspy

def does_figure_object_exists(fig_obj):
    """Test if a figure really exist
    """
    if fig_obj is None:
        return False
    else:
        # Test if the figure really exists. If not call the reset function 
        # and start again. This is necessary because with some backends 
        # Hyperspy fails to connect the close event to the function.
        try:
            fig_obj.show()
            return True
        except:
            fig_obj = None
            return False
                
def on_figure_window_close(figure, function):
    """Connects a close figure signal to a given function
    
    Parameters
    ----------
    
    figure : mpl figure instance
    function : function
    """
    window = figure.canvas.manager.window
    backend = plt.get_backend()
    if not hasattr(figure, '_on_window_close'):
        figure._on_window_close = list()
    if function not in figure._on_window_close:
        figure._on_window_close.append(function)
    
    if backend == 'GTKAgg':
        def function_wrapper(*args):
                function()
        window.connect('destroy', function_wrapper)

    elif backend == 'WXAgg':
        # In linux the following code produces a segmentation fault
        # so it is enabled only for Windows
        import wx
        def function_wrapper(event):
            for f in figure._on_window_close:
                f()
            plt.close(figure)
        window.Bind(wx.EVT_CLOSE, function_wrapper)
        
    elif backend == 'TkAgg':
        def function_wrapper(*args):
                function()
        figure.canvas.manager.window.bind("<Destroy>", function_wrapper)

    elif backend == 'Qt4Agg':
        from PyQt4.QtCore import SIGNAL
        window = figure.canvas.manager.window
        window.connect(window, SIGNAL('destroyed()'), function)


def plot_RGB_map(im_list, normalization = 'single', dont_plot = False):
    """Plots 2 or 3 maps in RGB
    
    Parameters
    ----------
    im_list : list of Image instances
    normalization : {'single', 'global'}
    dont_plot : bool
    
    Returns
    -------
    array: RGB matrix
    """
#    from widgets import cursors
    height,width = im_list[0].data.shape[:2]
    rgb = np.zeros((height, width,3))
    rgb[:,:,0] = im_list[0].data.squeeze()
    rgb[:,:,1] = im_list[1].data.squeeze()
    if len(im_list) == 3:
        rgb[:,:,2] = im_list[2].data.squeeze()
    if normalization == 'single':
        for i in xrange(rgb.shape[2]):
            rgb[:,:,i] /= rgb[:,:,i].max()
    elif normalization == 'global':
        rgb /= rgb.max()
    rgb = rgb.clip(0,rgb.max())
    if not dont_plot:
        figure = plt.figure()
        ax = figure.add_subplot(111)
        ax.frameon = False
        ax.set_axis_off()
        ax.imshow(rgb, interpolation = 'nearest')
#        cursors.add_axes(ax)
        figure.canvas.draw()
    else:
        return rgb
        
def subplot_parameters(fig):
    """Returns a list of the subplot paramters of a mpl figure
    
    Parameters
    ----------
    fig : mpl figure
    
    Returns
    -------
    tuple : (left, bottom, right, top, wspace, hspace)
    """
    wspace = fig.subplotpars.wspace
    hspace = fig.subplotpars.hspace
    left = fig.subplotpars.left
    right = fig.subplotpars.right
    top = fig.subplotpars.top
    bottom = fig.subplotpars.bottom
    return (left, bottom, right, top, wspace, hspace)
    
def hspy_figure(extra_buttons=None,
                _on_figure_window_close=None,
                *args, **kwargs):
    """Create a matplotlib figure with some extra features.
    
    This function adds the possibility to execute a function 
    when the figure is closed and to add extra buttons.
    
    
    The button call the gui method of figure.canvas.hspy_obj if it 
    exists.
    
    Parameters
    ----------
    extra_buttons : {tuple of dictionaries}
    
        
    All extra args and kwargs are passed to plt.figure
    

    Returns
    -------
    fig : plt.figure    
    
    """
    if extra_buttons is None:
        fig = plt.figure(*args, **kwargs)
    else:
        for button in extra_buttons:
            if button is None: # It is a separator
                NavigationToolbar2.toolitems += ((None,)*4,)
            else:                        
                NavigationToolbar2.toolitems += (
                    (button['text'], 
                     button['tooltip'], 
                     button['image'],
                     "hspy_" + button['method'] 
                     ),)
                exec(     
                "def action_wrapper(self, *args):"
                "    self.canvas.hspy_%s.gui()" % button['method'])
                setattr(NavigationToolbar2, "hspy_" + button['method'],
                        action_wrapper)
        
        # The buttons image files have to be in 
        # mpl.rcParams['datapath']/images but the hspy logo is not there.
        # As a workaround we have a copy of the NavigationToolbar button
        # images in data/mpl/images and we set the temporarily mpl's
        # datapath to point to hspy/data/mpl, create the figure and 
        # undo the changes.
        button_images = os.path.expandvars(
        os.path.join(
            os.path.dirname(hyperspy.__file__),
            'data',
            'mpl'))
        mpl_datapath = mpl.rcParams['datapath']
        mpl.rcParams['datapath'] = button_images
        fig = plt.figure(*args, **kwargs)
        mpl.rcParams['datapath'] = mpl_datapath
        NavigationToolbar2.toolitems = NavigationToolbar2.toolitems[
            :-len(extra_buttons)]

    if _on_figure_window_close is not None:
        on_figure_window_close(fig, _on_figure_window_close)
    
    return fig
