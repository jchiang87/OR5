import numpy as np
import pandas as pd

step3_template = """pipelineYaml: ${OR5_DIR}/pipelines/DRP.yaml#step3

retryUnlessExit: [2]
numberOfRetries: 2

payload:
  inCollection: u/jchiang/DRP/OR5/WFD/day1/DM-48585/step2
  payloadName: DRP/OR5/WFD/day1/DM-48585/step3/group%(group)02d
  butlerConfig: /repo/dc2
  dataQuery: "instrument='LSSTCam-imSim' and skymap='DC2_cells_v1' and tract in (%(tract_list)s)"
"""

# get tracts from empirical data frame
df = pd.read_parquet("OR5_WFD_day1_ccd_coords.parquet")
tracts = sorted(set(df['tract']))

# divide into 10 groups
indices = np.linspace(0, len(tracts)+1, 11, dtype=int)

for group, (imin, imax) in enumerate(zip(indices[:-1], indices[1:])):
    tract_list = ",".join([str(_) for _ in tracts[imin:imax]])
    outfile = f"bps_DRP_step3_group_{group:02d}.yaml"
    with open(outfile, 'w') as fobj:
        fobj.write(step3_template % locals())
