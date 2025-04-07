#!/usr/bin/env python
import os
import numpy as np
import lsst.daf.butler as daf_butler
import lsst.utils as utils
from bps_config_params import (bps_config_dir, folder, payload_name, survey,
                               sasq_timestamp, tagged_collection, lsst_version,
                               ticket, repo, cache_config_path, output_area)

PACKAGE_DIR = utils.getPackageDir("or5")

step = "step1"

os.makedirs(bps_config_dir, exist_ok=True)

template_file = os.path.join(PACKAGE_DIR, "bps",
                             f"bps_{step}_template.yaml")
with open(template_file) as fobj:
    bps_template = "".join(fobj.readlines())

# Group by exposures
njobs = 10000  # number of concurrent jobs
num_dets = 189  # number of detectors
nexp_groups = int(np.ceil(njobs / num_dets))

# Get exposure list.
butler = daf_butler.Butler(repo, collections=[tagged_collection])
where = "detector=94"
refs = butler.query_datasets("raw", where=where, limit=None)
exposures = sorted(_.dataId["exposure"] for _ in refs)
indices = np.linspace(0, len(exposures), nexp_groups+1, dtype=int)

for igroup, (imin, imax) in enumerate(zip(indices[:-1], indices[1:])):
    group = f"{igroup:02d}"
    exps = exposures[imin:imax]
    exposure_selection = f"(exposure in ({exps[0]}..{exps[-1]}))"
    bps_yaml = os.path.join(bps_config_dir,
                            f"bps_{step}_{payload_name}_{group}.yaml")
    with open(bps_yaml, "w") as fobj:
        fobj.write(bps_template % locals())
