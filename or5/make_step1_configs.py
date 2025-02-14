import os
import numpy as np
import lsst.daf.butler as daf_butler

step1_template = """pipelineYaml: ${OR5_DIR}/pipelines/DRP.yaml#isr

retryUnlessExit: [2]
numberOfRetries: 2

clusterAlgorithm: lsst.ctrl.bps.quantum_clustering_funcs.dimension_clustering
cluster:
  isr_detector:
    pipetasks: isr
    dimensions: detector

payload:
  weekly: ${WEEKLY}
  inCollection: %(tagged_collection)s,2.2i/calib,skymaps,refcats,pretrained_models
  payloadName: OR5/WFD/day1/step1/isr_detector/{weekly}/%(group)s
  butlerConfig: embargo_or5
  dataQuery: "instrument='LSSTCam-imSim' and %(exposure_selection)s"
"""

repo = "embargo_or5"
tagged_collection = "2.2i/raw/OR5/WDF/day1/DM-48585"
butler = daf_butler.Butler(repo, collections=[tagged_collection])

bps_config_dir = "./bps_configs"
os.makedirs(bps_config_dir, exist_ok=True)

# Group by exposures
njobs = 4000  # number of concurrent jobs
num_dets = 189  # number of detectors
nexp_groups = int(np.ceil(njobs / num_dets))
print(nexp_groups)

# Get exposure list (assuming complete focal planes for all exposures).
where = "detector=94"
refs = butler.query_datasets("raw", where=where, limit=None)
exposures = sorted(_.dataId['exposure'] for _ in refs)
indices = np.linspace(0, len(exposures), nexp_groups+1, dtype=int)

for igroup, (imin, imax) in enumerate(zip(indices[:-1], indices[1:])):
    group = f"{igroup:02d}"
    exps = exposures[imin:imax]
    print(group, len(exps))
    exposure_selection = f"(exposure in ({exps[0]}..{exps[-1]}))"
    bps_yaml = os.path.join(bps_config_dir,
                            f"bps_DRP_step1_isr_detector_{group}.yaml")
#    print(step1_template % locals())
#    print("******")
    with open(bps_yaml, "w") as fobj:
        fobj.write(step1_template % locals())
