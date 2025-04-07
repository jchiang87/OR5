import os
import numpy as np
import lsst.utils as utils
from bps_config_params import (bps_config_dir, folder, payload_name,
                               sasq_timestamp, tagged_collection, lsst_version,
                               ticket, repo, cache_config_path, output_area,
                               tract_lists, patch_lists)

PACKAGE_DIR = utils.getPackageDir("or5")

step = "step3a"

os.makedirs(bps_config_dir, exist_ok=True)

template_file = os.path.join(PACKAGE_DIR, "bps",
                             f"bps_{step}_template.yaml")
with open(template_file) as fobj:
    bps_template = "".join(fobj.readlines())

if tract_lists is not None:
    # Divide into groups.
    igroup = 0
    for tract_list in tract_lists:
        for patch_list in patch_lists:
            group = f"{igroup:002d}"
            bps_yaml = os.path.join(bps_config_dir,
                                    f"bps_{step}_{payload_name}_{group}.yaml")
            with open(bps_yaml, "w") as fobj:
                fobj.write(bps_template % locals())
            igroup += 1
else:
    tract_list = None
    patch_list = None
    bps_yaml = os.path.join(bps_config_dir,
                            f"bps_{step}_{payload_name}.yaml")
    with open(bps_yaml, "w") as fobj:
        fobj.write(bps_template % locals())
