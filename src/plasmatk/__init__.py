from importlib.metadata import version
from importlib_resources import files
import os
from os.path import join as pjoin

__version__ = version(__name__)

src_path = files(__name__).joinpath("cpp")

from . import parameters
from . import plotting


