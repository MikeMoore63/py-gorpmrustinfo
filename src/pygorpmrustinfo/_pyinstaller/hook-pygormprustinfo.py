import os
from pathlib import Path
from sysconfig import get_config_var

here = Path(__file__).absolute().parent.parent
print(here)
ext_suffix = get_config_var('EXT_SUFFIX')
so_file = os.path.join(here, ('_pygorpmrustinfo' + ext_suffix))

binaries = [(so_file,'.')]
