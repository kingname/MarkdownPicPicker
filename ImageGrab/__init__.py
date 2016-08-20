import sys


system = sys.platform
ImageGrab = None
if system == 'win32':
    from .WinImageGrab import WinImageGrab
    ImageGrab = WinImageGrab
elif system.startswith('darwin'):
    ImageGrab = None
