"""Creates a 4D image and plots it
"""

# Create a 2D image stack with random data
im = signals.Image({'data' : np.random.random((16,16,32,32))})

# Define the axis properties
im.axes_manager.signal_axes[0].name = ''
im.axes_manager.signal_axes[0].units = '1/nm'
im.axes_manager.signal_axes[0].scale = 0.1
im.axes_manager.signal_axes[0].offset = 0

im.axes_manager.signal_axes[1].name = ''
im.axes_manager.signal_axes[1].units = '1/nm'
im.axes_manager.signal_axes[1].scale = 0.1
im.axes_manager.signal_axes[1].offset = 0

im.axes_manager.navigation_axes[0].name = 'Y'
im.axes_manager.navigation_axes[0].units = 'nm'
im.axes_manager.navigation_axes[0].scale = 0.3
im.axes_manager.navigation_axes[0].offset = 100

im.axes_manager.navigation_axes[1].name = 'X'
im.axes_manager.navigation_axes[1].units = 'nm'
im.axes_manager.navigation_axes[1].scale = 0.3
im.axes_manager.navigation_axes[1].offset = 100

# Give a title
im.mapped_parameters.title = 'Random 2D image stack'

im.plot()
show() # No necessary when running in the HyperSpy's IPython profile


