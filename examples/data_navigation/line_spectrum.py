"""Creates a line spectrum and plots it
"""

# Create a line spectrum with random data
s = signals.Spectrum({'data' : np.random.random((100,1024))})

# Define the axis properties
s.axes_manager.signal_axes[0].name = 'Energy'
s.axes_manager.signal_axes[0].units = 'eV'
s.axes_manager.signal_axes[0].scale = 0.3
s.axes_manager.signal_axes[0].offset = 100

s.axes_manager.navigation_axes[0].name = 'time'
s.axes_manager.navigation_axes[0].units = 'fs'
s.axes_manager.navigation_axes[0].scale = 0.3
s.axes_manager.navigation_axes[0].offset = 100

# Give a title
s.mapped_parameters.title = 'Random line spectrum'

# Plot it
s.plot()

show() # No necessary when running in the HyperSpy's IPython profile



