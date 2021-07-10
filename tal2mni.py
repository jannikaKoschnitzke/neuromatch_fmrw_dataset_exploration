import os, requests
import numpy as np
import nimare.utils as nim
from nilearn import plotting

fname = 'motor_imagery.npz'
url = "https://osf.io/ksqv8/download"

if not os.path.isfile(fname):
  try:
    r = requests.get(url)
  except requests.ConnectionError:
    print("!!! Failed to download data !!!")
  else:
    if r.status_code != requests.codes.ok:
      print("!!! Failed to download data !!!")
    else:
      with open(fname, "wb") as fid:
        fid.write(r.content)

alldat = np.load(fname, allow_pickle=True)['dat']

# pick subject 0 and experiment 0 (real movements), experiment 1 (imaginary) -> can be changed to view other subjects
dat0_mov = alldat[0][0]
dat0_imag = alldat[0][1]


# transform talairach locations to mni
mni_locs1 = nim.tal2mni(dat0_mov['locs'])
mni_locs2 = nim.tal2mni(dat0_imag['locs'])

# adding mni locations to data
dat0_mov['mni_locs'] = mni_locs1
dat0_imag['mni_locs'] = mni_locs2

# visualise locations in 3D (opens in browser)
br0_img_mov = plotting.view_markers(dat0_mov['mni_locs'])
br0_img_mov.open_in_browser()

br0_img_imag = plotting.view_markers(dat0_imag['mni_locs'])
br0_img_imag.open_in_browser()