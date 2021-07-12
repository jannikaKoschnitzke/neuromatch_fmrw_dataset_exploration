import os, requests
import numpy as np
import nimare.utils as nim
from nilearn import plotting
import matplotlib as mp

# Using R inside python
from rpy2 import robjects
import rpy2.robjects.packages as rpackages
from rpy2.robjects.packages import importr
utils = rpackages.importr('utils')
utils.chooseCRANmirror(ind=1)

# install & load R packages
devtools = utils.install_packages('devtools')
custom_analytics = importr('devtools')
custom_analytics.install_github("yunshiuan/label4MRI")
# change lib_loc according to output of previous line (or whereever package is saved)
labels = importr("label4MRI", lib_loc="/home/jannika/R/x86_64-pc-linux-gnu-library/4.1")



# function for visualising subjects electrode locations during both experiments
def showSubjectsElectrodeLocation(subj):

  try:
    mov = "dat" + str(subj) + "_mov"
    imag = "dat" + str(subj) + "_imag"
    br_img_mov = plotting.view_markers(globals()[mov]['mni_locs'],
                                       marker_labels=list(globals()[mov]['aal_label']))
    br_img_mov.open_in_browser()

    br_img_imag = plotting.view_markers(globals()[imag]['mni_locs'],
                                        marker_labels=list(globals()[imag]['aal_label']))
    br_img_imag.open_in_browser()

  except KeyError:
    print("Subject does not exist, please choose a number between 0-6.")


# read in data
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
rregion = robjects.r['mni_to_region_name']
subjNum = range(6)


# generates data sets for all participants and experiments separately (e.g. subject 0, movement experiment: dat0_mov)
for i in subjNum:

  # pick subject i and experiment 0 (real movements), experiment 1 (imaginary)
  mov = alldat[i][0]
  imag = alldat[i][1]

  # transform talairach locations to mni
  mni_locs1 = nim.tal2mni(mov['locs'])
  mni_locs2 = nim.tal2mni(imag['locs'])

  # adding mni locations to data
  mov['mni_locs'] = mni_locs1
  imag['mni_locs'] = mni_locs2

  # rename new datasets according to subject (0, 1,2 ...)
  name_m = "dat" + str(i) + "_mov"
  name_i = "dat" + str(i) + "_imag"
  globals()[name_m] = mov
  globals()[name_i] = imag

  # add region names to datasets (aal and ba)

  mov = "dat" + str(i) + "_mov"
  l_mov = len(globals()[mov]["mni_locs"])
  imag = "dat" + str(i) + "_imag"
  l_imag = len(globals()[imag]["mni_locs"])

  x_m = ['' for i in range(l_mov)]
  x_i = ['' for i in range(l_imag)]

  for j in range(l_mov):
    x = rregion(int(globals()[mov]["mni_locs"][j, 0]), int(globals()[mov]["mni_locs"][j, 1]), int(globals()[mov]["mni_locs"][j, 2]))
    x_m[j] = np.asarray(x.rx2('aal.label'))[0]
    globals()[mov]["aal_label"] = x_m

  for j in range(l_imag):
    y = rregion(int(globals()[imag]["mni_locs"][j, 0]), int(globals()[imag]["mni_locs"][j, 1]), int(globals()[imag]["mni_locs"][j, 2]))
    x_i[j] = np.asarray(y.rx2('aal.label'))[0]
    globals()[imag]["aal_label"] = x_i



# visualise electrode locations for specific subject in 3D (opens in browser)
showSubjectsElectrodeLocation(0)
