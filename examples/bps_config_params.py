import os
import datetime
import numpy as np
from or5.or5_tracts import or5_wfd_tracts, or5_ddf_tracts

bps_config_dir = "./bps_configs"
lsst_version = "w_2025_11"
sasq_timestamp = datetime.datetime.now().strftime("%Y%m%d")

ticket = "DM-xxxxx"
repo = "embargo_or5"
#repo = "/repo/dc2"
cache_config_path = os.path.join(os.environ['OR5_DIR'], 'config')
#output_area="LSSTCam-imSim/OR5/runs"
output_area="u/jchiang/OR5/runs"

tract_lists, patch_lists = None, None

## WFD
#survey = "WFD"
## Tracts and patches for step3[a,b]
#ngroups = 10
#indices = np.linspace(0, len(or5_wfd_tracts) + 1, ngroups + 1, dtype=int)
#tract_lists = [",".join([str(_) for _ in or5_wfd_tracts[imin:imax]])
#               for imin, imax in zip(indices[:-1], indices[1:])]
#patch_lists = ["0..99"]


# DDF
survey = "DDF"
## Tracts and patches for step3[a,b]
#tract_lists = [str(_) for _ in or5_ddf_tracts]
#patch_lists = ["..".join([str(_) for _ in prange]) for prange in
#               zip((0, 19, 39, 59, 79), (19, 39, 59, 79, 99))]

tagged_collection = f"2.2i/raw/OR5/{survey}/day1/DM-48585"
folder = f"NV_{survey}_day1"
payload_name = f"OR5_{folder}"
